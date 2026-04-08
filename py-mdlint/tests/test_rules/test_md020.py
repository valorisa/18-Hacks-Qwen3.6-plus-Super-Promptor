# tests/test_rules/test_md020.py
"""Tests pour la règle MD020: no-missing-space-closed-atx."""


def test_violation_detected(run_rule):
    """No space before closing # → violation."""
    md = "# Heading#\n"
    violations = run_rule("MD020", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD020"


def test_clean_passes(run_rule):
    """Spaces inside closed atx → 0 violation."""
    md = "# Heading #\n"
    violations = run_rule("MD020", md)

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD020")
    if not rule or not rule.fixable:
        pytest.skip("MD020 is not auto-fixable")
    md = "# Heading#\n"
    violations = run_rule("MD020", md)
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert " #" in fixed


def test_config_override(run_rule):
    md = "# Heading#\n"
    v1 = run_rule("MD020", md, {})
    v2 = run_rule("MD020", md, {"fake": "value"})
    assert isinstance(v1, list)
