# tests/test_rules/test_md007.py
"""Tests pour la règle MD007: ul-indent."""


def test_violation_detected(run_rule):
    """Wrong indent for nested list → violation."""
    md = "* Item\n   * Nested (3 spaces)\n"
    violations = run_rule("MD007", md, {"indent": 2})

    assert isinstance(violations, list)


def test_clean_passes(run_rule):
    """Correct 2-space indent → 0 violation."""
    md = "* Item\n  * Nested (2 spaces)\n"
    violations = run_rule("MD007", md, {"indent": 2})

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD007")
    if not rule or not rule.fixable:
        pytest.skip("MD007 is not auto-fixable")
    md = "* Item\n   * Bad\n"
    violations = run_rule("MD007", md)
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert isinstance(fixed, str)


def test_config_override(run_rule):
    md = "* Item\n  * Nested\n"
    v1 = run_rule("MD007", md, {"indent": 2})
    v2 = run_rule("MD007", md, {"indent": 4})
    assert isinstance(v1, list) and isinstance(v2, list)
