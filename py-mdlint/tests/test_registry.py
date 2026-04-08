# tests/test_registry.py
"""Tests pour l'auto-discovery des règles."""

from py_mdlint.registry import load_rules
from py_mdlint.rules.base import Rule


def test_load_rules_returns_dict():
    """load_rules retourne un dict non vide."""
    rules = load_rules()
    
    assert isinstance(rules, dict)
    assert "MD001" in rules  # Notre règle exemple


def test_loaded_rules_are_rule_instances():
    """Toutes les règles chargées sont des instances de Rule."""
    rules = load_rules()
    
    for rule_id, rule in rules.items():
        assert isinstance(rule, Rule)
        assert rule.rule_id == rule_id


def test_md001_properties():
    """Vérifie les métadonnées de MD001."""
    rules = load_rules()
    rule = rules["MD001"]
    
    assert rule.alias == "heading-increment"
    assert "increment" in rule.description.lower()
    assert rule.fixable is False
