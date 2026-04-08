# tests/test_rules/test_md030.py
"""Tests pour la règle MD030: list-marker-space."""


def test_violation_detected(run_rule):
    """Wrong number of spaces after list marker → violation."""
    md = "-  Item (2 spaces)\n"
    violations = run_rule("MD030", md, {"ul_single": 1})

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD030"


def test_clean_passes(run_rule):
    """Correct spacing after marker → 0 violation."""
    md = "- Item (1 space)\n"
    violations = run_rule("MD030", md, {"ul_single": 1})

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD030")
    if not rule or not rule.fixable:
        pytest.skip("MD030 is not auto-fixable")
    md = "-  Item\n"
    violations = run_rule("MD030", md, {"ul_single": 1})
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert fixed == "- Item"


def test_config_override(run_rule):
    md = "-  Item\n"
    v1 = run_rule("MD030", md, {"ul_single": 1})
    v2 = run_rule("MD030", md, {"ul_single": 2})
    assert len(v1) >= 1
    assert len(v2) == 0
