# tests/test_rules/test_md026.py
"""Tests pour la règle MD026: no-trailing-punctuation."""


def test_violation_detected(run_rule):
    """Heading with trailing punctuation → violation."""
    md = "# This is a heading.\n"
    violations = run_rule("MD026", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD026"


def test_clean_passes(run_rule):
    """Heading without trailing punctuation → 0 violation."""
    md = "# This is a heading\n"
    violations = run_rule("MD026", md)

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD026")
    if not rule or not rule.fixable:
        pytest.skip("MD026 is not auto-fixable")
    md = "# Heading.\n"
    violations = run_rule("MD026", md)
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert not fixed.endswith(".")


def test_config_override(run_rule):
    md = "# Heading!\n"
    v1 = run_rule("MD026", md, {"punctuation": ".,;:!"})
    v2 = run_rule("MD026", md, {"punctuation": ""})
    assert len(v1) >= 1
    assert len(v2) == 0
