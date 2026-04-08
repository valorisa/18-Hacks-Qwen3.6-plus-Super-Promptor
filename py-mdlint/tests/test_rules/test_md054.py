# tests/test_rules/test_md054.py
"""Tests pour la règle MD054: link-image-style."""

import pytest


def test_violation_detected(run_rule):
    """Autolink when disabled → violation."""
    md = "<https://example.com>\n"
    violations = run_rule("MD054", md, {"autolink": False})

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD054"


def test_clean_passes(run_rule):
    """Autolink enabled → 0 violation."""
    md = "<https://example.com>\n"
    violations = run_rule("MD054", md, {"autolink": True})

    assert len(violations) == 0


@pytest.mark.skip(reason="MD054 is not auto-fixable")
def test_fix_if_applicable(run_rule):
    pass


def test_config_override(run_rule):
    md = "<https://example.com>\n"
    v1 = run_rule("MD054", md, {"autolink": True})
    v2 = run_rule("MD054", md, {"autolink": False})
    assert len(v2) >= 1
    assert len(v1) == 0
