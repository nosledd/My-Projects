"""Errors that express domain failures without leaking infrastructure details."""


class AutomationError(Exception):
    """Base error for the automation platform."""


class SafetyPolicyError(AutomationError):
    """Raised when an action is disallowed by platform policy."""


class ConfirmationRequiredError(AutomationError):
    """Raised when a confirmation-gated action is attempted too early."""


class InvalidPlanStateError(AutomationError):
    """Raised when a requested plan lifecycle transition is invalid."""

