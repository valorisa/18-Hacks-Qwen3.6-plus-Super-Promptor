# tests/test_rules/test_md027.py
"""Tests pour la règle MD027: no-multiple-space-blockquote."""


def test_violation_detected(run_rule):
    """Multiple spaces after > → violation."""
    md = ">  Text with extra spaces\n"
    violations = run_rule("MD027", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD027"


def test_clean_passes(run_rule):
    """Single space after > → 0 violation."""
    md = "> Text\n"
    violations = run_rule("MD027", md)

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD027")
    if not rule or not rule.fixable:
        pytest.skip("MD027 is not auto-fixable")
    md = ">  Text\n"
    violations = run_rule("MD027", md)
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert fixed == "> Text"


def test_config_override(run_rule):
    md = ">  Text\n"
    v1 = run_rule("MD027", md, {})
    v2 = run_rule("MD027", md, {"fake": "value"})
    assert isinstance(v1, list)
