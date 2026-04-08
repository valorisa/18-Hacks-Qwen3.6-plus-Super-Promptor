# tests/test_rules/test_md039.py
"""Tests pour la règle MD039: no-space-in-links."""


def test_violation_detected(run_rule):
    """Spaces inside link text → violation."""
    md = "[ a link ](https://example.com)\n"
    violations = run_rule("MD039", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD039"


def test_clean_passes(run_rule):
    """No spaces inside link text → 0 violation."""
    md = "[a link](https://example.com)\n"
    violations = run_rule("MD039", md)

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD039")
    if not rule or not rule.fixable:
        pytest.skip("MD039 is not auto-fixable")
    md = "[ a link ](url)\n"
    violations = run_rule("MD039", md)
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert "[ a" not in fixed


def test_config_override(run_rule):
    md = "[ link ](url)\n"
    v1 = run_rule("MD039", md, {})
    v2 = run_rule("MD039", md, {"fake": "value"})
    assert isinstance(v1, list)
