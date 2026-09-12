"""Stateless Vercel endpoints for the certificate-only public demo.

Each request processes its uploaded files in a temporary directory.  No
uploaded document, pending plan, or output is retained after a response.
"""

from __future__ import annotations

from contextlib import contextmanager
from io import BytesIO
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

from flask import Flask, jsonify, request, send_file


PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from automation.adapters.tools.certificate_output import (  # noqa: E402
    certificate_filename,
    make_zip,
    render_certificate,
)
from automation.application.certificate_planning import (  # noqa: E402
    detect_placeholders,
    normalise_name,
    read_workbook_rows,
)


MAX_UPLOAD_BYTES = 4 * 1024 * 1024
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_BYTES


def _error(message: str, status: int = 400):
    return jsonify({"error": message}), status


def _files() -> tuple[object, object]:
    template = request.files.get("template")
    workbook = request.files.get("workbook")
    if template is None or workbook is None:
        raise ValueError("Upload one PDF certificate template and one XLSX data spreadsheet.")
    if not template.filename.lower().endswith(".pdf"):
        raise ValueError("The certificate template must be a PDF file.")
    if not workbook.filename.lower().endswith(".xlsx"):
        raise ValueError("The data file must be an .xlsx spreadsheet.")
    return template, workbook


@contextmanager
def _prepare(template_upload: object, workbook_upload: object):
    """Validate the two uploads and return the deterministic certificate plan."""
    with TemporaryDirectory(prefix="fieldwork-") as directory:
        root = Path(directory)
        template_path = root / "template.pdf"
        workbook_path = root / "data.xlsx"
        template_upload.save(template_path)
        workbook_upload.save(workbook_path)

        placeholders = detect_placeholders(template_path)
        headers, rows = read_workbook_rows(workbook_path)
        column_by_name = {normalise_name(header): header for header in headers}
        mapping = {
            placeholder: column_by_name.get(normalise_name(placeholder))
            for placeholder in placeholders
        }
        missing = [placeholder for placeholder, header in mapping.items() if header is None]
        if missing:
            values = ", ".join("{{" + value + "}}" for value in missing)
            raise ValueError("Missing Excel columns for: " + values)
        required = tuple(header for header in mapping.values() if header is not None)
        blank_rows = [
            index + 2
            for index, row in enumerate(rows)
            if any(not row[header].strip() for header in required)
        ]
        if blank_rows:
            values = ", ".join(map(str, blank_rows[:10]))
            raise ValueError("Required certificate values are blank in Excel row(s): " + values)
        yield template_path, mapping, rows, headers, required


@app.get("/")
def homepage():
    """Serve the public certificate interface."""
    return send_file(PROJECT_ROOT / "index.html", mimetype="text/html")


@app.post("/api/preview")
def preview():
    """Validate inputs and return a preview.  No output file is created here."""
    try:
        template, workbook = _files()
        with _prepare(template, workbook) as plan:
            _, mapping, rows, headers, required = plan
            unused = [header for header in headers if header not in required]
            return jsonify(
                {
                    "summary": f"Ready to generate {len(rows)} certificate PDF(s) in one ZIP file.",
                    "data": {
                        "columns": ["Certificate placeholder", "Excel column"],
                        "rows": [["{{" + key + "}}", value] for key, value in mapping.items()],
                        "record_count": len(rows),
                        "example": rows[0],
                    },
                    "warnings": ["Unused Excel column: " + header for header in unused],
                }
            )
    except ValueError as error:
        return _error(str(error))
    except Exception:
        return _error("The files could not be processed. Confirm that the PDF uses selectable {{PLACEHOLDER}} text and the spreadsheet is valid.")


@app.post("/api/create")
def create():
    """Generate the ZIP only after the browser submits an explicit approval."""
    try:
        template, workbook = _files()
        with _prepare(template, workbook) as plan:
            template_path, mapping, rows, _, _ = plan
            files = {
                certificate_filename(row, index): render_certificate(template_path, mapping, row)
                for index, row in enumerate(rows, start=1)
            }
            archive = make_zip(files)
        if len(archive) > MAX_UPLOAD_BYTES:
            return _error("The generated ZIP is too large for the Vercel demo. Use fewer records or a smaller template.", 413)
        return send_file(
            BytesIO(archive),
            mimetype="application/zip",
            as_attachment=True,
            download_name="certificates.zip",
        )
    except ValueError as error:
        return _error(str(error))
    except Exception:
        return _error("The certificates could not be created. Check the placeholder template and Excel data, then try again.")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "fieldwork-vercel-certificate-demo"})


@app.errorhandler(413)
def too_large(_: object):
    return _error("The PDF and XLSX together must be smaller than 4 MB for the Vercel demo.", 413)
