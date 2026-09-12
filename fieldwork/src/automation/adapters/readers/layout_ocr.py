"""Coordinate-aware OCR for scanned documents and visually structured tables."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import shutil


@dataclass(frozen=True, slots=True)
class OcrWord:
    """One OCR token with its page-relative bounding box."""

    page_number: int
    text: str
    left: int
    top: int
    width: int
    height: int
    confidence: float


class LayoutOcrReader:
    """Extract OCR words while preserving their visual positions for planning."""

    def read_pdf(self, path: Path) -> str:
        tesseract_path = self._tesseract_path()
        if tesseract_path is None:
            raise RuntimeError("This is a scanned PDF. Install Tesseract OCR, then restart the application.")
        try:
            from pdf2image import convert_from_path
            import pytesseract
        except ImportError as error:
            raise RuntimeError("Scanned-PDF support requires the OCR dependencies. Install the project's ocr extra.") from error
        pytesseract.pytesseract.tesseract_cmd = str(tesseract_path)
        try:
            images = convert_from_path(str(path), dpi=250, thread_count=1)
            words = [word for number, image in enumerate(images, start=1) for word in self._page_words(pytesseract, image, number)]
        except Exception as error:
            raise RuntimeError("OCR could not read this PDF. Check the local Tesseract and Poppler setup.") from error
        if not words:
            raise RuntimeError("OCR found no readable text in this PDF.")
        return self._layout_text(words)

    @staticmethod
    def _tesseract_path() -> Path | None:
        configured = os.getenv("AUTOMATION_TESSERACT_PATH")
        candidates = [configured] if configured else []
        candidates.append(shutil.which("tesseract"))
        candidates.append(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
        for candidate in candidates:
            if candidate and Path(candidate).is_file():
                return Path(candidate)
        return None

    @staticmethod
    def _page_words(pytesseract: object, image: object, page_number: int) -> list[OcrWord]:
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, config="--psm 6")
        words: list[OcrWord] = []
        for index, raw in enumerate(data["text"]):
            text = raw.strip()
            try:
                confidence = float(data["conf"][index])
            except (TypeError, ValueError):
                confidence = -1.0
            if text and confidence >= 0:
                words.append(OcrWord(page_number, text, int(data["left"][index]), int(data["top"][index]), int(data["width"][index]), int(data["height"][index]), confidence))
        return words

    @staticmethod
    def _layout_text(words: list[OcrWord]) -> str:
        """Emit page/row/x-coordinate text without pretending OCR is a perfect table."""
        lines: list[str] = ["[OCR_LAYOUT: every token includes its x-position; preserve row and column relationships]"]
        page_words: dict[int, list[OcrWord]] = {}
        for word in words:
            page_words.setdefault(word.page_number, []).append(word)
        for page, tokens in page_words.items():
            rows: list[list[OcrWord]] = []
            for token in sorted(tokens, key=lambda item: (item.top, item.left)):
                if not rows or abs(token.top - rows[-1][0].top) > max(12, token.height):
                    rows.append([token])
                else:
                    rows[-1].append(token)
            lines.append(f"[PAGE {page}]")
            for row in rows:
                cells = " | ".join(f"x={word.left}:{word.text}" for word in sorted(row, key=lambda item: item.left))
                lines.append(cells)
        return "\n".join(lines)
