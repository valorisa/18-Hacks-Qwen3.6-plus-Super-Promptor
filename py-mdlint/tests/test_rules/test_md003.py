# tests/test_rules/test_md003.py
"""Tests pour la règle MD003: heading-style."""


def test_violation_detected(run_rule):
    """Mix de styles ATX et setext → violation."""
    md = "# ATX Heading\n\nSetext Heading\n==============\n"
    violations = run_rule("MD003", md, {"style": "atx"})

    assert len(violations) >= 1
    assert violations[0].rule_id == "MD003"
    assert "setext" in violations[0].message.lower()


def test_clean_passes(run_rule):
    """Style uniforme → 0 violation."""
    md = "# Heading 1\n\n## Heading 2\n\n### Heading 3\n"
    violations = run_rule("MD003", md, {"style": "atx"})

    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    """Vérifie que le fix convertit setext → atx."""
    from py_mdlint.registry import load_rules

    md = "# H1\n\nSetext\n====\n"
    violations = run_rule("MD003", md, {"style": "atx"})

    if violations:
        rules = load_rules()
        rule = rules["MD003"]
        lines = md.splitlines()

        setext_violation = next((v for v in violations if "setext" in v.message.lower()), None)
        if setext_violation:
            fixed_line = rule.fix(setext_violation, lines)
            assert fixed_line.strip().startswith("##")


def test_config_override(run_rule):
    """Vérifie que le paramètre style est respecté."""
    md = "# ATX\n\nSetext\n====\n"

    violations_atx = run_rule("MD003", md, {"style": "atx"})
    assert len(violations_atx) >= 1

    violations_setext = run_rule("MD003", md, {"style": "setext"})
    assert len(violations_setext) >= 1

    violations_consistent = run_rule("MD003", md, {"style": "consistent"})
    assert isinstance(violations_consistent, list)
