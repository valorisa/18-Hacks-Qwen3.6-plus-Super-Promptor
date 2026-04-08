# tests/test_rules/test_md019.py
"""Tests pour la règle MD019: no-multiple-space-atx."""


def test_violation_detected(run_rule):
    """Multiple spaces after # → violation."""
    md = "#  Heading\n"
    violations = run_rule("MD019", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD019"


def test_clean_passes(run_rule):
    """Single space after # → 0 violation."""
    md = "# Heading\n"
    violations = run_rule("MD019", md)

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD019")
    if not rule or not rule.fixable:
        pytest.skip("MD019 is not auto-fixable")
    md = "#  Heading\n"
    violations = run_rule("MD019", md)
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert fixed == "# Heading"


def test_config_override(run_rule):
    md = "#  Heading\n"
    v1 = run_rule("MD019", md, {})
    v2 = run_rule("MD019", md, {"fake": "value"})
    assert isinstance(v1, list)
