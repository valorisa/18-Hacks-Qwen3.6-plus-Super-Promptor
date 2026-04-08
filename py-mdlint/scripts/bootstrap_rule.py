#!/usr/bin/env python3
"""scripts/bootstrap_rule.py — Génère le squelette d'une nouvelle règle + test."""

import sys
from pathlib import Path

RULES_DIR = Path(__file__).parent.parent / "src" / "py_mdlint" / "rules"
TESTS_DIR = Path(__file__).parent.parent / "tests" / "test_rules"

TEMPLATE_RULE = '''\
# src/py_mdlint/rules/{rule_id_lower}.py
"""{rule_id}: {alias} — {description}."""

from .base import Rule, Violation, Token


class Rule{rule_id}(Rule):
    """
    {rule_id}: {alias}
    
    {description}
    """
    
    rule_id = "{rule_id}"
    alias = "{alias}"
    description = "{description}"
    fixable = {fixable}
    
    def check(
        self, 
        tokens: list[Token], 
        lines: list[str], 
        config: dict
    ) -> list[Violation]:
        violations = []
        
        # TODO: Implémenter la logique de détection
        # Parcourir tokens et/ou lines pour trouver les violations
        
        return violations
    
    def fix(self, violation: Violation, lines: list[str]) -> str:
        if not self.fixable:
            raise NotImplementedError(f"Rule {self.rule_id} is not auto-fixable")
        
        # TODO: Implémenter la correction
        line_idx = violation.line_number - 1
        return lines[line_idx]
'''

TEMPLATE_TEST = '''\
# tests/test_rules/test_{rule_id_lower}.py
"""Tests pour la règle {rule_id}: {alias}."""


def test_violation_detected(run_rule):
    """TODO: Markdown qui viole la règle → au moins 1 violation."""
    md = "# TODO: Exemple de Markdown qui viole {rule_id}"
    violations = run_rule("{rule_id}", md)
    
    assert len(violations) >= 1
    assert violations[0].rule_id == "{rule_id}"


def test_clean_passes(run_rule):
    """TODO: Markdown valide → 0 violation."""
    md = "# TODO: Exemple de Markdown valide pour {rule_id}"
    violations = run_rule("{rule_id}", md)
    
    assert len(violations) == 0


def test_fix_if_applicable(run_rule):
    """TODO: Si fixable, vérifie que fix() corrige."""
    from py_mdlint.registry import load_rules
    from py_mdlint.rules.base import Violation
    
    rules = load_rules()
    rule = rules["{rule_id}"]
    
    if not rule.fixable:
        violation = Violation(rule_id="{rule_id}", line_number=1, message="Test", fixable=False)
        try:
            rule.fix(violation, ["test"])
            assert False, "Expected NotImplementedError"
        except NotImplementedError:
            pass  # Comportement attendu
    else:
        # TODO: Tester la correction automatique
        pass


def test_config_override(run_rule):
    """TODO: Vérifie que les paramètres de config modifient le comportement."""
    md = "# TODO: Markdown de test"
    violations_default = run_rule("{rule_id}", md, {})
    violations_custom = run_rule("{rule_id}", md, {{"fake_param": "value"}})
    
    # TODO: Ajuster selon si la règle a des paramètres
    assert len(violations_default) == len(violations_custom)
'''


def bootstrap_rule(rule_id: str, alias: str, description: str, fixable: bool = False):
    """Génère les fichiers de règle et test."""
    rule_id_lower = rule_id.lower()
    
    # Rule file
    rule_path = RULES_DIR / f"{rule_id_lower}.py"
    if rule_path.exists():
        print(f"⚠️  {rule_path} existe déjà, skip.")
    else:
        rule_path.write_text(
            TEMPLATE_RULE.format(
                rule_id=rule_id,
                rule_id_lower=rule_id_lower,
                alias=alias,
                description=description,
                fixable=str(fixable),
            ),
            encoding="utf-8",
        )
        print(f"✅ Créé: {rule_path}")
    
    # Test file
    test_path = TESTS_DIR / f"test_{rule_id_lower}.py"
    if test_path.exists():
        print(f"⚠️  {test_path} existe déjà, skip.")
    else:
        test_path.write_text(
            TEMPLATE_TEST.format(
                rule_id=rule_id,
                rule_id_lower=rule_id_lower,
                alias=alias,
                description=description,
            ),
            encoding="utf-8",
        )
        print(f"✅ Créé: {test_path}")


def main():
    """CLI: python bootstrap_rule.py MD003 heading-style "Heading style" [fixable]"""
    if len(sys.argv) < 4:
        print("Usage: python bootstrap_rule.py <RULE_ID> <alias> <description> [fixable]")
        print("Exemple: python bootstrap_rule.py MD009 no-trailing-spaces 'Trailing spaces' true")
        sys.exit(1)
    
    rule_id = sys.argv[1]
    alias = sys.argv[2]
    description = sys.argv[3]
    fixable = sys.argv[4].lower() == "true" if len(sys.argv) > 4 else False
    
    bootstrap_rule(rule_id, alias, description, fixable)


if __name__ == "__main__":
    main()
