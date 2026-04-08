# src/py_mdlint/__init__.py
"""py-mdlint — Markdown linter compatible avec DavidAnson/markdownlint."""

__version__ = "1.0.0"
__all__ = ["main", "load_rules", "parse_markdown", "MarkdownlintConfig"]

from .cli import main
from .registry import load_rules
from .parser import parse_markdown
from .config import MarkdownlintConfig
