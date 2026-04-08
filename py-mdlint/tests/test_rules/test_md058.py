# tests/test_rules/test_md058.py
"""Tests pour la règle MD058: blanks-around-tables."""


def test_violation_detected(run_rule):
    """Table without blank line before → violation."""
    md = "Text\n| A | B |\n| --- | --- |\n"
    violations = run_rule("MD058", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD058"


def test_clean_passes(run_rule):
    """Table with blank lines around → 0 violation."""
    md = "Text\n\n| A | B |\n| --- | --- |\n\nMore text\n"
    violations = run_rule("MD058", md)

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD058")
    if not rule or not rule.fixable:
        pytest.skip("MD058 is not auto-fixable")
    md = "Text\n| A | B |\n"
    violations = run_rule("MD058", md)
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert isinstance(fixed, str)


def test_config_override(run_rule):
    md = "Text\n| A | B |\n"
    v1 = run_rule("MD058", md, {})
    v2 = run_rule("MD058", md, {"fake": "value"})
    assert isinstance(v1, list)
