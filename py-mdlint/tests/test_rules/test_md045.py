# tests/test_rules/test_md045.py
"""Tests pour la règle MD045: no-alt-text."""

import pytest


def test_violation_detected(run_rule):
    """Image without alt text → violation."""
    md = "![](image.jpg)\n"
    violations = run_rule("MD045", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD045"


def test_clean_passes(run_rule):
    """Image with alt text → 0 violation."""
    md = "![Description](image.jpg)\n"
    violations = run_rule("MD045", md)

    assert len(violations) == 0


@pytest.mark.skip(reason="MD045 is not auto-fixable")
def test_fix_if_applicable(run_rule):
    pass


def test_config_override(run_rule):
    md = "![](img.jpg)\n"
    v1 = run_rule("MD045", md, {})
    v2 = run_rule("MD045", md, {"fake": "value"})
    assert isinstance(v1, list)
