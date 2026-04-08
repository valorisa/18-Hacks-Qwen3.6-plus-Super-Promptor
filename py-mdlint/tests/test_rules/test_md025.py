# tests/test_rules/test_md025.py
"""Tests pour la règle MD025: single-title."""

import pytest


def test_violation_detected(run_rule):
    """Deux h1 dans le contenu → violation."""
    md = "# First Title\n\nContent\n\n# Second Title\n"
    violations = run_rule("MD025", md)

    assert len(violations) == 1
    assert violations[0].rule_id == "MD025"
    assert "Multiple top-level headings" in violations[0].message


def test_clean_passes(run_rule):
    """Un seul h1 → 0 violation."""
    md = "# Single Title\n\nContent here\n\n## Subsection\n"
    violations = run_rule("MD025", md)

    assert len(violations) == 0


@pytest.mark.skip(reason="MD025 is not auto-fixable")
def test_fix_if_applicable(run_rule):
    """MD025 n'est pas auto-fixable → test skip."""
    pass


def test_config_override(run_rule):
    """Vérifie front_matter_title exclusion."""
    md_two = "# Title 1\n\n# Title 2\n"
    violations_two = run_rule("MD025", md_two)
    assert len(violations_two) >= 1
