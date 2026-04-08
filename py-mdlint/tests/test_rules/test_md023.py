# tests/test_rules/test_md023.py
"""Tests pour la règle MD023: heading-start-left."""


def test_violation_detected(run_rule):
    """Heading with leading spaces → violation."""
    md = "  # Heading\n"
    violations = run_rule("MD023", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD023"


def test_clean_passes(run_rule):
    """Heading at start of line → 0 violation."""
    md = "# Heading\n"
    violations = run_rule("MD023", md)

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD023")
    if not rule or not rule.fixable:
        pytest.skip("MD023 is not auto-fixable")
    md = "  # Heading\n"
    violations = run_rule("MD023", md)
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert fixed == "# Heading"


def test_config_override(run_rule):
    md = "  # Heading\n"
    v1 = run_rule("MD023", md, {})
    v2 = run_rule("MD023", md, {"fake": "value"})
    assert isinstance(v1, list)
