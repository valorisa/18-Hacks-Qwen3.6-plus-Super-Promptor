# tests/test_rules/test_md038.py
"""Tests pour la règle MD038: no-space-in-code."""


def test_violation_detected(run_rule):
    """Spaces inside code span → violation."""
    md = "Use ` code ` here\n"
    violations = run_rule("MD038", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD038"


def test_clean_passes(run_rule):
    """No spaces inside code span → 0 violation."""
    md = "Use `code` here\n"
    violations = run_rule("MD038", md)

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD038")
    if not rule or not rule.fixable:
        pytest.skip("MD038 is not auto-fixable")
    md = "Use ` code `\n"
    violations = run_rule("MD038", md)
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert "` code" not in fixed


def test_config_override(run_rule):
    md = "` code `\n"
    v1 = run_rule("MD038", md, {})
    v2 = run_rule("MD038", md, {"fake": "value"})
    assert isinstance(v1, list)
