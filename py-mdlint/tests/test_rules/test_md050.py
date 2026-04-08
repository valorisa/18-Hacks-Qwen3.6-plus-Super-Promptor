# tests/test_rules/test_md050.py
"""Tests pour la règle MD050: strong-style."""


def test_violation_detected(run_rule):
    """Underscore strong when asterisk expected → violation."""
    md = "This is __strong__ text\n"
    violations = run_rule("MD050", md, {"style": "asterisk"})

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD050"


def test_clean_passes(run_rule):
    """Asterisk strong → 0 violation."""
    md = "This is **strong** text\n"
    violations = run_rule("MD050", md, {"style": "asterisk"})

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD050")
    if not rule or not rule.fixable:
        pytest.skip("MD050 is not auto-fixable")
    md = "__strong__\n"
    violations = run_rule("MD050", md, {"style": "asterisk"})
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert "**" in fixed


def test_config_override(run_rule):
    md = "__strong__\n"
    v1 = run_rule("MD050", md, {"style": "asterisk"})
    v2 = run_rule("MD050", md, {"style": "underscore"})
    assert len(v1) >= 1
    assert len(v2) == 0
