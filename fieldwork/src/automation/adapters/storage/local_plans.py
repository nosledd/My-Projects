"""Durable JSON storage for pending plans and confirmation state."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Mapping

from automation.domain.errors import ConfirmationRequiredError
from automation.domain.models import (
    ActionCategory,
    ActionPlan,
    ConfirmationRecord,
    PlanStatus,
    Preview,
    ProposedAction,
)


def _json_value(value: object) -> object:
    """Convert immutable domain containers back to JSON-compatible values."""
    if isinstance(value, Mapping):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, tuple | list):
        return [_json_value(item) for item in value]
    if isinstance(value, frozenset | set):
        return sorted(_json_value(item) for item in value)
    return value


class LocalPlanRepository:
    """Store only JSON-compatible plan data; never deserialize executable data."""

    def __init__(self, directory: Path) -> None:
        self._directory = directory
        directory.mkdir(parents=True, exist_ok=True)

    def save(self, plan: ActionPlan, preview: Preview) -> None:
        payload = {
            "plan": {
                "plan_id": plan.plan_id,
                "request_id": plan.request_id,
                "content_hash": plan.content_hash,
                "status": plan.status.value,
                "created_at": plan.created_at.isoformat(),
                "expires_at": plan.expires_at.isoformat(),
                "actions": [
                    {
                        "action_id": action.action_id,
                        "tool_name": action.tool_name,
                        "tool_version": action.tool_version,
                        "category": action.category.value,
                        "arguments": _json_value(action.arguments),
                        "input_artifact_ids": list(action.input_artifact_ids),
                    }
                    for action in plan.actions
                ],
            },
            "preview": {
                "plan_id": preview.plan_id,
                "summary": preview.summary,
                "data": _json_value(preview.data),
                "warnings": list(preview.warnings),
            },
        }
        path = self._path(plan.plan_id)
        temporary = path.with_suffix(".tmp")
        temporary.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        temporary.replace(path)

    def get(self, plan_id: str) -> tuple[ActionPlan, Preview]:
        try:
            payload = json.loads(self._path(plan_id).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ConfirmationRequiredError("pending plan could not be found") from error

        plan_data = payload["plan"]
        actions = tuple(
            ProposedAction(
                action_id=item["action_id"],
                tool_name=item["tool_name"],
                tool_version=item["tool_version"],
                category=ActionCategory(item["category"]),
                arguments=item["arguments"],
                input_artifact_ids=tuple(item["input_artifact_ids"]),
            )
            for item in plan_data["actions"]
        )
        plan = ActionPlan(
            plan_id=plan_data["plan_id"],
            request_id=plan_data["request_id"],
            content_hash=plan_data["content_hash"],
            actions=actions,
            status=PlanStatus(plan_data["status"]),
            created_at=datetime.fromisoformat(plan_data["created_at"]),
            expires_at=datetime.fromisoformat(plan_data["expires_at"]),
        )
        preview_data = payload["preview"]
        return plan, Preview(
            plan_id=preview_data["plan_id"],
            summary=preview_data["summary"],
            data=preview_data["data"],
            warnings=tuple(preview_data["warnings"]),
        )

    def claim(self, confirmation: ConfirmationRecord) -> ActionPlan:
        plan, preview = self.get(confirmation.plan_id)
        if not confirmation.approved or confirmation.plan_content_hash != plan.content_hash:
            raise ConfirmationRequiredError("confirmation does not authorize this plan")
        if plan.status != PlanStatus.AWAITING_CONFIRMATION:
            raise ConfirmationRequiredError("plan was already used")
        claimed = ActionPlan(
            plan_id=plan.plan_id,
            request_id=plan.request_id,
            content_hash=plan.content_hash,
            actions=plan.actions,
            status=PlanStatus.CLAIMED_FOR_EXECUTION,
            created_at=plan.created_at,
            expires_at=plan.expires_at,
        )
        self.save(claimed, preview)
        return claimed

    def _path(self, plan_id: str) -> Path:
        if not plan_id.isalnum():
            raise ConfirmationRequiredError("invalid plan identifier")
        return self._directory / f"{plan_id}.json"
