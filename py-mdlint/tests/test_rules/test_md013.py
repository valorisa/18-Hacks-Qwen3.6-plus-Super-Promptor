# tests/test_rules/test_md013.py
"""Tests pour la règle MD013: line-length."""

import pytest


def test_violation_detected(run_rule):
    """Line longer than 80 chars → violation."""
    md = "This is a very long line that exceeds the default eighty character limit for markdown linting purposes and should trigger a violation\n"
    violations = run_rule("MD013", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD013"


def test_clean_passes(run_rule):
    """Short lines → 0 violation."""
    md = "Short line\nAnother short line\n"
    violations = run_rule("MD013", md)

    assert len(violations) == 0


@pytest.mark.skip(reason="MD013 is not auto-fixable")
def test_fix_if_applicable(run_rule):
    pass


def test_config_override(run_rule):
    md = "This is a moderately long line that is over fifty but under eighty characters long for testing\n"
    v1 = run_rule("MD013", md, {"line_length": 80})
    v2 = run_rule("MD013", md, {"line_length": 50})
    assert len(v2) >= len(v1)
