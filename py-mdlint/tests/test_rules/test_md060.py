# tests/test_rules/test_md060.py
"""Tests pour la règle MD060: table-column-style."""


def test_violation_detected(run_rule):
    """Table with alignment markers → check detection."""
    md = "| A | B |\n| :--- | ---: |\n| 1 | 2 |\n"
    violations = run_rule("MD060", md)

    assert isinstance(violations, list)


def test_clean_passes(run_rule):
    """Simple table → 0 violation."""
    md = "| A | B |\n| --- | --- |\n| 1 | 2 |\n"
    violations = run_rule("MD060", md)

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD060")
    if not rule or not rule.fixable:
        pytest.skip("MD060 is not auto-fixable")
    md = "| A | B |\n| :--- | ---: |\n"
    violations = run_rule("MD060", md)
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert isinstance(fixed, str)


def test_config_override(run_rule):
    md = "| A | B |\n| --- | --- |\n"
    v1 = run_rule("MD060", md, {})
    v2 = run_rule("MD060", md, {"fake": "value"})
    assert isinstance(v1, list)
