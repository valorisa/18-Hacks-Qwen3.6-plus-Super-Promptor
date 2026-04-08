# src/py_mdlint/utils/colors.py
"""Palette de couleurs sobres avec support NO_COLOR."""

import os
import sys


class Colors:
    """Couleurs ANSI sobres pour l'interface CLI."""
    
    CYAN = "\033[96m"      # Bordures du menu
    GREEN = "\033[92m"     # Titres, numéros, succès
    WHITE = "\033[97m"     # Texte courant
    YELLOW = "\033[93m"    # Erreurs, avertissements
    RESET = "\033[0m"
    
    @classmethod
    def enabled(cls) -> bool:
        """Vérifie si les couleurs doivent être affichées."""
        return not os.getenv("NO_COLOR") and sys.stdout.isatty()
    
    @classmethod
    def wrap(cls, color: str, text: str) -> str:
        """Enveloppe un texte avec une couleur si activée."""
        if not cls.enabled():
            return text
        return f"{color}{text}{cls.RESET}"
    
    @classmethod
    def border(cls, text: str) -> str:
        return cls.wrap(cls.CYAN, text)
    
    @classmethod
    def title(cls, text: str) -> str:
        return cls.wrap(cls.GREEN, text)
    
    @classmethod
    def text(cls, text: str) -> str:
        return cls.wrap(cls.WHITE, text)
    
    @classmethod
    def warning(cls, text: str) -> str:
        return cls.wrap(cls.YELLOW, text)
    
    @classmethod
    def success(cls, text: str) -> str:
        return cls.wrap(cls.GREEN, text)
