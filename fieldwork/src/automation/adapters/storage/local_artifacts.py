"""Managed local artifact storage; never accepts arbitrary output paths."""
from __future__ import annotations
from hashlib import sha256
from pathlib import Path
from time import time
from uuid import uuid4
from automation.domain.models import ArtifactKind, ArtifactReference

class LocalArtifactStore:
    def __init__(self, uploads: Path, outputs: Path) -> None:
        self._uploads, self._outputs = uploads.resolve(), outputs.resolve()
        self._uploads.mkdir(parents=True, exist_ok=True); self._outputs.mkdir(parents=True, exist_ok=True)
    def ingest(self, path: Path) -> ArtifactReference:
        resolved = path.resolve()
        if not resolved.is_file(): raise ValueError("input file does not exist")
        target = self._uploads / f"{uuid4().hex}_{resolved.name}"
        target.write_bytes(resolved.read_bytes())
        return self._reference(target, ArtifactKind.FILE)
    def read_text(self, artifact_id: str) -> str:
        path = self._find(self._uploads, artifact_id)
        suffix = path.suffix.lower()
        if suffix in {".txt", ".md", ".json", ".csv"}: return path.read_text(encoding="utf-8", errors="replace")
        if suffix == ".pdf": return self._read_pdf(path)
        if suffix == ".docx":
            try:
                from docx import Document
                return "\n".join(p.text for p in Document(str(path)).paragraphs)
            except ImportError as error: raise RuntimeError("DOCX support requires python-docx") from error
        raise ValueError(f"unsupported input format: {suffix}")

    def path_for(self, artifact_id: str) -> Path:
        """Return a managed input path for a specialised local tool."""
        return self._find(self._uploads, artifact_id)

    def output_path_for(self, artifact_id: str) -> Path:
        """Return one managed output selected by its unguessable artifact ID."""
        return self._find(self._outputs, artifact_id)

    def cleanup_expired(self, max_age_seconds: int) -> int:
        """Remove only old managed uploads and outputs for a short-lived web beta."""
        cutoff = time() - max_age_seconds
        removed = 0
        for directory in (self._uploads, self._outputs):
            for path in directory.iterdir():
                if path.is_file() and path.name != ".gitkeep" and path.stat().st_mtime < cutoff:
                    path.unlink(missing_ok=True)
                    removed += 1
        return removed
    def create_output(self, name: str, media_type: str, content: bytes) -> ArtifactReference:
        safe_name = Path(name).name
        if safe_name != name or not safe_name: raise ValueError("invalid output name")
        path = self._outputs / f"{uuid4().hex}_{safe_name}"
        temp = path.with_suffix(path.suffix + ".tmp"); temp.write_bytes(content); temp.replace(path)
        return self._reference(path, ArtifactKind.FILE)
    def _find(self, root: Path, artifact_id: str) -> Path:
        matches = list(root.glob(f"{artifact_id}_*"))
        if len(matches) != 1: raise ValueError("unknown artifact")
        return matches[0]
    def _reference(self, path: Path, kind: ArtifactKind) -> ArtifactReference:
        data = path.read_bytes(); return ArtifactReference(path.name.split("_", 1)[0], kind, "application/octet-stream", sha256(data).hexdigest(), path.name.split("_", 1)[1], len(data))

    def _read_pdf(self, path: Path) -> str:
        """Prefer embedded text; use local OCR only for image-only PDFs."""
        try:
            from pypdf import PdfReader
        except ImportError as error: raise RuntimeError("PDF support requires pypdf") from error
        text = "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages).strip()
        return text if text else self._ocr_pdf(path)

    @staticmethod
    def _ocr_pdf(path: Path) -> str:
        from automation.adapters.readers.layout_ocr import LayoutOcrReader
        return LayoutOcrReader().read_pdf(path)
