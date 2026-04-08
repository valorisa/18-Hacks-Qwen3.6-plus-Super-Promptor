# tests/test_rules/test_md001.py
"""Tests pour la règle MD001: heading-increment."""


def test_violation_detected(run_rule):
    """Saut h1→h3 → violation MD001."""
    md = "# Title\n\n### Subtitle"
    violations = run_rule("MD001", md)
    
    assert len(violations) == 1
    assert violations[0].rule_id == "MD001"
    assert violations[0].line_number == 3
    assert "Expected: h2; Actual: h3" in violations[0].message
    assert violations[0].fixable is False


def test_clean_passes(run_rule):
    """Hiérarchie correcte → 0 violation."""
    md = "# Title\n\n## Subtitle\n\n### Section"
    violations = run_rule("MD001", md)
    
    assert len(violations) == 0


def test_multiple_violations(run_rule):
    """Plusieurs sauts de niveau → multiples violations."""
    md = "# H1\n\n#### H4\n\n##### H5\n\n# New H1"
    violations = run_rule("MD001", md)
    
    # H1→H4 (saut de 3) et H1→H5 après reset ne compte pas car nouveau H1
    assert len(violations) >= 1
    assert any("Expected: h2; Actual: h4" in v.message for v in violations)


def test_config_override(run_rule):
    """MD001 n'a pas de paramètres configurables → test de non-régression."""
    md = "# Title\n\n### Subtitle"
    violations_default = run_rule("MD001", md, {})
    violations_custom = run_rule("MD001", md, {"fake_param": "value"})
    
    # Même résultat car pas de params
    assert len(violations_default) == len(violations_custom)


def test_fix_not_applicable(run_rule):
    """MD001 n'est pas auto-fixable → fix() lève NotImplementedError."""
    from py_mdlint.registry import load_rules
    from py_mdlint.rules.base import Violation
    
    rules = load_rules()
    rule = rules["MD001"]
    
    violation = Violation(
        rule_id="MD001",
        line_number=3,
        message="Test",
        fixable=False
    )
    
    try:
        rule.fix(violation, ["# H1", "", "### H3"])
        assert False, "Expected NotImplementedError"
    except NotImplementedError:
        pass  # Comportement attendu
