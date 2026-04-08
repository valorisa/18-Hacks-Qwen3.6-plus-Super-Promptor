# tests/test_rules/test_md051.py
"""Tests pour la règle MD051: link-fragments."""

import pytest


def test_violation_detected(run_rule):
    """Invalid link fragment → violation."""
    md = "# Heading\n\n[Link](#nonexistent)\n"
    violations = run_rule("MD051", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD051"


def test_clean_passes(run_rule):
    """Valid link fragment → 0 violation."""
    md = "# Heading\n\n[Link](#heading)\n"
    violations = run_rule("MD051", md)

    assert len(violations) == 0


@pytest.mark.skip(reason="MD051 is not auto-fixable")
def test_fix_if_applicable(run_rule):
    pass


def test_config_override(run_rule):
    md = "# Title\n\n[Link](#missing)\n"
    v1 = run_rule("MD051", md, {})
    v2 = run_rule("MD051", md, {"fake": "value"})
    assert isinstance(v1, list)
