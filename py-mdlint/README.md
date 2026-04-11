# 🐍 py-mdlint

> **Markdown linter Python compatible avec `markdownlint` JS**
> Installation pip-ready • CLI interactive & batch • Mode `--strict` • Cache AST • Auto-fix par patch • CI/CD ready

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Fonctionnalités

- ✅ **53 règles implémentées** (MD001→MD060, gaps exclus : 002, 006, 008, 015, 016, 017, 057)
- 🛠️ **Auto-fix intelligent** : 22 règles corrigées automatiquement, système de `patch` (`insert`/`delete`/`replace`)
- 🎨 **CLI interactive** : 6 écrans, couleurs sobres, support `NO_COLOR`
- 🚦 **Mode CI/Batch** : `--batch`, `--report github`, `--strict` (force exit 1)
- ⚡ **Cache AST** : Parsing accéléré pour gros dépôts (`.py-mdlint-cache/`)
- 🔍 **Validation croisée** : Script `compare-with-js.js` pour alignement avec `markdownlint-cli2`
- ⚙️ **Config flexible** : `.markdownlint.json` / `.yaml` avec validation Pydantic

## 📦 Installation

```bash
# Standard
pip install py-mdlint

# Avec cache & validation YAML
pip install "py-mdlint[yaml,watch]"

# Développement
pip install -e ".[dev,yaml,watch]"
```

## 🚀 Usage

### Mode Interactif (défaut)

```bash
$ py-mdlint
╔══════════════════════════════════╗
║  py-mdlint — Markdown Linter     ║
╠══════════════════════════════════╣
║  1. Linter un fichier/dossier    ║
║  2. Créer un fichier de config   ║
║  3. Voir les règles disponibles  ║
║  4. Linter + corriger            ║
║  5. Générer workflow GitHub      ║
║  6. Quitter                      ║
╚══════════════════════════════════╝
```

### Mode Batch (CI/Scripts)

```bash
py-mdlint --batch .
py-mdlint --batch --report json --config .custom.json docs/
py-mdlint --batch --fix --ignore MD013 .
```

### Mode Strict (Pipeline exigeant)

Transforme les warnings en erreurs CI (`exit code 1` sur toute violation).

```bash
py-mdlint --batch --strict .
# Sortie: 🔴 ERROR MD022 line 42
# Exit: 1 (échec du pipeline)
```

### Mode Watch (Développement)

Re-lint automatique sur modification `.md` (nécessite `watchdog`).

```bash
py-mdlint --batch --watch docs/
```

## ⚙️ Configuration

Créez `.markdownlint.json` à la racine :

```json
{
  "default": true,
  "MD013": { "line_length": 120, "tables": false },
  "MD033": { "allowed_elements": ["br", "img", "details"] },
  "MD007": { "indent": 2 }
}
```

> Supporte `.markdownlint.yaml` (installez `[yaml]` extra).

## 📋 Référentiel des Règles (53 actives)

### Headings (13 règles)

| ID | Alias | Description | Fixable |
| -- | ----- | ----------- | ------- |
| MD001 | heading-increment | Incrémentation niveau headings | ❌ |
| MD003 | heading-style | Cohérence style headings | ✅ |
| MD018 | no-missing-space-atx | Espace manquant après `#` | ✅ |
| MD019 | no-multiple-space-atx | Espaces multiples après `#` | ✅ |
| MD020 | no-missing-space-closed-atx | Espace manquant avant `#` fermant | ✅ |
| MD021 | no-multiple-space-closed-atx | Espaces multiples avant `#` fermant | ✅ |
| MD022 | blanks-around-headings | Lignes vides autour headings | ✅ |
| MD023 | heading-start-left | Heading doit débuter colonne 1 | ✅ |
| MD024 | no-duplicate-heading | Doublons de headings | ❌ |
| MD025 | single-title | Titre unique (h1) par doc | ❌ |
| MD026 | no-trailing-punctuation | Ponctuation finale dans headings | ✅ |
| MD041 | first-line-h1 | Première ligne = h1 | ❌ |
| MD043 | heading-structure | Structure de headings imposée | ❌ |

### Lists (7 règles)

| ID | Alias | Description | Fixable |
| -- | ----- | ----------- | ------- |
| MD004 | ul-style | Marqueur listes non-ordonnées | ✅ |
| MD005 | list-indent | Indentation listes incohérente | ✅ |
| MD007 | ul-indent | Indentation listes à puces | ✅ |
| MD029 | ol-prefix | Préfixe listes ordonnées | ✅ |
| MD030 | list-marker-space | Espaces après marqueurs listes | ✅ |
| MD031 | blanks-around-fences | Lignes vides autour blocs code | ✅ |
| MD032 | blanks-around-lists | Lignes vides autour listes | ✅ |

### Whitespace & Format (12 règles)

| ID | Alias | Description | Fixable |
| -- | ----- | ----------- | ------- |
| MD009 | no-trailing-spaces | Espaces en fin de ligne | ✅ |
| MD010 | no-hard-tabs | Tabulations dures | ✅ |
| MD012 | no-multiple-blanks | Lignes vides consécutives multiples | ✅ |
| MD013 | line-length | Longueur max des lignes | ❌ |
| MD027 | no-multiple-space-blockquote | Espaces après `>` | ✅ |
| MD028 | no-blanks-blockquote | Lignes vides dans blockquotes | ✅ |
| MD037 | no-space-in-emphasis | Espaces dans `*em*` | ✅ |
| MD038 | no-space-in-code | Espaces dans `` `code` `` | ✅ |
| MD039 | no-space-in-links | Espaces dans `[lien]` | ✅ |
| MD047 | single-trailing-newline | Nouvelle ligne unique en fin fichier | ✅ |
| MD049 | emphasis-style | Cohérence style emphase | ✅ |
| MD050 | strong-style | Cohérence style gras | ✅ |

### Links & Images (9 règles)

| ID | Alias | Description | Fixable |
| -- | ----- | ----------- | ------- |
| MD011 | no-reversed-links | Liens inversés | ✅ |
| MD034 | no-bare-urls | URLs nues non protégées | ✅ |
| MD042 | no-empty-links | Liens vides | ❌ |
| MD045 | no-alt-text | Textes alt manquants | ❌ |
| MD051 | link-fragments | Fragments de liens invalides | ❌ |
| MD052 | reference-links-images | Références sans définition | ❌ |
| MD053 | link-image-reference-definitions | Références inutilisées | ✅ |
| MD054 | link-image-style | Style autolink/explicite | ❌ |
| MD059 | descriptive-link-text | Texte de lien non descriptif | ❌ |

### Code & Style (8 règles)

| ID | Alias | Description | Fixable |
| -- | ----- | ----------- | ------- |
| MD014 | commands-show-output | `$` avant commandes sans output | ✅ |
| MD035 | hr-style | Cohérence règles horizontales | ✅ |
| MD036 | no-emphasis-as-heading | Emphase utilisée comme heading | ❌ |
| MD040 | fenced-code-language | Langage manquant dans blocs code | ❌ |
| MD044 | proper-names | Capitalisation noms propres | ✅ |
| MD046 | code-block-style | Style blocs code | ✅ |
| MD048 | code-fence-style | Style fence (backtick/tilde) | ✅ |
| MD055 | table-pipe-style | Style pipes tableaux | ✅ |

### Tables (4 règles)

| ID | Alias | Description | Fixable |
| -- | ----- | ----------- | ------- |
| MD056 | table-column-count | Nombre colonnes tableaux | ✅ |
| MD058 | blanks-around-tables | Lignes vides autour tableaux | ✅ |
| MD060 | table-column-style | Alignement colonnes tableaux | ✅ |

> 💡 **22 règles auto-fixables** • 31 nécessitent intervention manuelle

## 🔄 CI/CD Intégration

### GitHub Actions

```yaml
- name: Markdown Lint
  run: py-mdlint --batch --strict --report github .
  env:
    NO_COLOR: 1
    PY_MDLINT_NO_CACHE: 1
```

### Cache CI (optionnel)

```yaml
- name: Cache AST
  uses: actions/cache@v3
  with:
    path: .py-mdlint-cache
    key: ${{ runner.os }}-py-mdlint-${{ hashFiles('**/*.md') }}
```

## 🔍 Validation Croisée (Dev)

```bash
npm i -g markdownlint-cli2
node scripts/compare-with-js.js .
```

> Compare les sorties JSON et liste les écarts de détection.

## 🤝 Contribuer

1. Fork & clone
2. `pip install -e ".[dev]"`
3. `python scripts/bootstrap_rule.py MDXXX alias "desc" --fixable`
4. `pytest tests/ -v`
5. PR avec tests & docs mis à jour

**Licence** : MIT • **Compatible** : macOS, Linux, WSL, Windows 11
