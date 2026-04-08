# tests/test_rules/test_md012.py
"""Tests pour la règle MD012: no-multiple-blanks."""


def test_violation_detected(run_rule):
    """3 lignes vides consécutives → violation (max=1)."""
    md = "Line 1\n\n\n\nLine 2\n"
    violations = run_rule("MD012", md, {"maximum": 1})

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD012"
    assert "Multiple consecutive blank lines" in violations[0].message


def test_clean_passes(run_rule):
    """1 ligne vide max → 0 violation."""
    md = "Line 1\n\nLine 2\n\nLine 3\n"
    violations = run_rule("MD012", md, {"maximum": 1})

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    """MD012 fix nécessite traitement global → test de non-régression."""
    from py_mdlint.registry import load_rules

    md = "Line 1\n\n\n\nLine 2\n"
    violations = run_rule("MD012", md, {"maximum": 1})

    if violations:
        rules = load_rules()
        rule = rules["MD012"]
        lines = md.splitlines()

        result = rule.fix(violations[0], lines)
        assert result == lines[violations[0].line_number - 1]


def test_config_override(run_rule):
    """Vérifie que maximum est respecté."""
    md = "Line 1\n\n\nLine 2\n"

    violations_1 = run_rule("MD012", md, {"maximum": 1})
    assert len(violations_1) >= 1

    violations_2 = run_rule("MD012", md, {"maximum": 2})
    assert len(violations_2) == 0
