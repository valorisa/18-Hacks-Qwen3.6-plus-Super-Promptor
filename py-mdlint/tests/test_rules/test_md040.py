# tests/test_rules/test_md040.py
"""Tests pour la règle MD040: fenced-code-language."""

import pytest


def test_violation_detected(run_rule):
    """Fenced code block without language → violation."""
    md = "```\ncode here\n```\n"
    violations = run_rule("MD040", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD040"


def test_clean_passes(run_rule):
    """Fenced code block with language → 0 violation."""
    md = "```python\ncode here\n```\n"
    violations = run_rule("MD040", md)

    assert len(violations) == 0


@pytest.mark.skip(reason="MD040 is not auto-fixable")
def test_fix_if_applicable(run_rule):
    pass


def test_config_override(run_rule):
    md = "```javascript\ncode\n```\n"
    v1 = run_rule("MD040", md, {})
    v2 = run_rule("MD040", md, {"allowed_languages": ["python", "bash"]})
    assert len(v2) >= 1
    assert isinstance(v1, list)
