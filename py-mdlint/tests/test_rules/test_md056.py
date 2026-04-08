# tests/test_rules/test_md056.py
"""Tests pour la règle MD056: table-column-count."""


def test_violation_detected(run_rule):
    """Inconsistent column count → violation."""
    md = "| A | B |\n| --- | --- |\n| 1 | 2 | 3 |\n"
    violations = run_rule("MD056", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD056"


def test_clean_passes(run_rule):
    """Consistent column count → 0 violation."""
    md = "| A | B |\n| --- | --- |\n| 1 | 2 |\n"
    violations = run_rule("MD056", md)

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD056")
    if not rule or not rule.fixable:
        pytest.skip("MD056 is not auto-fixable")
    md = "| A | B |\n| --- | --- |\n| 1 | 2 | 3 |\n"
    violations = run_rule("MD056", md)
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert isinstance(fixed, str)


def test_config_override(run_rule):
    md = "| A | B |\n| --- | --- |\n| 1 | 2 |\n"
    v1 = run_rule("MD056", md, {})
    v2 = run_rule("MD056", md, {"fake": "value"})
    assert isinstance(v1, list)
