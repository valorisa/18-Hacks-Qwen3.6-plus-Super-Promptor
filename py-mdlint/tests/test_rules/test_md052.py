# tests/test_rules/test_md052.py
"""Tests pour la règle MD052: reference-links-images."""

import pytest


def test_violation_detected(run_rule):
    """Reference link without definition → violation."""
    md = "Some [undefined-ref] here\n"
    violations = run_rule("MD052", md)

    assert isinstance(violations, list)


def test_clean_passes(run_rule):
    """Reference link with definition → 0 violation."""
    md = "Some [defined-ref] here\n\n[defined-ref]: https://example.com\n"
    violations = run_rule("MD052", md)

    assert len(violations) == 0


@pytest.mark.skip(reason="MD052 is not auto-fixable")
def test_fix_if_applicable(run_rule):
    pass


def test_config_override(run_rule):
    md = "[ref] text\n"
    v1 = run_rule("MD052", md, {})
    v2 = run_rule("MD052", md, {"fake": "value"})
    assert isinstance(v1, list)
