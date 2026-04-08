# src/py_mdlint/utils/text.py
"""Utilities pour les opérations de texte et auto-fixes."""

import re
from typing import Optional


def rstrip_line(line: str) -> str:
    """Supprime les espaces/trailing whitespace d'une ligne."""
    return line.rstrip()


def normalize_spaces_in_line(line: str, target: int = 1) -> str:
    """Normalise les espaces multiples en un seul (ou target)."""
    return re.sub(r' +', ' ' * target, line)


def ensure_trailing_newline(content: str) -> str:
    """Garantit que le contenu se termine par exactement un \\n."""
    return content.rstrip('\n') + '\n'


def collapse_blank_lines(lines: list[str], max_consecutive: int = 1) -> list[str]:
    """Réduit les lignes vides consécutives à max_consecutive."""
    result = []
    blank_count = 0
    
    for line in lines:
        if line.strip() == "":
            blank_count += 1
            if blank_count <= max_consecutive:
                result.append(line)
        else:
            blank_count = 0
            result.append(line)
    
    return result


def normalize_heading_spacing(line: str, style: str = "atx") -> Optional[str]:
    """
    Normalise l'espacement dans les headings ATX.
    
    Args:
        line: Ligne de heading (ex: "#Title" ou "#  Title")
        style: "atx" ou "atx_closed"
    
    Returns:
        Ligne normalisée ou None si pas un heading ATX valide
    """
    if not line.startswith("#"):
        return None
    
    # Pattern: #+ suivi d'espaces optionnels puis contenu
    match = re.match(r'^(#+)(\s*)(.*?)(\s*)(#*)\s*$', line)
    if not match:
        return None
    
    hashes_open, space_before, content, space_after, hashes_close = match.groups()
    
    # Toujours un espace après les # ouvrants (sauf si vide)
    if content:
        space_before = " "
    
    # Pour les headings fermés, un espace avant les # fermants
    if hashes_close:
        space_after = " " if content else ""
        return f"{hashes_open}{space_before}{content}{space_after}{hashes_close}"
    
    return f"{hashes_open}{space_before}{content}"
