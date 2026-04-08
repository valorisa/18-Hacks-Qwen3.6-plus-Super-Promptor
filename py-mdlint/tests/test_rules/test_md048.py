# tests/test_rules/test_md048.py
"""Tests pour la règle MD048: code-fence-style."""


def test_violation_detected(run_rule):
    """Tilde fence when backtick expected → violation."""
    md = "~~~python\ncode\n~~~\n"
    violations = run_rule("MD048", md, {"style": "backtick"})

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD048"


def test_clean_passes(run_rule):
    """Backtick fence → 0 violation."""
    md = "```python\ncode\n```\n"
    violations = run_rule("MD048", md, {"style": "backtick"})

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD048")
    if not rule or not rule.fixable:
        pytest.skip("MD048 is not auto-fixable")
    md = "~~~\ncode\n~~~\n"
    violations = run_rule("MD048", md, {"style": "backtick"})
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert "```" in fixed


def test_config_override(run_rule):
    md = "```\ncode\n```\n"
    v1 = run_rule("MD048", md, {"style": "backtick"})
    v2 = run_rule("MD048", md, {"style": "tilde"})
    assert len(v2) >= 1
    assert len(v1) == 0
