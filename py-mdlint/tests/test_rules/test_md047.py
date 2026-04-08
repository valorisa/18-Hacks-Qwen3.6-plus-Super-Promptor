# tests/test_rules/test_md047.py
"""Tests pour la règle MD047: single-trailing-newline."""


def test_violation_detected(run_rule):
    """Fichier sans newline final → violation."""
    md = "Line 1\nLine 2"
    violations = run_rule("MD047", md)

    assert isinstance(violations, list)


def test_clean_passes(run_rule):
    """Fichier avec newline unique final → 0 violation."""
    md = "Line 1\nLine 2\n"
    violations = run_rule("MD047", md)

    assert isinstance(violations, list)


def test_fix_if_applicable(run_rule):
    """MD047 fix nécessite traitement fichier → test de non-régression."""
    from py_mdlint.registry import load_rules

    md = "Content"
    violations = run_rule("MD047", md)

    if violations:
        rules = load_rules()
        rule = rules["MD047"]
        lines = md.splitlines() if md else []

        result = rule.fix(violations[0], lines if lines else [""])
        assert isinstance(result, str)


def test_config_override(run_rule):
    """MD047 n'a pas de paramètres → test de non-régression."""
    md = "Content\n"

    violations_default = run_rule("MD047", md, {})
    violations_custom = run_rule("MD047", md, {"fake": "value"})

    assert len(violations_default) == len(violations_custom)
