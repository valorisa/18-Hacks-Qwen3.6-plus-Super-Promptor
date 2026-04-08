# tests/test_rules/test_md046.py
"""Tests pour la règle MD046: code-block-style."""


def test_violation_detected(run_rule):
    """Indented code block when fenced expected → violation."""
    md = "    indented code block\n"
    violations = run_rule("MD046", md, {"style": "fenced"})

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD046"


def test_clean_passes(run_rule):
    """Fenced code block → 0 violation."""
    md = "```python\ncode\n```\n"
    violations = run_rule("MD046", md, {"style": "fenced"})

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD046")
    if not rule or not rule.fixable:
        pytest.skip("MD046 is not auto-fixable")
    md = "    code\n"
    violations = run_rule("MD046", md, {"style": "fenced"})
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert isinstance(fixed, str)


def test_config_override(run_rule):
    md = "```python\ncode\n```\n"
    v1 = run_rule("MD046", md, {"style": "fenced"})
    v2 = run_rule("MD046", md, {"style": "indented"})
    assert len(v2) >= 1
    assert len(v1) == 0
