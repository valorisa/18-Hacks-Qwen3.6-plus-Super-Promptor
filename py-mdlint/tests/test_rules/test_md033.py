# tests/test_rules/test_md033.py
"""Tests pour la règle MD033: no-inline-html."""

import pytest


def test_violation_detected(run_rule):
    """HTML inline non autorisé → violation."""
    md = "Text with <span>inline HTML</span>\n"
    violations = run_rule("MD033", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD033"
    assert "span" in violations[0].message


def test_clean_passes(run_rule):
    """Pas d'HTML inline → 0 violation."""
    md = "Just **Markdown** and *no* HTML here.\n"
    violations = run_rule("MD033", md)

    assert len(violations) == 0


@pytest.mark.skip(reason="MD033 is not auto-fixable")
def test_fix_if_applicable(run_rule):
    """MD033 n'est pas auto-fixable → test skip."""
    pass


def test_config_override(run_rule):
    """Vérifie allowed_elements parameter."""
    md = "Text with <br> and <span>tags</span>\n"

    violations_none = run_rule("MD033", md, {})
    assert len(violations_none) >= 2

    violations_br = run_rule("MD033", md, {"allowed_elements": ["br"]})
    assert len(violations_br) == 1
    assert "span" in violations_br[0].message
