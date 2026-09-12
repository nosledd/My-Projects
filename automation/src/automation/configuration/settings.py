"""Validated runtime settings loaded from environment variables."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import os

@dataclass(frozen=True, slots=True)
class Settings:
    root: Path
    ollama_url: str
    ollama_model: str
    log_level: str
    @property
    def uploads_dir(self) -> Path: return self.root / "data" / "uploads"
    @property
    def outputs_dir(self) -> Path: return self.root / "data" / "outputs"
    @property
    def workspace_dir(self) -> Path: return self.root / "data" / "workspace"
    @property
    def plans_dir(self) -> Path: return self.workspace_dir / "plans"
    @classmethod
    def from_environment(cls, root: Path) -> "Settings":
        return cls(root.resolve(), os.getenv("AUTOMATION_OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/"), os.getenv("AUTOMATION_OLLAMA_MODEL", "gemma3:4b"), os.getenv("AUTOMATION_LOG_LEVEL", "INFO"))
