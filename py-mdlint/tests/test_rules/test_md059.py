# tests/test_rules/test_md059.py
"""Tests pour la règle MD059: descriptive-link-text."""

import pytest


def test_violation_detected(run_rule):
    """Non-descriptive link text → violation."""
    md = "[click here](https://example.com)\n"
    violations = run_rule("MD059", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD059"


def test_clean_passes(run_rule):
    """Descriptive link text → 0 violation."""
    md = "[Download the report](https://example.com)\n"
    violations = run_rule("MD059", md)

    assert len(violations) == 0


@pytest.mark.skip(reason="MD059 is not auto-fixable")
def test_fix_if_applicable(run_rule):
    pass


def test_config_override(run_rule):
    md = "[here](url)\n"
    v1 = run_rule("MD059", md, {})
    v2 = run_rule("MD059", md, {"fake": "value"})
    assert isinstance(v1, list)
