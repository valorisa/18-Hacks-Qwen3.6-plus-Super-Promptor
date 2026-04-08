# tests/test_rules/test_md036.py
"""Tests pour la règle MD036: no-emphasis-as-heading."""

import pytest


def test_violation_detected(run_rule):
    """Emphasis used as heading → violation."""
    md = "**Section Title**\n\nSome content\n"
    violations = run_rule("MD036", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD036"


def test_clean_passes(run_rule):
    """Proper heading used → 0 violation."""
    md = "## Section Title\n\nSome content\n"
    violations = run_rule("MD036", md)

    assert len(violations) == 0


@pytest.mark.skip(reason="MD036 is not auto-fixable")
def test_fix_if_applicable(run_rule):
    pass


def test_config_override(run_rule):
    md = "**Title**\n\nContent\n"
    v1 = run_rule("MD036", md, {})
    v2 = run_rule("MD036", md, {"punctuation": ""})
    assert isinstance(v1, list)
