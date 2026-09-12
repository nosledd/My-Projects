"""Plan-bound confirmation validation."""
from __future__ import annotations
from datetime import datetime, timezone
from automation.domain.errors import ConfirmationRequiredError
from automation.domain.models import ActionPlan, ConfirmationRecord, PlanStatus

def confirm(plan: ActionPlan, approved: bool, confirmation_id: str) -> ConfirmationRecord:
    if plan.status.value != PlanStatus.AWAITING_CONFIRMATION.value:
        raise ConfirmationRequiredError("plan is not awaiting confirmation")
    if datetime.now(timezone.utc) >= plan.expires_at:
        raise ConfirmationRequiredError("plan has expired")
    return ConfirmationRecord(confirmation_id, plan.plan_id, plan.content_hash, approved, datetime.now(timezone.utc))
