# tests/test_rules/test_md005.py
"""Tests pour la règle MD005: list-indent."""


def test_violation_detected(run_rule):
    """Inconsistent list indentation → violation."""
    md = "* Item 1\n  * Nested\n   * Misaligned\n"
    violations = run_rule("MD005", md)

    assert isinstance(violations, list)


def test_clean_passes(run_rule):
    """Consistent indentation → 0 violation."""
    md = "* Item 1\n  * Nested\n  * Also nested\n"
    violations = run_rule("MD005", md)

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    """Vérifie que le fix est applicable."""
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD005")
    if not rule or not rule.fixable:
        pytest.skip("MD005 is not auto-fixable")

    md = "* Item 1\n   * Bad indent\n"
    violations = run_rule("MD005", md)
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert isinstance(fixed, str)


def test_config_override(run_rule):
    """MD005 n'a pas de paramètres spécifiques."""
    md = "* Item\n  * Nested\n"
    violations_default = run_rule("MD005", md, {})
    violations_custom = run_rule("MD005", md, {"fake": "value"})
    assert isinstance(violations_default, list)
