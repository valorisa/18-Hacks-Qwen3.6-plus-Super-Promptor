# tests/test_rules/test_md032.py
"""Tests pour la règle MD032: blanks-around-lists."""


def test_violation_detected(run_rule):
    """Liste sans ligne vide avant → violation."""
    md = "Text\n- Item 1\n- Item 2\n"
    violations = run_rule("MD032", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD032"
    assert "Above" in violations[0].message


def test_clean_passes(run_rule):
    """Liste avec lignes vides autour → 0 violation."""
    md = "Text\n\n- Item 1\n- Item 2\n\nMore text\n"
    violations = run_rule("MD032", md)

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    """MD032 fix nécessite insertion → test de non-régression."""
    from py_mdlint.registry import load_rules

    md = "Text\n- Item 1\n"
    violations = run_rule("MD032", md)

    if violations:
        rules = load_rules()
        rule = rules["MD032"]
        lines = md.splitlines()

        result = rule.fix(violations[0], lines)
        assert result == lines[violations[0].line_number - 1]


def test_config_override(run_rule):
    """MD032 n'a pas de paramètres spécifiques → test de non-régression."""
    md = "Text\n- Item\n"

    violations_default = run_rule("MD032", md, {})
    violations_custom = run_rule("MD032", md, {"fake_param": "value"})

    assert len(violations_default) == len(violations_custom)
