# src/py_mdlint/utils/fs.py
"""Utilities pour la gestion des fichiers et chemins."""

from pathlib import Path
from typing import Iterator, Union


def find_markdown_files(
    path: Union[str, Path], 
    exclude_patterns: list[str] = None
) -> Iterator[Path]:
    """
    Trouve récursivement tous les fichiers .md dans un chemin.
    
    Args:
        path: Chemin de départ (fichier ou dossier)
        exclude_patterns: Patterns glob à exclure (ex: ["node_modules/*"])
    
    Yields:
        Chemins absolus des fichiers Markdown trouvés
    """
    exclude_patterns = exclude_patterns or []
    path = Path(path).resolve()
    
    if path.is_file():
        if path.suffix == ".md":
            yield path
        return
    
    for md_file in path.rglob("*.md"):
        # Vérifie les exclusions
        relative = md_file.relative_to(path)
        if any(relative.match(pattern) for pattern in exclude_patterns):
            continue
        yield md_file


def normalize_path(path: Union[str, Path], base: Path = None) -> Path:
    """Normalise un chemin relatif ou absolu."""
    path = Path(path)
    if not path.is_absolute() and base:
        path = base / path
    return path.resolve()


def read_file_safe(filepath: Path, encoding: str = "utf-8") -> str:
    """Lit un fichier avec gestion d'erreurs d'encodage."""
    try:
        return filepath.read_text(encoding=encoding)
    except UnicodeDecodeError:
        # Fallback avec erreurs ignorées
        return filepath.read_text(encoding=encoding, errors="ignore")
