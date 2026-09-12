"""Tests for non-bypassable initial safety decisions."""

import pytest

from automation.domain.errors import SafetyPolicyError
from automation.domain.models import ActionCategory, ProposedAction
from automation.domain.policies import SafetyPolicy


def _action(category: ActionCategory) -> ProposedAction:
    return ProposedAction("action", "test.tool", "1", category, {})


def test_creating_an_output_requires_confirmation() -> None:
    assert SafetyPolicy().requires_confirmation(_action(ActionCategory.CREATE_OUTPUT))


@pytest.mark.parametrize(
    "category",
    [
        ActionCategory.MODIFY_EXISTING,
        ActionCategory.DELETE,
        ActionCategory.SYSTEM_COMMAND,
        ActionCategory.NETWORK_ACTION,
    ],
)
def test_unsafe_categories_are_forbidden(category: ActionCategory) -> None:
    with pytest.raises(SafetyPolicyError):
        SafetyPolicy().validate(_action(category))
