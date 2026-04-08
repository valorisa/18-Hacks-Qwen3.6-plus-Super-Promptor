# src/py_mdlint/config.py
"""Chargement et validation de configuration avec Pydantic."""

import json
from pathlib import Path
from typing import Optional, Union

from pydantic import BaseModel, Field, field_validator


class LineLengthConfig(BaseModel):
    """Configuration pour MD013 (line-length)."""
    line_length: int = Field(default=80, ge=0)  # 0 = illimité
    code_blocks: bool = True
    tables: bool = True


class HTMLConfig(BaseModel):
    """Configuration pour MD033 (no-inline-html)."""
    allowed_elements: list[str] = Field(default_factory=list)


class HeadingStructureConfig(BaseModel):
    """Configuration pour MD043 (heading-structure)."""
    headings: list[str] = Field(default_factory=lambda: ["#"])


class HeadingStyleConfig(BaseModel):
    """Configuration pour MD003 (heading-style)."""
    style: str = Field(default="atx")


class TrailingSpacesConfig(BaseModel):
    """Configuration pour MD009 (no-trailing-spaces)."""
    br_spaces: int = Field(default=0, ge=0)


class MultipleBlanksConfig(BaseModel):
    """Configuration pour MD012 (no-multiple-blanks)."""
    maximum: int = Field(default=1, ge=1)


class BlanksAroundHeadingsConfig(BaseModel):
    """Configuration pour MD022 (blanks-around-headings)."""
    lines_above: int = Field(default=1, ge=0)
    lines_below: int = Field(default=1, ge=0)


class SingleTitleConfig(BaseModel):
    """Configuration pour MD025 (single-title)."""
    level: int = Field(default=1, ge=1, le=6)
    front_matter_title: str = Field(default=r"^\s*title\s*[:=]")


class BlanksAroundFencesConfig(BaseModel):
    """Configuration pour MD031 (blanks-around-fences)."""
    list_items: bool = Field(default=True)


class SingleTrailingNewlineConfig(BaseModel):
    """Configuration pour MD047 (single-trailing-newline)."""
    pass


class MarkdownlintConfig(BaseModel):
    """
    Schéma principal de configuration.
    
    Supporte:
    - Activation/désactivation globale via "default"
    - Paramètres par règle via clé MDXXX
    """
    default: bool = True
    MD003: Optional[HeadingStyleConfig] = None
    MD009: Optional[TrailingSpacesConfig] = None
    MD012: Optional[MultipleBlanksConfig] = None
    MD013: Optional[LineLengthConfig] = None
    MD022: Optional[BlanksAroundHeadingsConfig] = None
    MD025: Optional[SingleTitleConfig] = None
    MD031: Optional[BlanksAroundFencesConfig] = None
    MD033: Optional[HTMLConfig] = None
    MD043: Optional[HeadingStructureConfig] = None
    MD047: Optional[SingleTrailingNewlineConfig] = None
    
    @field_validator("*", mode="before")
    @classmethod
    def parse_rule_config(cls, value, info):
        """Permet de passer un bool ou un dict pour activer/configurer une règle."""
        if isinstance(value, bool):
            return value
        if isinstance(value, dict):
            return value
        return value
    
    def is_rule_enabled(self, rule_id: str) -> bool:
        """Vérifie si une règle est activée."""
        rule_config = getattr(self, rule_id, None)
        if rule_config is None:
            return self.default  # Fallback sur default
        if isinstance(rule_config, bool):
            return rule_config
        return True  # Dict présent = activée
    
    def get_rule_params(self, rule_id: str) -> dict:
        """Récupère les paramètres d'une règle sous forme de dict."""
        rule_config = getattr(self, rule_id, None)
        if isinstance(rule_config, BaseModel):
            return rule_config.model_dump()
        if isinstance(rule_config, dict):
            return rule_config
        return {}


def load_config(config_path: Optional[Union[str, Path]] = None) -> MarkdownlintConfig:
    """
    Charge la configuration depuis un fichier JSON/YAML.
    
    Priorité de recherche :
    1. Chemin explicite via argument CLI
    2. .markdownlint.json dans cwd
    3. .markdownlint.yaml dans cwd
    4. Recherche ascendante vers racine Git
    5. Fallback: config par défaut (toutes règles activées)
    """
    from .utils.fs import read_file_safe
    
    # Détection automatique si aucun chemin fourni
    if config_path is None:
        for candidate in [".markdownlint.json", ".markdownlint.yaml", ".markdownlint.yml"]:
            if Path(candidate).exists():
                config_path = candidate
                break
    
    # Fallback si aucun fichier trouvé
    if config_path is None or not Path(config_path).exists():
        return MarkdownlintConfig()
    
    # Lecture et parsing
    content = read_file_safe(Path(config_path))
    path = Path(config_path)
    
    if path.suffix in (".yaml", ".yml"):
        try:
            import yaml
            data = yaml.safe_load(content)
        except ImportError:
            raise ImportError(
                "YAML config requires 'pyyaml'. Install with: pip install py-mdlint[yaml]"
            )
    else:
        data = json.loads(content)
    
    return MarkdownlintConfig.model_validate(data)
