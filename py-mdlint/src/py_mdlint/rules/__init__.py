# src/py_mdlint/rules/__init__.py
"""Registry des règles — auto-discovery depuis le dossier rules/."""

from .base import Rule, Violation, Token

__all__ = ["Rule", "Violation", "Token", "load_rules"]


def load_rules() -> dict[str, Rule]:
    """
    Auto-discover toutes les classes Rule dans le dossier rules/.
    
    Returns:
        Dict mapping rule_id → instance de Rule
    """
    import importlib
    from pathlib import Path
    
    rules = {}
    rules_dir = Path(__file__).parent
    
    for rule_file in rules_dir.glob("md*.py"):
        if rule_file.name in ("__init__.py", "base.py"):
            continue
        
        # Import dynamique du module
        module_name = f"py_mdlint.rules.{rule_file.stem}"
        module = importlib.import_module(module_name)
        
        # Extraction de la classe Rule correspondante
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (
                isinstance(attr, type) 
                and issubclass(attr, Rule) 
                and attr != Rule
                and hasattr(attr, 'rule_id')
                and attr.rule_id
            ):
                rule_instance = attr()
                rules[rule_instance.rule_id] = rule_instance
    
    return rules
