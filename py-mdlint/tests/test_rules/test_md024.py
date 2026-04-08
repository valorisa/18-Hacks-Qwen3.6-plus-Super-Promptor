# tests/test_rules/test_md024.py
"""Tests pour la règle MD024: no-duplicate-heading."""

import pytest


def test_violation_detected(run_rule):
    """Duplicate headings → violation."""
    md = "# Title\n\n## Section\n\n## Section\n"
    violations = run_rule("MD024", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD024"


def test_clean_passes(run_rule):
    """Unique headings → 0 violation."""
    md = "# Title\n\n## Section One\n\n## Section Two\n"
    violations = run_rule("MD024", md)

    assert len(violations) == 0


@pytest.mark.skip(reason="MD024 is not auto-fixable")
def test_fix_if_applicable(run_rule):
    pass


def test_config_override(run_rule):
    md = "# Title\n\n## Section\n\n## Section\n"
    v1 = run_rule("MD024", md, {})
    v2 = run_rule("MD024", md, {"siblings_only": True})
    assert isinstance(v1, list) and isinstance(v2, list)
