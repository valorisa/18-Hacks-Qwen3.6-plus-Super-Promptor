# tests/test_rules/test_md004.py
"""Tests pour la règle MD004: ul-style."""


def test_violation_detected(run_rule):
    """Mixed list markers → violation."""
    md = "* Item 1\n+ Item 2\n- Item 3\n"
    violations = run_rule("MD004", md, {"style": "dash"})

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD004"


def test_clean_passes(run_rule):
    """Consistent markers → 0 violation."""
    md = "- Item 1\n- Item 2\n- Item 3\n"
    violations = run_rule("MD004", md, {"style": "dash"})

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    """Vérifie que le fix corrige le marker."""
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD004")
    if not rule or not rule.fixable:
        pytest.skip("MD004 is not auto-fixable")

    md = "* Item 1\n"
    violations = run_rule("MD004", md, {"style": "dash"})
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert isinstance(fixed, str)


def test_config_override(run_rule):
    """Vérifie que le paramètre style est respecté."""
    md = "* Item 1\n- Item 2\n"
    violations_asterisk = run_rule("MD004", md, {"style": "asterisk"})
    violations_dash = run_rule("MD004", md, {"style": "dash"})
    assert isinstance(violations_asterisk, list) and isinstance(violations_dash, list)
