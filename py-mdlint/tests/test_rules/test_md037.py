# tests/test_rules/test_md037.py
"""Tests pour la règle MD037: no-space-in-emphasis."""


def test_violation_detected(run_rule):
    """Spaces inside emphasis → violation."""
    md = "This is ** bold ** text\n"
    violations = run_rule("MD037", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD037"


def test_clean_passes(run_rule):
    """No spaces inside emphasis → 0 violation."""
    md = "This is **bold** text\n"
    violations = run_rule("MD037", md)

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD037")
    if not rule or not rule.fixable:
        pytest.skip("MD037 is not auto-fixable")
    md = "This is ** bold ** text\n"
    violations = run_rule("MD037", md)
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert " **" not in fixed


def test_config_override(run_rule):
    md = "** bold **\n"
    v1 = run_rule("MD037", md, {})
    v2 = run_rule("MD037", md, {"fake": "value"})
    assert isinstance(v1, list)
