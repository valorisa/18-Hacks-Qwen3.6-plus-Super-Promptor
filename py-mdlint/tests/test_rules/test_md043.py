# tests/test_rules/test_md043.py
"""Tests pour la règle MD043: required-headings."""

import pytest


def test_violation_detected(run_rule):
    """Heading structure doesn't match required → violation."""
    md = "# Intro\n\n## Details\n"
    violations = run_rule("MD043", md, {"headings": ["# Intro", "## Missing"]})

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD043"


def test_clean_passes(run_rule):
    """Heading structure matches → 0 violation."""
    md = "# Intro\n\n## Details\n"
    violations = run_rule("MD043", md, {"headings": ["# Intro", "## Details"]})

    assert len(violations) == 0


@pytest.mark.skip(reason="MD043 is not auto-fixable")
def test_fix_if_applicable(run_rule):
    pass


def test_config_override(run_rule):
    md = "# Title\n\n## Section\n"
    v1 = run_rule("MD043", md, {"headings": ["#"]})
    v2 = run_rule("MD043", md, {"headings": ["*", "## Section"]})
    assert isinstance(v1, list) and isinstance(v2, list)
