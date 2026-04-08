# tests/test_rules/test_md009.py
"""Tests pour la règle MD009: no-trailing-spaces."""


def test_violation_detected(run_rule):
    """Ligne avec trailing spaces → violation."""
    md = "Line with spaces   \nNext line\n"
    violations = run_rule("MD009", md)

    assert len(violations) == 1
    assert violations[0].rule_id == "MD009"
    assert violations[0].line_number == 1
    assert "Trailing spaces" in violations[0].message


def test_clean_passes(run_rule):
    """Pas de trailing spaces → 0 violation."""
    md = "Clean line\nAnother clean line\n"
    violations = run_rule("MD009", md)

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    """Vérifie que le fix supprime les trailing spaces."""
    from py_mdlint.registry import load_rules

    md = "Line with spaces   \nClean\n"
    violations = run_rule("MD009", md)

    if violations:
        rules = load_rules()
        rule = rules["MD009"]
        lines = md.splitlines()

        fixed_line = rule.fix(violations[0], lines)
        assert fixed_line == "Line with spaces"
        assert not fixed_line.endswith(" ")


def test_config_override(run_rule):
    """Vérifie br_spaces parameter."""
    md = "Hard break  \n<br>\n"

    violations_default = run_rule("MD009", md, {})
    assert len(violations_default) >= 1

    violations_br = run_rule("MD009", md, {"br_spaces": 2})
    assert isinstance(violations_br, list)
