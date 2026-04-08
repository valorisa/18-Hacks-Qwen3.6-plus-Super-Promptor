# tests/test_rules/test_md049.py
"""Tests pour la règle MD049: emphasis-style."""


def test_violation_detected(run_rule):
    """Underscore emphasis when asterisk expected → violation."""
    md = "This is _emphasized_ text\n"
    violations = run_rule("MD049", md, {"style": "asterisk"})

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD049"


def test_clean_passes(run_rule):
    """Asterisk emphasis → 0 violation."""
    md = "This is *emphasized* text\n"
    violations = run_rule("MD049", md, {"style": "asterisk"})

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD049")
    if not rule or not rule.fixable:
        pytest.skip("MD049 is not auto-fixable")
    md = "This is _emphasized_ text\n"
    violations = run_rule("MD049", md, {"style": "asterisk"})
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert "*" in fixed


def test_config_override(run_rule):
    md = "_emphasized_\n"
    v1 = run_rule("MD049", md, {"style": "asterisk"})
    v2 = run_rule("MD049", md, {"style": "underscore"})
    assert len(v1) >= 1
    assert len(v2) == 0
