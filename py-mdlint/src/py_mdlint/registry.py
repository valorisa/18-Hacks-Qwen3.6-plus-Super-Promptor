# src/py_mdlint/registry.py
"""Registry des règles — point d'entrée pour auto-discovery."""

from .rules import load_rules

__all__ = ["load_rules"]
