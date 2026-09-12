"""Unit tests for domain model invariants."""

from datetime import datetime, timedelta, timezone

import pytest

from automation.domain.models import (
    ActionCategory,
    ActionPlan,
    PlanStatus,
    ProposedAction,
)


def test_action_plan_rejects_expiry_at_or_before_creation() -> None:
    created_at = datetime.now(timezone.utc)
    action = ProposedAction(
        action_id="action-1",
        tool_name="pdf.extract_fields",
        tool_version="1.0.0",
        category=ActionCategory.READ_ONLY,
        arguments={},
    )

    with pytest.raises(ValueError, match="expires_at"):
        ActionPlan(
            plan_id="plan-1",
            request_id="request-1",
            content_hash="content-hash",
            actions=(action,),
            status=PlanStatus.DRAFT,
            created_at=created_at,
            expires_at=created_at - timedelta(seconds=1),
        )


def test_proposed_action_copies_arguments_into_an_immutable_mapping() -> None:
    arguments = {"fields": ["invoice_number"]}
    action = ProposedAction(
        action_id="action-1",
        tool_name="pdf.extract_fields",
        tool_version="1.0.0",
        category=ActionCategory.READ_ONLY,
        arguments=arguments,
    )

    arguments["fields"] = ["total"]

    assert action.arguments["fields"] == ("invoice_number",)
    with pytest.raises(TypeError):
        action.arguments["output_name"] = "report.xlsx"  # type: ignore[index]
