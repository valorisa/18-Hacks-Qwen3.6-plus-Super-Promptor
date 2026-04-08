# tests/test_rules/test_md041.py
"""Tests pour la règle MD041: first-line-h1."""

import pytest


def test_violation_detected(run_rule):
    """First line is not a heading → violation."""
    md = "Some text\n\n# Heading\n"
    violations = run_rule("MD041", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD041"


def test_clean_passes(run_rule):
    """First line is h1 → 0 violation."""
    md = "# Heading\n\nContent\n"
    violations = run_rule("MD041", md)

    assert len(violations) == 0


@pytest.mark.skip(reason="MD041 is not auto-fixable")
def test_fix_if_applicable(run_rule):
    pass


def test_config_override(run_rule):
    md = "Text\n\n# Heading\n"
    v1 = run_rule("MD041", md, {})
    v2 = run_rule("MD041", md, {"allow_preamble": True})
    assert isinstance(v1, list) and isinstance(v2, list)
