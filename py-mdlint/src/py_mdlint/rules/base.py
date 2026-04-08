# src/py_mdlint/rules/base.py
"""Classes de base pour les règles de linting."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Literal, Optional


@dataclass(slots=True)
class Token:
    """Token normalisé pour consommation par les règles."""
    type: str
    tag: str
    content: str
    line_number: int
    column: int
    level: int
    attrs: dict[str, str] = field(default_factory=dict)
    children: list['Token'] = field(default_factory=list)
    meta: dict = field(default_factory=dict)


@dataclass(slots=True)
class Patch:
    """Opération atomique pour correction de fichier."""
    type: Literal["insert", "delete", "replace"]
    line_number: int
    content: Optional[str] = None
    old_content: Optional[str] = None


@dataclass(slots=True)
class Violation:
    """Représente une violation de règle détectée."""
    rule_id: str
    line_number: int
    column: Optional[int] = None
    message: str = ""
    fixable: bool = False
    fixed_line: Optional[str] = None
    suggestion: Optional[str] = None
    patch: Optional[Patch] = None

    def to_dict(self) -> dict:
        """Sérialisation pour rapport JSON/GitHub."""
        return {
            "rule_id": self.rule_id,
            "line": self.line_number,
            "column": self.column,
            "message": self.message,
            "fixable": self.fixable,
            "suggestion": self.suggestion,
        }


class Rule(ABC):
    """Classe de base abstraite pour toutes les règles."""

    rule_id: str = ""
    alias: str = ""
    description: str = ""
    fixable: bool = False

    def __init__(self) -> None:
        self.params: dict = {}
    
    @abstractmethod
    def check(
        self, 
        tokens: list[Token], 
        lines: list[str], 
        config: dict
    ) -> list[Violation]:
        """
        Exécute la règle sur le contenu parse.
        
        Args:
            tokens: Liste de tokens normalisés
            lines: Lignes originales du fichier (pour contexte/fix)
            config: Configuration chargée (avec paramètres de la règle)
        
        Returns:
            Liste des violations détectées
        """
        ...
    
    def fix(self, violation: Violation, lines: list[str]) -> str:
        """
        Applique la correction auto-fixable.

        Args:
            violation: La violation à corriger
            lines: Liste mutable des lignes du fichier

        Returns:
            La ligne corrigée

        Raises:
            NotImplementedError: Si la règle n'est pas auto-fixable
        """
        if not self.fixable:
            raise NotImplementedError(
                f"Rule {self.rule_id} ({self.alias}) is not auto-fixable"
            )
        if violation.patch and violation.patch.content is not None:
            return violation.patch.content
        if violation.fixed_line is not None:
            return violation.fixed_line
        return lines[violation.line_number - 1]
    
    def get_param(self, key: str, default: Any = None) -> Any:
        """Accès sécurisé aux paramètres de configuration."""
        return self.params.get(key, default)
