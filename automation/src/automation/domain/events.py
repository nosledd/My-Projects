"""Small immutable audit event record shared by future event publishers."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True, slots=True)
class AuditEvent:
    """A redaction-ready event describing a platform lifecycle occurrence."""

    event_type: str
    occurred_at: datetime
    request_id: str
    details: Mapping[str, object] = field(default_factory=dict)
    plan_id: str | None = None
    action_id: str | None = None

    def __post_init__(self) -> None:
        if not self.event_type or not self.request_id:
            raise ValueError("event_type and request_id must not be empty")
        object.__setattr__(self, "details", MappingProxyType(dict(self.details)))
