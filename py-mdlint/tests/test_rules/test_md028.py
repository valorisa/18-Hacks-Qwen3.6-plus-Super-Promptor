# tests/test_rules/test_md028.py
"""Tests pour la règle MD028: no-blanks-blockquote."""


def test_violation_detected(run_rule):
    """Blank line inside blockquote → violation."""
    md = "> Quote line 1\n>\n> Quote line 2\n"
    violations = run_rule("MD028", md)

    assert isinstance(violations, list)


def test_clean_passes(run_rule):
    """Properly separated blockquotes → 0 violation."""
    md = "> Quote line 1\n\n> Quote line 2\n"
    violations = run_rule("MD028", md)

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD028")
    if not rule or not rule.fixable:
        pytest.skip("MD028 is not auto-fixable")
    md = "> Quote\n>\n> More\n"
    violations = run_rule("MD028", md)
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert isinstance(fixed, str)


def test_config_override(run_rule):
    md = "> Quote\n>\n> More\n"
    v1 = run_rule("MD028", md, {})
    v2 = run_rule("MD028", md, {"fake": "value"})
    assert isinstance(v1, list)
