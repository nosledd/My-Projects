# AI Automation Platform

Local-first Python foundation for a safety-oriented AI automation platform.

The MVP accepts text, CSV, PDF, and DOCX inputs, asks local Ollama for a
structured CSV/JSON/text output proposal, shows it, and creates a new managed
output only after confirmation.

Install the project dependencies with `python -m pip install -e .`. This
installs `pypdf` for PDFs, `python-docx` for Word documents, and `openpyxl` for
native Excel workbook generation.

For scanned or image-only PDFs, install the optional Python OCR packages with
`python -m pip install -e ".[ocr]"`. You must also install Tesseract OCR and
Poppler on Windows and make both available on your `PATH`.

## Browser interface

Run `./run_web.ps1` in PowerShell, then open `http://127.0.0.1:8080`.
This launcher uses the bundled Python runtime, which includes PDF support.
The local page lets you upload documents, preview the proposed output, and
explicitly approve or cancel creation of the output file.

## Layout

- `src/automation/`: application source package.
- `tests/`: unit, integration, and fixture locations.
- `data/`: managed runtime directories for future uploads, temporary workspace
  files, and generated outputs.
- `logs/`: local operational logs.

Copy `.env.example` to `.env` when configuration is needed. Settings are read
from environment variables at startup.

## Hosting certificate generation

The repository is a monorepo. The deployable application is in `fieldwork/`.
For a small public beta, deploy it as a Docker web service and use
`fieldwork/Dockerfile` from the repository root. It binds to the platform's
`PORT`, exposes `GET /health`, returns a ZIP download link after confirmation,
and removes managed uploads/outputs after `AUTOMATION_RETENTION_MINUTES`.

The Docker configuration disables Gemma (`AUTOMATION_ENABLE_GEMMA=false`) so
the public beta supports deterministic Certificate generation only. Do not
enable generic/Excel AI automation until you have a secured, reachable Ollama
or other model service.
