"""Deterministic safety rules for proposed actions."""

from __future__ import annotations

from .errors import SafetyPolicyError
from .models import ActionCategory, ProposedAction


class SafetyPolicy:
    """Classify actions independently of user and model instructions."""

    _forbidden = frozenset(
        {
            ActionCategory.MODIFY_EXISTING,
            ActionCategory.DELETE,
            ActionCategory.SYSTEM_COMMAND,
            ActionCategory.NETWORK_ACTION,
        },
    )
    _requires_confirmation = frozenset({ActionCategory.CREATE_OUTPUT})

    def validate(self, action: ProposedAction) -> None:
        """Reject actions that the initial local platform never permits."""
        if action.category in self._forbidden:
            raise SafetyPolicyError(f"action category is forbidden: {action.category}")

    def requires_confirmation(self, action: ProposedAction) -> bool:
        """Return whether execution requires a plan-bound user approval."""
        self.validate(action)
        return action.category in self._requires_confirmation

