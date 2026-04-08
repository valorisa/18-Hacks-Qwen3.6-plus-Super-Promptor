# tests/test_rules/test_md042.py
"""Tests pour la règle MD042: no-empty-links."""

import pytest


def test_violation_detected(run_rule):
    """Empty link → violation."""
    md = "[click here]()\n"
    violations = run_rule("MD042", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD042"


def test_clean_passes(run_rule):
    """Valid link → 0 violation."""
    md = "[click here](https://example.com)\n"
    violations = run_rule("MD042", md)

    assert len(violations) == 0


@pytest.mark.skip(reason="MD042 is not auto-fixable")
def test_fix_if_applicable(run_rule):
    pass


def test_config_override(run_rule):
    md = "[link]()\n"
    v1 = run_rule("MD042", md, {})
    v2 = run_rule("MD042", md, {"fake": "value"})
    assert isinstance(v1, list)
