# tests/test_rules/test_md014.py
"""Tests pour la règle MD014: commands-show-output."""


def test_violation_detected(run_rule):
    """Dollar signs before commands without output → violation."""
    md = "```bash\n$ ls\n$ cat file\n```\n"
    violations = run_rule("MD014", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD014"


def test_clean_passes(run_rule):
    """Commands with output → 0 violation."""
    md = "```bash\n$ ls\nfile1.txt file2.txt\n```\n"
    violations = run_rule("MD014", md)

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    from py_mdlint.registry import load_rules
    rules = load_rules()
    rule = rules.get("MD014")
    if not rule or not rule.fixable:
        pytest.skip("MD014 is not auto-fixable")
    md = "```bash\n$ ls\n```\n"
    violations = run_rule("MD014", md)
    if violations:
        lines = md.splitlines()
        fixed = rule.fix(violations[0], lines)
        assert not fixed.strip().startswith("$")


def test_config_override(run_rule):
    md = "```bash\n$ ls\n```\n"
    v1 = run_rule("MD014", md, {})
    v2 = run_rule("MD014", md, {"fake": "value"})
    assert isinstance(v1, list)
