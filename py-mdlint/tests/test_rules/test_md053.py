# tests/test_rules/test_md053.py
"""Tests pour la règle MD053: link-image-reference-definitions."""


def test_violation_detected(run_rule):
    """Unused reference definition → violation."""
    md = "[unused-ref]: https://example.com\n"
    violations = run_rule("MD053", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD053"


def test_clean_passes(run_rule):
    """Used reference definition → 0 violation."""
    md = "Some [used-ref] here\n\n[used-ref]: https://example.com\n"
    violations = run_rule("MD053", md)

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD053")
    if not rule or not rule.fixable:
        pytest.skip("MD053 is not auto-fixable")
    md = "[unused]: https://example.com\n"
    violations = run_rule("MD053", md)
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert isinstance(fixed, str)


def test_config_override(run_rule):
    md = "[ref]: https://example.com\n"
    v1 = run_rule("MD053", md, {})
    v2 = run_rule("MD053", md, {"fake": "value"})
    assert isinstance(v1, list)
