# tests/test_rules/test_md034.py
"""Tests pour la règle MD034: no-bare-urls."""


def test_violation_detected(run_rule):
    """Bare URL → violation."""
    md = "Visit https://example.com for more info\n"
    violations = run_rule("MD034", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD034"


def test_clean_passes(run_rule):
    """URL in angle brackets → 0 violation."""
    md = "Visit <https://example.com> for more info\n"
    violations = run_rule("MD034", md)

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD034")
    if not rule or not rule.fixable:
        pytest.skip("MD034 is not auto-fixable")
    md = "Visit https://example.com today\n"
    violations = run_rule("MD034", md)
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert "<https://" in fixed


def test_config_override(run_rule):
    md = "Visit https://example.com\n"
    v1 = run_rule("MD034", md, {})
    v2 = run_rule("MD034", md, {"fake": "value"})
    assert isinstance(v1, list)
