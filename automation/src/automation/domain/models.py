"""Immutable domain records shared by future automation workflows.

These models describe requests, artifacts, plans, previews, confirmations, and
execution outcomes. They intentionally contain no I/O, tool execution, LLM calls,
or policy decisions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping


def _freeze_value(value: object) -> object:
    """Convert common mutable containers into immutable equivalents."""
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze_value(item) for key, item in value.items()})
    if isinstance(value, list | tuple):
        return tuple(_freeze_value(item) for item in value)
    if isinstance(value, set | frozenset):
        return frozenset(_freeze_value(item) for item in value)
    return value


class ArtifactKind(StrEnum):
    """The broad representation of an artifact managed by the platform."""

    FILE = "file"
    STRUCTURED_DATA = "structured_data"
    TEXT = "text"


class ActionCategory(StrEnum):
    """The side-effect category declared by a proposed tool action."""

    READ_ONLY = "read_only"
    PREPARATION = "preparation"
    CREATE_OUTPUT = "create_output"
    MODIFY_EXISTING = "modify_existing"
    DELETE = "delete"
    SYSTEM_COMMAND = "system_command"
    NETWORK_ACTION = "network_action"


class PlanStatus(StrEnum):
    """The permitted lifecycle states of an immutable action plan."""

    DRAFT = "draft"
    VALIDATED = "validated"
    PREPARED = "prepared"
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    CONFIRMED = "confirmed"
    CLAIMED_FOR_EXECUTION = "claimed_for_execution"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


@dataclass(frozen=True, slots=True)
class ArtifactReference:
    """Metadata identifying an artifact without exposing filesystem operations."""

    artifact_id: str
    kind: ArtifactKind
    media_type: str
    content_hash: str
    display_name: str
    size_bytes: int | None = None

    def __post_init__(self) -> None:
        if not self.artifact_id:
            raise ValueError("artifact_id must not be empty")
        if not self.media_type:
            raise ValueError("media_type must not be empty")
        if not self.content_hash:
            raise ValueError("content_hash must not be empty")
        if not self.display_name:
            raise ValueError("display_name must not be empty")
        if self.size_bytes is not None and self.size_bytes < 0:
            raise ValueError("size_bytes must be zero or greater")


@dataclass(frozen=True, slots=True)
class UserRequest:
    """A user's natural-language request and its approved input artifacts."""

    request_id: str
    instruction: str
    input_artifacts: tuple[ArtifactReference, ...]
    created_at: datetime

    def __post_init__(self) -> None:
        if not self.request_id:
            raise ValueError("request_id must not be empty")
        if not self.instruction.strip():
            raise ValueError("instruction must not be blank")


@dataclass(frozen=True, slots=True)
class ProposedAction:
    """A schema-validated intent to invoke one named tool."""

    action_id: str
    tool_name: str
    tool_version: str
    category: ActionCategory
    arguments: Mapping[str, object]
    input_artifact_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.action_id:
            raise ValueError("action_id must not be empty")
        if not self.tool_name:
            raise ValueError("tool_name must not be empty")
        if not self.tool_version:
            raise ValueError("tool_version must not be empty")
        object.__setattr__(
            self,
            "arguments",
            MappingProxyType(
                {key: _freeze_value(value) for key, value in self.arguments.items()},
            ),
        )


@dataclass(frozen=True, slots=True)
class ActionPlan:
    """An immutable proposed workflow associated with one user request."""

    plan_id: str
    request_id: str
    content_hash: str
    actions: tuple[ProposedAction, ...]
    status: PlanStatus
    created_at: datetime
    expires_at: datetime

    def __post_init__(self) -> None:
        if not self.plan_id:
            raise ValueError("plan_id must not be empty")
        if not self.request_id:
            raise ValueError("request_id must not be empty")
        if not self.content_hash:
            raise ValueError("content_hash must not be empty")
        if not self.actions:
            raise ValueError("actions must contain at least one action")
        if self.expires_at <= self.created_at:
            raise ValueError("expires_at must be later than created_at")


@dataclass(frozen=True, slots=True)
class Preview:
    """A user-reviewable description of a plan's expected outcome."""

    plan_id: str
    summary: str
    data: Mapping[str, object] = field(default_factory=dict)
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.plan_id:
            raise ValueError("plan_id must not be empty")
        if not self.summary.strip():
            raise ValueError("summary must not be blank")
        object.__setattr__(
            self,
            "data",
            MappingProxyType(
                {key: _freeze_value(value) for key, value in self.data.items()},
            ),
        )


@dataclass(frozen=True, slots=True)
class ConfirmationRecord:
    """A user's decision for one exact version of a proposed plan."""

    confirmation_id: str
    plan_id: str
    plan_content_hash: str
    approved: bool
    decided_at: datetime

    def __post_init__(self) -> None:
        if not self.confirmation_id:
            raise ValueError("confirmation_id must not be empty")
        if not self.plan_id:
            raise ValueError("plan_id must not be empty")
        if not self.plan_content_hash:
            raise ValueError("plan_content_hash must not be empty")


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    """The terminal outcome of executing an approved action plan."""

    execution_id: str
    plan_id: str
    status: PlanStatus
    completed_at: datetime
    output_artifacts: tuple[ArtifactReference, ...] = ()
    summary: str = ""
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.execution_id:
            raise ValueError("execution_id must not be empty")
        if not self.plan_id:
            raise ValueError("plan_id must not be empty")
        if self.status not in {PlanStatus.COMPLETED, PlanStatus.FAILED}:
            raise ValueError("execution result status must be completed or failed")
