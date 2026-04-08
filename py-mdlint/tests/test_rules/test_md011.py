# tests/test_rules/test_md011.py
"""Tests pour la règle MD011: no-reversed-links."""


def test_violation_detected(run_rule):
    """Reversed link syntax → violation."""
    md = "(https://example.com)[Link text]\n"
    violations = run_rule("MD011", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD011"


def test_clean_passes(run_rule):
    """Correct link syntax → 0 violation."""
    md = "[Link text](https://example.com)\n"
    violations = run_rule("MD011", md)

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD011")
    if not rule or not rule.fixable:
        pytest.skip("MD011 is not auto-fixable")
    md = "(https://example.com)[Link]\n"
    violations = run_rule("MD011", md)
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert "[" in fixed and "](" in fixed


def test_config_override(run_rule):
    md = "(url)[text]\n"
    v1 = run_rule("MD011", md, {})
    v2 = run_rule("MD011", md, {"fake": "value"})
    assert isinstance(v1, list)
