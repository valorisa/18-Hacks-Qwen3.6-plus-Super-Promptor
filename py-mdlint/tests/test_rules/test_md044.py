# tests/test_rules/test_md044.py
"""Tests pour la règle MD044: proper-names."""


def test_violation_detected(run_rule):
    """Incorrect capitalization of proper name → violation."""
    md = "I love javascript programming\n"
    violations = run_rule("MD044", md, {"names": ["JavaScript"]})

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD044"


def test_clean_passes(run_rule):
    """Correct capitalization → 0 violation."""
    md = "I love JavaScript programming\n"
    violations = run_rule("MD044", md, {"names": ["JavaScript"]})

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD044")
    if not rule or not rule.fixable:
        pytest.skip("MD044 is not auto-fixable")
    md = "I use github daily\n"
    violations = run_rule("MD044", md, {"names": ["GitHub"]})
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert "GitHub" in fixed


def test_config_override(run_rule):
    md = "I use javascript and github\n"
    v1 = run_rule("MD044", md, {"names": ["JavaScript", "GitHub"]})
    v2 = run_rule("MD044", md, {"names": []})
    assert len(v1) >= 1
    assert len(v2) == 0
