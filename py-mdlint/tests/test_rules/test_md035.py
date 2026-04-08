# tests/test_rules/test_md035.py
"""Tests pour la règle MD035: hr-style."""


def test_violation_detected(run_rule):
    """Inconsistent HR styles → violation."""
    md = "---\n\n***\n"
    violations = run_rule("MD035", md, {"style": "---"})

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD035"


def test_clean_passes(run_rule):
    """Consistent HR style → 0 violation."""
    md = "---\n\n---\n"
    violations = run_rule("MD035", md, {"style": "---"})

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD035")
    if not rule or not rule.fixable:
        pytest.skip("MD035 is not auto-fixable")
    md = "***\n"
    violations = run_rule("MD035", md, {"style": "---"})
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert fixed == "---"


def test_config_override(run_rule):
    md = "---\n\n***\n"
    v1 = run_rule("MD035", md, {"style": "---"})
    v2 = run_rule("MD035", md, {"style": "***"})
    assert len(v1) >= 1
    assert len(v2) >= 1
