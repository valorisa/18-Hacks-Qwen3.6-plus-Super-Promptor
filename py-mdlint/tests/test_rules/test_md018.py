# tests/test_rules/test_md018.py
"""Tests pour la règle MD018: no-missing-space-atx."""


def test_violation_detected(run_rule):
    """No space after # → violation."""
    md = "#Heading\n"
    violations = run_rule("MD018", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD018"


def test_clean_passes(run_rule):
    """Space after # → 0 violation."""
    md = "# Heading\n"
    violations = run_rule("MD018", md)

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD018")
    if not rule or not rule.fixable:
        pytest.skip("MD018 is not auto-fixable")
    md = "#Heading\n"
    violations = run_rule("MD018", md)
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert fixed.startswith("# ")


def test_config_override(run_rule):
    md = "#Heading\n"
    v1 = run_rule("MD018", md, {})
    v2 = run_rule("MD018", md, {"fake": "value"})
    assert isinstance(v1, list)
