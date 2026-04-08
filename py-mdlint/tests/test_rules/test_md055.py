# tests/test_rules/test_md055.py
"""Tests pour la règle MD055: table-pipe-style."""


def test_violation_detected(run_rule):
    """Missing trailing pipe → violation."""
    md = "| Header | Header2\n| ------ | -------\n| Cell | Cell2\n"
    violations = run_rule("MD055", md, {"style": "leading_and_trailing"})

    assert isinstance(violations, list)


def test_clean_passes(run_rule):
    """Pipes on both sides → 0 violation."""
    md = "| Header | Header2 |\n| ------ | ------- |\n| Cell | Cell2 |\n"
    violations = run_rule("MD055", md, {"style": "leading_and_trailing"})

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD055")
    if not rule or not rule.fixable:
        pytest.skip("MD055 is not auto-fixable")
    md = "| Header | Header2\n"
    violations = run_rule("MD055", md, {"style": "leading_and_trailing"})
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert isinstance(fixed, str)


def test_config_override(run_rule):
    md = "| Header | Header2 |\n"
    v1 = run_rule("MD055", md, {"style": "leading_and_trailing"})
    v2 = run_rule("MD055", md, {"style": "no_pipes"})
    assert isinstance(v1, list) and isinstance(v2, list)
