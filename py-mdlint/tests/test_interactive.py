# tests/test_interactive.py
"""Tests pour le menu interactif (input mocké)."""

import pytest
from unittest.mock import patch, MagicMock
from py_mdlint.interactive import InteractiveMenu


def test_get_choice_valid_input():
    """get_choice retourne la valeur valide."""
    menu = InteractiveMenu()
    
    with patch("builtins.input", return_value="2"):
        result = menu.get_choice("Choix: ", ["1", "2", "3"])
    
    assert result == "2"


def test_get_choice_default():
    """get_choice retourne la valeur par défaut si entrée vide."""
    menu = InteractiveMenu()
    
    with patch("builtins.input", return_value=""):
        result = menu.get_choice("Choix: ", ["1", "2"], default="1")
    
    assert result == "1"


def test_get_choice_retry_on_invalid():
    """get_choice re-demande sur input invalide."""
    menu = InteractiveMenu()
    
    with patch("builtins.input", side_effect=["invalid", "2", ""]):
        with patch("builtins.print"):  # Supprimer output warning
            result = menu.get_choice("Choix: ", ["1", "2", "3"])
    
    assert result == "2"


def test_screen_lint_defaults():
    """screen_lint retourne les valeurs par défaut."""
    menu = InteractiveMenu()
    
    with patch("builtins.input", side_effect=["", "", "", ""]):
        result = menu.screen_lint()
    
    assert result["path"] == "."
    assert result["config"] == ".markdownlint.json"
    assert result["report"] == "console"
    assert result["ignore"] == []
