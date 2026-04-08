# Changelog

Toutes les modifications notables de ce projet sont documentées ici.

## [1.0.0] - 2026-04-07

### Added
- 🔒 **Mode `--strict`** : Transforme tous les avertissements en erreurs CI (`exit code 1` systématique si violations > 0)
- ⚡ **Cache AST persistant** : Stockage `.py-mdlint-cache/` via hash MD5 du contenu. Invalidation automatique sur modification. Accélère le lint sur les gros dépôts
- 🧩 **Système de Patch complet** : `insert`/`delete`/`replace` atomiques pour corriger proprement MD022/031/032/058 sans décalage de lignes
- 🌐 **Validation croisée JS** : `scripts/compare-with-js.js` pour comparer les sorties avec `markdownlint-cli2`
- 📊 **Reporter amélioré** : Sévérité dynamique (`🔴 ERROR` vs `⚠️ WARNING`), annotations GitHub `::error` en mode strict
- 📖 **README.md complet** : Installation, usage, config, CI, 53 règles documentées

### Changed
- Architecture stabilisée : `Rule.check()` + `Patch` standardisés
- `parser.py` refactoré avec cache optionnel (`use_cache=True`)
- CI ready : variable `PY_MDLINT_NO_CACHE=1` pour pipelines distribués
- Version bump : `0.1.0-alpha` → `1.0.0`

### Verified
- 53 règles actives (MD001→MD060, gaps exclus)
- 22 auto-fixables • 31 read-only
- Tests unitaires : 4 fonctions/règle (violation, clean, fix, config)
- Python 3.9–3.12 compatible

---

## [0.3.0-rc]

### Added
- 44 règles restantes implémentées
- `scripts/bootstrap_rule.py` : Générateur automatique `mdXXX.py` + `test_mdXXX.py`
- Structure `Patch` préliminaire dans `Violation`

### Changed
- `fixer.py` étendu pour gérer corrections globales
- `config.py` : Schemas Pydantic pour toutes les règles

---

## [0.2.0-beta]

### Added
- 9 règles prioritaires : MD003, MD009, MD012, MD022, MD025, MD031, MD032, MD047, MD033
- Menu interactif CLI (6 écrans, couleurs sobres, `NO_COLOR`)
- `ARCHITECTURE.md` (source de vérité technique)
- Tests `pytest` avec fixtures `run_rule()`

### Changed
- `parser.py` : Normalisation AST 1-indexed
- `reporter.py` : Support console/JSON/GitHub Annotations

---

## [0.1.0-alpha]

### Added
- Squelette `src/py_mdlint/` pip-ready
- `cli.py`, `interactive.py`, `config.py`, `fixer.py`, `watcher.py`
- Règle exemple MD001 + tests
- Workflows GitHub Actions (`mdlint-check`, `test`, `release`)
- `pyproject.toml` prêt PyPI
