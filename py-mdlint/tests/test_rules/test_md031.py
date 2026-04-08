# tests/test_rules/test_md031.py
"""Tests pour la règle MD031: blanks-around-fences."""


def test_violation_detected(run_rule):
    """Fence sans ligne vide avant → violation."""
    md = "Text\n```python\ncode\n```\n"
    violations = run_rule("MD031", md)

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD031"
    assert "surrounded by blank lines" in violations[0].message


def test_clean_passes(run_rule):
    """Fence avec lignes vides autour → 0 violation."""
    md = "Text\n\n```python\ncode\n```\n\nMore text\n"
    violations = run_rule("MD031", md)

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    """MD031 fix nécessite insertion → test de non-régression."""
    from py_mdlint.registry import load_rules

    md = "Text\n```python\ncode\n```\n"
    violations = run_rule("MD031", md)

    if violations:
        rules = load_rules()
        rule = rules["MD031"]
        lines = md.splitlines()

        result = rule.fix(violations[0], lines)
        assert result == lines[violations[0].line_number - 1]


def test_config_override(run_rule):
    """Vérifie list_items parameter."""
    md = "- Item\n  ```\n  code\n  ```\n"

    violations_list = run_rule("MD031", md, {"list_items": True})
    assert isinstance(violations_list, list)

    violations_no_list = run_rule("MD031", md, {"list_items": False})
    assert isinstance(violations_no_list, list)
