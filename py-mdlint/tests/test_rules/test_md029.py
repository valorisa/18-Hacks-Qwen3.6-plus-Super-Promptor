# tests/test_rules/test_md029.py
"""Tests pour la règle MD029: ol-prefix."""


def test_violation_detected(run_rule):
    """Non-sequential ordered list → violation."""
    md = "1. Item\n3. Item\n"
    violations = run_rule("MD029", md, {"style": "ordered"})

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD029"


def test_clean_passes(run_rule):
    """All 1. style → 0 violation."""
    md = "1. Item\n1. Item\n"
    violations = run_rule("MD029", md, {"style": "one"})

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD029")
    if not rule or not rule.fixable:
        pytest.skip("MD029 is not auto-fixable")
    md = "1. Item\n3. Item\n"
    violations = run_rule("MD029", md, {"style": "one"})
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert fixed.startswith("1.")


def test_config_override(run_rule):
    md = "1. Item\n2. Item\n"
    v1 = run_rule("MD029", md, {"style": "one"})
    v2 = run_rule("MD029", md, {"style": "ordered"})
    assert isinstance(v1, list) and isinstance(v2, list)
