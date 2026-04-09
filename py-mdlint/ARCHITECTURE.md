# ARCHITECTURE — py-mdlint

> Document de référence pour les décisions techniques. Mis à jour à chaque changement d'architecture.

## Objectifs

- Compatible `markdownlint` JS (règles MD001→MD060, gaps exclus)
- Installable via `pip install py-mdlint`
- CLI interactive (couleurs sobres) + mode batch CI
- Mode `--fix` idempotent pour règles auto-fixables
- Extensible : ajout de règles via simple fichier dans `rules/`

## Composants principaux

```text
src/py_mdlint/
├── cli.py          # Entry point + routing interactive/batch/watch
├── interactive.py  # Menu 6 écrans + couleurs sobres + NO_COLOR support
├── parser.py       # Wrapper markdown-it-py → AST normalisé (1-indexed)
├── config.py       # Chargement JSON/YAML + validation pydantic
├── registry.py     # Auto-discovery des règles depuis rules/
├── reporter.py     # Sorties: console, JSON, GitHub Annotations
├── fixer.py        # Orchestrateur --fix (ordre inverse, idempotent)
├── watcher.py      # Mode --watch avec watchdog (optional)
├── rules/
│   ├── base.py     # Classe abstraite Rule + Violation dataclass
│   ├── md001.py    # Exemple de règle implémentée
│   └── ...         # 52 règles restantes à ajouter
└── utils/
    ├── colors.py   # Palette cyan/vert/blanc/jaune + fallback
    ├── fs.py       # Découverte fichiers, normalisation paths
    └── text.py     # Utilities pour auto-fixes (rstrip, normalize_spaces...)
```

## Flux d'exécution

```text
[CLI] → [Config] → [Parser] → [Registry.load_rules()]
       → [Rule.check() for each] → [Reporter.format()]
       → [Fixer.apply() if --fix] → [Output]
```

## Palette couleurs (sobres)

| Usage | Code ANSI | Variable |
| ----- | --------- | -------- |
| Bordures menu | `\033[96m` | `Colors.CYAN` |
| Titres/numéros/succès | `\033[92m` | `Colors.GREEN` |
| Texte courant | `\033[97m` | `Colors.WHITE` |
| Erreurs/avertissements | `\033[93m` | `Colors.YELLOW` |
| Reset | `\033[0m` | `Colors.RESET` |

→ Support `NO_COLOR` env var + fallback silencieux si terminal non-compatible.

## Mode `--watch` (optional)

- Dépendance : `watchdog` (extra: `pip install py-mdlint[watch]`)
- Surveillance récursive du dossier cible
- Re-lint automatique sur modification `.md`
- Output compact : uniquement violations nouvelles/modifiées
- Désactivable via `--no-watch` ou env `PY_MDLINT_WATCH=0`

## Validation config avec Pydantic

```python
# Exemple schema partiel
class MarkdownlintConfig(BaseModel):
    default: bool = True
    MD013: Optional[LineLengthConfig] = None
    MD033: Optional[HTMLConfig] = None
    # ... autres règles
```

→ Validation stricte au chargement, erreurs explicites.

## Stratégie de tests

- 1 fichier `test_rules/test_mdXXX.py` par règle
- Fixture `run_rule()` pour exécution isolée
- Tests : violation_detected, clean_passes, fix_if_applicable, config_override
- Couverture cible : ≥90% sur `rules/` et `fixer.py`

## Publication

- Build : `python -m build`
- Validation : `twine check dist/*`
- Publication : `twine upload dist/*` (via GitHub Actions sur tag)

## Roadmap v0.1→v1.0

| Version | Objectif | Règles |
| ------- | -------- | ------ |
| v0.1.0-alpha | Squelette validable | Structure + MD001 exemple |
| v0.2.0-beta | Top 10 règles fréquentes | MD001/003/009/012/022/025/031/032/047 + fixes |
| v0.5.0-rc | 53 règles complètes | Toutes règles + tests + docs |
| v1.0.0 | Production ready | Stability guarantee + semver |
