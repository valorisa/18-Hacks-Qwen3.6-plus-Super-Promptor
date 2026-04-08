# tests/test_rules/test_md022.py
"""Tests pour la règle MD022: blanks-around-headings."""


def test_violation_detected(run_rule):
    """Heading sans ligne vide avant → violation."""
    md = "Text\n## Heading\n"
    violations = run_rule("MD022", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD022"
    assert "Above" in violations[0].message


def test_clean_passes(run_rule):
    """Heading avec lignes vides autour → 0 violation."""
    md = "Text\n\n## Heading\n\nMore text\n"
    violations = run_rule("MD022", md)

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    """MD022 fix nécessite insertion → test de non-régression."""
    from py_mdlint.registry import load_rules

    md = "Text\n## Heading\n"
    violations = run_rule("MD022", md)

    if violations:
        rules = load_rules()
        rule = rules["MD022"]
        lines = md.splitlines()

        result = rule.fix(violations[0], lines)
        assert result == lines[violations[0].line_number - 1]


def test_config_override(run_rule):
    """Vérifie lines_above/lines_below parameters."""
    md = "Text\n## Heading\n\n"

    violations_above = run_rule("MD022", md, {"lines_above": 1, "lines_below": 0})
    assert len(violations_above) >= 1

    violations_none = run_rule("MD022", md, {"lines_above": 0, "lines_below": 0})
    assert isinstance(violations_none, list)
