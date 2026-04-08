# tests/test_rules/test_md010.py
"""Tests pour la règle MD010: no-hard-tabs."""


def test_violation_detected(run_rule):
    """Tab character → violation."""
    md = "Text\twith tab\n"
    violations = run_rule("MD010", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD010"


def test_clean_passes(run_rule):
    """No tabs → 0 violation."""
    md = "Text with spaces only\n"
    violations = run_rule("MD010", md)

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD010")
    if not rule or not rule.fixable:
        pytest.skip("MD010 is not auto-fixable")
    md = "Text\there\n"
    violations = run_rule("MD010", md)
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert "\t" not in fixed


def test_config_override(run_rule):
    md = "Text\there\n"
    v1 = run_rule("MD010", md, {"spaces_per_tab": 1})
    v2 = run_rule("MD010", md, {"spaces_per_tab": 4})
    assert len(v1) == len(v2)
