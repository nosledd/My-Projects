"""Render validated values over selectable placeholders in a PDF certificate."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
import re
from zipfile import ZIP_DEFLATED, ZipFile


PLACEHOLDER = re.compile(r"\{\{\s*([A-Za-z][A-Za-z0-9 _-]*)\s*\}\}")


def safe_stem(value: object) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "_", str(value).strip()).strip("_")
    return text[:60] or "record"


def certificate_filename(row: dict[str, str], index: int) -> str:
    parts = [safe_stem(row.get("Name", "")), safe_stem(row.get("Register No", ""))]
    useful = [part for part in parts if part != "record"]
    return "Certificate_" + ("_".join(useful) if useful else f"{index:03d}") + ".pdf"


def render_certificate(template: Path, mapping: dict[str, str], row: dict[str, str]) -> bytes:
    """Replace text in place and shift its native PDF text matrix to stay centred."""
    try:
        from pypdf import PdfReader, PdfWriter
        from pypdf.generic import ContentStream, FloatObject, NameObject, TextStringObject
        from reportlab.pdfbase.pdfmetrics import stringWidth
    except ImportError as error:
        raise RuntimeError("Certificate PDF rendering requires pypdf and reportlab") from error

    replacements = {"{{" + placeholder + "}}": str(row[column]) for placeholder, column in mapping.items()}
    reader = PdfReader(str(template)); writer = PdfWriter()
    found: set[str] = set()
    for page in reader.pages:
        stream = ContentStream(page.get_contents(), reader)
        fonts = page["/Resources"].get("/Font", {})
        current_font, current_size = "Helvetica", 12.0

        def font_name(resource: object) -> str:
            font = fonts.get(resource)
            if font is None:
                return "Helvetica"
            base = str(font.get_object().get("/BaseFont", "/Helvetica")).lstrip("/")
            return base if base in {"Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Helvetica-BoldOblique", "Times-Roman", "Times-Bold", "Courier", "Courier-Bold"} else "Helvetica"

        def shift_current_matrix(index: int, old: str, new: str) -> None:
            """Centre the new native-font text around the old token's centre."""
            delta = (stringWidth(old, current_font, current_size) - stringWidth(new, current_font, current_size)) / 2
            for previous in range(index - 1, -1, -1):
                operands, operation = stream.operations[previous]
                if operation == b"Tm" and len(operands) >= 6:
                    operands[4] = FloatObject(float(operands[4]) + delta)
                    return
                if operation == b"BT":
                    return

        for index, (operands, operator) in enumerate(stream.operations):
            if operator == b"Tf" and len(operands) >= 2:
                current_font, current_size = font_name(operands[0]), float(operands[1])
                continue
            if operator not in {b"Tj", b"'"} or not operands or not isinstance(operands[0], TextStringObject):
                continue
            original = str(operands[0])
            for placeholder, replacement in replacements.items():
                if placeholder in original:
                    # Templates normally emit each placeholder in its own Tj operation.
                    # Native font, colour, and design remain unchanged; only x changes.
                    shift_current_matrix(index, placeholder, replacement)
                    operands[0] = TextStringObject(original.replace(placeholder, replacement))
                    found.add(placeholder)
                    break
        page[NameObject("/Contents")] = stream
        writer.add_page(page)
    missing = set(replacements) - found
    if missing:
        raise ValueError("Template placeholder text could not be replaced: " + ", ".join(sorted(missing)))
    output = BytesIO(); writer.write(output); return output.getvalue()


def make_zip(files: dict[str, bytes]) -> bytes:
    output = BytesIO()
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for name, content in files.items():
            archive.writestr(name, content)
    return output.getvalue()
