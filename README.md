# 18 Hacks for Qwen3.6+ with Super-Promptor

<!-- markdownlint-disable MD013 -->

> 🎯 Optimisez votre utilisation de Qwen3.6+ via OpenRouter avec 18 stratégies avancées de gestion de tokens, pilotées par Promptor, votre expert en Reverse Prompt Engineering.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Qwen3.6+](https://img.shields.io/badge/Model-Qwen3.6+-blue)](https://qwenlm.github.io/)
[![OpenRouter](https://img.shields.io/badge/Provider-OpenRouter-orange)](https://openrouter.ai/)
[![PowerShell](https://img.shields.io/badge/Shell-PowerShell_7.6+-blueviolet)](https://learn.microsoft.com/powershell/)
[![Promptor Council](https://img.shields.io/badge/Promptor-v3_Council_Edition-brightgreen)](COUNCIL_INTEGRATION.md)

---

## 📋 Table des Matières

- [🎬 Origine du Projet](#-origine-du-projet)
- [❓ Pourquoi ce projet ?](#-pourquoi-ce-projet-)
- [🔑 Concepts Clés](#-concepts-clés)
- [📊 Le Problème : Coût Exponentiel des Tokens](#-le-problème--coût-exponentiel-des-tokens)
- [✅ La Solution : Hygiène de Contexte + Promptor](#-la-solution--hygiène-de-contexte--promptor)
- [🚀 Installation Rapide](#-installation-rapide)
- [⚙️ Configuration](#️-configuration)
- [🎯 Utilisation Quotidienne](#-utilisation-quotidienne)
- [📚 Les 18 Hacks Détaillés](#-les-18-hacks-détaillés)
- [🤖 Promptor : Votre Assistant de Création de Prompts](#-promptor--votre-assistant-de-création-de-prompts)
  - [⭐ NOUVEAU : Promptor v3 Council Edition](#-nouveau--promptor-v3-council-edition)
- [🔍 Dépannage](#-dépannage)
- [❓ FAQ](#-faq)
- [🤝 Contribuer](#-contribuer)
- [📜 Licence](#-licence)

---

## 🎬 Origine du Projet

Ce projet est la **transposition fidèle et adaptée** des 18 hacks + les 5 cercles + le reverse prompt engineering, via
la modélisation des instructions dans le but de générer une représentation d'arbre décisionnel, présentés dans les vidéos YouTube
**[18 Claude Code Hacks You NEED to Know About](https://youtu.be/WSL8730oQ8A?si=N6gA07gIgN3YlLjX)**, les **[5 cercles |
Claude Code : LA sauce secrète pour le cadrer SYSTEMATIQUEMENT](https://youtu.be/jDlGwnIc57Y?si=L2FzIvItPHECDA3d)** et **[J'ai testé tous les prompts Claude : voici le meilleur!](https://youtu.be/iRCn9yKBIfo?si=UVAaqrRXTvqKvSHP)**
initialement conçus pour **Claude Code d'Anthropic**, vers l'écosystème **Qwen3.6+ via OpenRouter et OpenCode**.

### Pourquoi une transposition ?

La vidéo originale expose des stratégies brillantes d'optimisation de tokens pour Claude Code.
Cependant, **Qwen3.6+ n'est pas Claude** : son architecture (linear attention + sparse MoE),
son contexte natif de 1M tokens, son système de cache (prefix matching implicite + `cache_control` explicite),
et son accès via OpenRouter (API OpenAI-compatible, pas de commandes `/slash` natives) nécessitent
une **adaptation technique profonde**, pas un simple copier-coller.

### Ce que ce projet apporte en plus

| Aspect | Vidéo Originale (Claude) | Ce Projet (Qwen3.6+) |
| ------ | ----------------------- | ------------------- |
| **Modèle** | Claude 3.5/4 Sonnet | Qwen3.6-Plus / Flash / Max |
| **Accès** | CLI Claude Code natif | OpenRouter (API OpenAI-compatible) |
| **Cache** | `cache_control: ephemeral` natif | Prefix matching implicite + gestion client-side |
| **Commandes** | `/clear`, `/compact`, `/think` | Équivalents programmatiques via `messages` array |
| **Monitoring** | Commandes intégrées | Parsing `response.usage` + alertes personnalisées |
| **Prompt Engineering** | Implicite | **Promptor** : meta-prompt expert en Reverse Prompt Engineering |

### La valeur ajoutée de Promptor

Au-delà de la simple transposition technique, ce projet intègre **Promptor**, un meta-prompt
expert en création de prompts sur-mesure. Promptor applique automatiquement les hacks pertinents
lors de la génération de prompts, créant ainsi une **boucle vertueuse d'optimisation** :
les hacks améliorent les prompts, et Promptor génère des prompts qui respectent les hacks.

---

## ❓ Pourquoi ce projet ?

Lorsque vous interagissez avec un modèle de langage comme **Qwen3.6+**, chaque message déclenche une
**relecture complète de l'historique**. Le coût en tokens n'est pas linéaire, il est **exponentiel**.
Une conversation de 100 messages peut consommer 98,5 % de ses tokens uniquement pour la relecture du
contexte, sans apporter de valeur réelle à la requête courante.

Ce problème est amplifié par :

- **L'overhead système invisible** : fichiers de configuration, serveurs MCP, outils déclarés
- **La dégradation progressive** : plus la conversation est longue, plus la qualité se dégrade ("lost in the middle")
- **L'absence de monitoring natif** : sans outil de suivi, on consomme sans voir

Ce projet résout ce problème par une approche duale :

1. **18 Hacks d'Optimisation** : Stratégies concrètes, organisées en 3 niveaux (Fondamentaux, Intermédiaire, Expert), adaptées spécifiquement à Qwen3.6+ / OpenRouter.
2. **Promptor** : Meta-prompt expert en Reverse Prompt Engineering qui génère des prompts sur-mesure, en appliquant automatiquement les hacks pertinents.

---

## 🔑 Concepts Clés

| Terme | Définition |
| ----- | --------- |
| **Token** | Plus petite unité de texte traitée et facturée. En français, 1 token ≈ 1,3 mots. |
| **Hygiène de Contexte** | Pratique consistant à maintenir un contexte minimal et pertinent pour éviter la dégradation des performances et le gaspillage de tokens. |
| **Promptor** | Expert virtuel spécialisé en création de prompts optimisés. Applique systématiquement les hacks pertinents lors de la génération. |
| **OpenRouter** | Plateforme d'agrégation de modèles LLM offrant un accès unifié via une API compatible OpenAI. Supporte Qwen, Claude, GPT et bien d'autres. |
| **Prefix Caching** | Mécanisme de cache qui évite de retraiter le contexte inchangé entre les appels. Timeout d'environ 5 minutes sur OpenRouter. |
| **Lost in the Middle** | Phénomène où les informations situées au milieu d'un long contexte sont moins bien prises en compte par le modèle. |
| **Sparse MoE** | Architecture de Qwen3.6+ (Mixture of Experts) qui n'active qu'une partie des paramètres par token, permettant un contexte large à coût réduit. |
| **Reverse Prompt Engineering** | Technique consistant à analyser un résultat souhaité pour reconstruire le prompt optimal qui le génère. Spécialité de Promptor. |

---

## 📊 Le Problème : Coût Exponentiel des Tokens

### Croissance de la consommation par message

| Message | Contenu relu par le modèle | Coût estimé (tokens) |
| ------- | ------------------------- | ------------------- |
| 1 | Message 1 + réponse | ~500 |
| 2 | Messages 1-2 + réponses 1-2 | ~1 500 |
| 5 | Messages 1-5 + réponses 1-5 | ~4 000 |
| 10 | Messages 1-10 + réponses 1-10 | ~8 000 |
| 30 | Messages 1-30 + réponses 1-30 | ~15 000+ |
| 50 | Messages 1-50 + réponses 1-50 | ~25 000+ |

### Overhead invisible ajouté à chaque message

| Source | Impact estimé | Détail |
| ------ | -------------- | ------ |
| 📄 `.promptor_starter.md` | ~2-5k tokens | Matrice Promptor chargée en contexte |
| 📄 `qwen_sys.md` | ~1-3k tokens | Instructions système (si <200 lignes) |
| 🔌 Serveurs MCP connectés | ~5-18k tokens/msg | Par serveur MCP actif |
| 🛠️ Outils/functions déclarés | ~1-3k tokens/outil | Définition JSON injectée à chaque appel |
| 📁 Fichiers référencés | Variable | Dépend de la taille des fichiers |

**Conclusion** : Sans optimisation, une session de 50 messages avec 2 serveurs MCP et 3 outils
peut consommer **50 000+ tokens** dont seulement 10-15 % utiles à la tâche réelle.

---

## ✅ La Solution : Hygiène de Contexte + Promptor

### Bénéfices Attendus

| Bénéfice | Impact Estimé | Détail |
| ------- | ------------ | ------ |
| 💰 Économie de tokens | 60-80 % de réduction | Sur sessions longues (>30 messages) |
| 🎯 Qualité de réponse | Moins de "lost in the middle" | Contexte focalisé = réponses plus pertinentes |
| ⚡ Productivité | Moins d'itérations | Résultats plus précis du premier coup |
| 🎛️ Contrôle total | Monitoring temps réel | Alertes configurables, routing intelligent |
| 🔄 Automatisation | Promptor applique les hacks | Plus besoin d'y penser manuellement |

### Philosophie du Projet

> **"Le meilleur token est celui qu'on ne consomme pas."**

Chaque hack de ce projet suit 3 principes :

1. **Mesurable** : Le gain en tokens doit être quantifiable
2. **Reproductible** : Applicable systématiquement, pas au cas par cas
3. **Transparent** : L'utilisateur ne doit pas avoir à y penser

---

## 🚀 Installation Rapide

### Prérequis

- ✅ PowerShell 7.6+ ([Installer](https://learn.microsoft.com/powershell/scripting/install/installing-powershell))
- ✅ Git ([Installer](https://git-scm.com/download/win))
- ✅ GitHub CLI (`gh`) ([Installer](https://cli.github.com/))
- ✅ OpenCode ([Documentation](https://opencode.ai))
- ✅ Compte OpenRouter avec clé API ([Créer une clé](https://openrouter.ai/keys))
- ✅ Python 3.10+ (pour les exemples) ([Installer](https://python.org/downloads/))

### Commandes d'Initialisation

```powershell
# 1. Vérifier l'authentification GitHub CLI
gh auth status || gh auth login

# 2. Se placer dans l'espace de travail
Set-Location C:\Users\bbrod\Projets

# 3. Cloner ce dépôt (privé)
gh repo clone valorisa/18-Hacks-for-Qwen3.6+_with-Super-Promptor -- --depth 1

# 4. Accéder au projet
Set-Location "18-Hacks-for-Qwen3.6+_with-Super-Promptor"

# 5. Copier les exemples de configuration
Copy-Item config/opencode/.env.example config/opencode/.env
Copy-Item config/opencode/opencode.json.example config/opencode/opencode.json
```

---

## ⚙️ Configuration

### Architecture des Fichiers

| Fichier | Rôle | Portée |
| ------- | ---- | ------ |
| `~/.config/opencode/AGENTS.md` | 18 hacks d'optimisation tokens | **Toujours actif** dans toutes les sessions |
| `~/.config/opencode/commands/promptor.md` | Promptor (expert prompt engineering) | Actif via `/promptor` |
| `~/.config/opencode/opencode.json` | Provider + modèle par défaut | Configuration globale |

### Installation de la Configuration Globale

```powershell
# Copier les fichiers de config vers le dossier global d'OpenCode
Copy-Item config/opencode/AGENTS.md $env:USERPROFILE\.config\opencode\AGENTS.md
Copy-Item config/opencode/commands/promptor.md $env:USERPROFILE\.config\opencode\commands\promptor.md -Force
```

### Fichier `.env` (Variables Personnalisées)

Copiez `.env.example` vers `.env` et renseignez votre clé API :

```bash
# 🔑 OPENROUTER - Authentification
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxx

# 🎯 QWEN3.6+ - Paramètres d'optimisation
QWEN_DEFAULT_MODEL=qwen/qwen3.6-plus
QWEN_FLASH_MODEL=qwen/qwen-flash
QWEN_MAX_MODEL=qwen/qwen-max
QWEN_CONTEXT_LIMIT=1000000
QWEN_ALERT_WARNING=70
QWEN_ALERT_CRITICAL=90
QWEN_PLAN_MODE=true
QWEN_MANUAL_COMPACT_THRESHOLD=60
QWEN_CACHE_TIMEOUT_MIN=5
QWEN_MAX_SUBAGENTS=2
QWEN_OFFPEAK_START_HOUR=20
QWEN_ENABLE_OFFPEAK_SCHEDULING=false
QWEN_SYS_PROMPT_FILE=.qwen_sys.md
QWEN_PROGRESS_FILE=qwen_progress.md
QWEN_LOG_LEVEL=INFO
QWEN_DEBUG_TOKEN_USAGE=false
```

### Fichier `opencode.json`

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "openrouter": {
      "options": {
        "apiKey": "{env:OPENROUTER_API_KEY}"
      }
    }
  },
  "model": "openrouter/qwen/qwen3.6-plus-preview:free"
}
```

> ⚠️ **Ne commitez jamais votre fichier `.env`**. Il est déjà exclu par le `.gitignore`.

---

## 🎯 Utilisation Quotidienne

### Workflow Typique

```powershell
# Lancer OpenCode
opencode
```

Les 18 hacks sont **toujours actifs** (via `~/.config/opencode/AGENTS.md`).

Pour utiliser Promptor (création de prompts sur-mesure) :

```powershell
/promptor
```

### Étapes d'Utilisation

1. Lancez `opencode` dans votre projet
2. Les 18 hacks sont automatiquement appliqués dans chaque session
3. Tapez `/promptor` pour créer un prompt optimisé pour un outil IA cible
4. Décrivez votre besoin en langage naturel
5. Promptor génère un prompt optimisé appliquant les hacks pertinents
6. Copiez le prompt dans l'outil IA cible
7. Itérez jusqu'à obtenir un prompt 5 étoiles

---

## 📚 Les 18 Hacks Détaillés

### 🔹 Niveau 1 : Fondamentaux (Hacks 1-9)

| # | Hack | Gain Estimé | Implémentation Qwen3.6+ |
| - | ---- | ----------- | ---------------------- |
| 1 | **Nouvelle session par tâche** | ~40-60 % | Reset explicite de l'array `messages`. Pas de `/clear` natif, gestion client-side. |
| 2 | **Désactiver MCP inutiles** | ~5-18k tokens/msg | Supprimer les outils non utilisés de `tools=[]` dans l'appel API. |
| 3 | **Regrouper les prompts** | ~3x moins cher | 1 message combiné vs 3 follow-ups. Éditer/regénérer au lieu d'empiler. |
| 4 | **Plan Mode (95 % confiance)** | Évite réécritures | Exiger un plan structuré avant exécution via `extra_body={"reasoning_effort":"high"}`. |
| 5 | **Monitoring natif** | Visibilité temps réel | Parser `response.usage.prompt_tokens` à chaque appel API. |
| 6 | **Status Line** | Alertes proactives | Calculer `% contexte utilisé` en console à partir des réponses API. |
| 7 | **Dashboard OpenRouter** | Vue globale | Vérifier la conso sur [openrouter.ai/activity](https://openrouter.ai/activity) toutes les 20-30 min. |
| 8 | **Injection chirurgicale** | Réduction ciblée | Ne coller que la section/fonction nécessaire, jamais un fichier entier. |
| 9 | **Surveillance active** | Stop boucles inutiles | Détecter les répétitions dans `self.messages`, interrompre via paramètre `stop`. |

### 🔸 Niveau 2 : Intermédiaire (Hacks 10-14)

| # | Hack | Gain Estimé | Implémentation Qwen3.6+ |
| -- | ------ | ------------- | ------------------------ |
| 10 | **`.qwen_sys.md` < 200 lignes** | ~2-5k tokens/msg | Traiter comme un INDEX (pointeurs vers fichiers), pas un dump de contenu brut. |
| 11 | **Références précises `@fichier:Lx-Ly`** | Moins d'exploration | Guider le modèle vers des lignes spécifiques. Parsing regex côté client. |
| 12 | **Compact manuel à 60 %** | Qualité préservée | Demander un résumé structuré, resetter `messages`, réinjecter résumé + tâche. |
| 13 | **Gestion pauses >5 min** | Évite "full reload" | Compact avant absence. Le cache prefix OpenRouter expire après ~5 min d'inactivité. |
| 14 | **Troncature outputs shell** | ~50 lignes max | Filtrer les logs/CLI via regex. Un `git log` complet peut consommer des milliers de tokens. |

### 🔺 Niveau 3 : Expert (Hacks 15-18)

| # | Hack | Gain Estimé | Implémentation Qwen3.6+ |
| -- | ------ | ------------- | ------------------------ |
| 15 | **Router de modèles** | 40-60 % coût | `plus` (défaut), `flash` (sous-tâches), `max` (complexe). Logique conditionnelle. |
| 16 | **Sous-agents limités** | 7-10x moins cher | Max 2-3 parallèles. Déléguer à `qwen-flash`. Chaque sous-agent = contexte complet rechargé. |
| 17 | **Off-Peak Scheduling** | Meilleure dispo/coût | Peak : 14h-20h CET. Off-Peak : après 20h + weekend. Grouper les tâches lourdes hors pic. |
| 18 | **Source de vérité persistante** | Contexte raccourci | `qwen_progress.md` pour décisions stables et règles d'archi. Jamais de logs de conversation. |

---

## 🤖 Promptor : Votre Assistant de Création de Prompts

### Fonctionnement

Promptor suit un workflow en 3 étapes itératives :

1. **Identification** : Pose 2 questions pour cerner votre besoin et l'outil cible
2. **Création** : Génère un prompt optimisé en 4 parties (Calibrage, Prompt, Auto-Critique, Interrogatoire)
3. **Itération** : Affine le prompt jusqu'à obtenir 5/5 étoiles

### ⭐ NOUVEAU : Promptor v3.1 Council Edition

**Architecture hybride avec délibération multi-perspective optionnelle + 4 garde-fous META**

Promptor v3.1 Council Edition étend le pipeline standard avec une **Phase 4 optionnelle : LLM Council**, basée sur la méthodologie d'Andrej Karpathy.

**Nouveautés v3.1 (2026-05-12) :**
- 🔍 **Détection proxy variables** : Évite le fairness-washing (variables interdites masquées par corrélations)
- 🏥 **Workflow humain obligatoire** : Si escalade détectée, qui/quand/quoi/comment doivent être spécifiés
- 🔧 **Questions META** : Architecture système + testabilité pour prompts production-critical
- 📐 **Note architecturale** : Clarification composant vs autonome dans prompt généré

[Voir le changelog complet v3.0 → v3.1](CHANGELOG_v3.1.md)

**Quand utiliser le Council ?**
- Prompts pour production critique (security, compliance, legal)
- Auto-critique < 4/5 sur domaine à haut risque
- Premier prompt d'un domaine complexe jamais exploré
- Impact business élevé (système client-facing, infrastructure critique)

**Architecture Council :**
```
Pipeline Standard (C1-C5 → 18 Hacks → A-B-C-D)
                    ↓
    [COUNCIL] trigger ou confirmation après auto-critique
                    ↓
    5 Advisors indépendants (parallèle, 30-60s)
    ├─ The Contrarian : Cherche les failles
    ├─ First Principles Thinker : Vérifie si c'est la bonne question
    ├─ The Expansionist : Opportunités manquées
    ├─ The Outsider : Curse of knowledge, fresh eyes
    └─ The Executor : Exécutabilité réelle
                    ↓
    Peer Review anonymisé (5 reviewers, 30-60s)
                    ↓
    Chairman Synthesis (20-30s)
    - Convergence : où les advisors s'accordent
    - Divergence : désaccords productifs
    - Angles morts : détectés via peer review
    - Recommandation finale
    - Action immédiate (une chose concrète)
                    ↓
    Artefacts générés
    ├─ council-report-{{timestamp}}.html (visuel, auto-ouvert)
    └─ council-transcript-{{timestamp}}.md (complet)
```

**Coût relatif :**
- Standard : 1x baseline (~20-30s)
- Council activé : ~11x baseline (~3 minutes)

**Trigger :**
- Ajouter `[COUNCIL]` à votre requête : `"Crée un prompt pour [tâche critique] [COUNCIL]"`
- Ou confirmer après proposition automatique (si auto-critique < 4/5 + domaine critique)

**Documentation complète :**
- 📘 [COUNCIL_INTEGRATION.md](COUNCIL_INTEGRATION.md) — Architecture détaillée, FAQ, roadmap
- 📄 [Exemple complet : Modération de contenu](examples/council-example-moderation.md) — Cas d'usage production avec verdict Council
- 📋 [README Commands](config/opencode/commands/README.md) — Comparaison v3 vs v3 Council

**Skill Claude Code disponible :** `/promptor-council`

### Options Utiles

| Option | Description | Exemple |
| ------ | ----------- | ------- |
| `[MODE:API]` | Format technique (JSON/code) | `"Génère un prompt pour analyser des données [MODE:API]"` |
| `[COLLAB:MODE]` | Co-création guidée étape par étape | `"Créons un prompt pour un agent support [COLLAB:MODE]"` |
| `[TUTO:MODE]` | Tutoriel interactif 4 étapes | Idéal première utilisation |
| `[FOOTER:MIN]` | Footer minimaliste (1 ligne) | Pour les réponses courtes |
| `[DEBUG:MODE]` | Affiche les infos techniques | Mode expert |
| `[EXPORT:COPY]` | Version condensée à copier | Pour partage rapide |
| `[?mot]` | Explication à la demande | `"C'est quoi un [?prompt] ?"` |

### Protocole de Lien Automatique avec les Hacks

Promptor applique systématiquement les hacks suivants lors de la génération de prompts :

- **Hack #3** : Regroupe les instructions en un seul prompt cohérent
- **Hack #4** : Exige un plan avant toute génération de code/contenu
- **Hack #11** : Utilise des références précises plutôt que des contextes larges
- **Hack #12** : Propose un compactage si le prompt généré est trop long
- **Hack #15** : Recommande le modèle Qwen adapté à la complexité du prompt

---

## 🔍 Dépannage

### OpenCode ne reconnaît pas `/promptor`

| Symptôme | Cause Probable | Solution |
| -------- | ------------- | -------- |
| `/promptor` n'apparaît pas | Fichier `promptor.md` absent du dossier `commands/` | Vérifier `~/.config/opencode/commands/promptor.md` |
| Les hacks ne sont pas appliqués | Fichier `AGENTS.md` absent | Vérifier `~/.config/opencode/AGENTS.md` |
| `Unrecognized key: "commands"` | JSON config invalide | Lancer `scripts/Fix-OpenCodeConfig.ps1` |

### Consommation de tokens toujours élevée

| Vérification | Commande / Action |
| ------------ | ----------------- |
| MCP inutiles connectés | Déconnecter les serveurs MCP non essentiels |
| `.qwen_sys.md` trop long | `Get-Content .qwen_sys.md`, Measure-Object -Line` (doit être <200) |
| Pas de compact manuel | Surveiller `% contexte` → compacter à 60 % |
| Outputs shell non filtrés | Utiliser des hooks pour tronquer les logs >50 lignes |
| Modèle surdimensionné | Vérifier le routing : `flash` pour les tâches simples |

### Problèmes Python (exemples)

| Erreur | Cause | Solution |
| ------ | ----- | -------- |
| `ModuleNotFoundError: No module named 'openai'` | Dépendance manquante | `pip install -r examples/requirements.txt` |
| `OPENROUTER_API_KEY not set` | Variable d'environnement absente | Copier `.env.example` vers `.env` et renseigner la clé |
| `401 Unauthorized` | Clé API invalide | Vérifier la clé sur [openrouter.ai/keys](https://openrouter.ai/keys) |

---

## ❓ FAQ

### Q1 : Ce projet est-il un fork de la vidéo YouTube originale ?

Non. Ce projet est une **transposition indépendante** des concepts présentés dans la vidéo
[18 Claude Code Hacks You NEED to Know About](https://youtu.be/WSL8730oQ8A?si=N6gA07gIgN3YlLjX),
adaptés spécifiquement à l'écosystème Qwen3.6+ / OpenRouter. Aucune affiliation avec l'auteur
de la vidéo ou Anthropic. Crédit intellectuel reconnu dans le README.

### Q2 : Pourquoi Qwen3.6+ et pas un autre modèle ?

Qwen3.6+ offre un **contexte natif de 1M tokens**, une architecture **sparse MoE** efficace,
et un accès abordable via OpenRouter (y compris une version gratuite `:free`). C'est un excellent
compromis qualité/coût pour les développeurs qui travaillent sur des sessions longues avec
du codage agentique et de la génération de contenu.

### Q3 : Les 18 hacks fonctionnent-ils avec d'autres modèles (GPT-4, Claude, etc.) ?

Les **principes généraux** (hygiène de contexte, regroupement de prompts, monitoring) sont
universels. Cependant, les **implémentations techniques** (cache, routing, compactage) sont
spécifiques à Qwen3.6+ / OpenRouter. Pour Claude, référez-vous à la vidéo originale. Pour GPT-4,
une adaptation serait nécessaire (notamment sur le caching et le monitoring).

### Q4 : Promptor remplace-t-il ChatGPT ou Claude pour créer des prompts ?

Non. Promptor est un **meta-prompt** : c'est un système de règles qui s'exécute DANS un modèle
IA (Qwen3.6+, ChatGPT, Claude, etc.) pour lui faire générer des prompts optimisés. Vous avez
besoin d'un modèle IA pour exécuter Promptor. La valeur ajoutée est dans la **méthodologie**
et l'**application automatique des hacks**.

### Q5 : Combien de tokens économise-t-on vraiment avec ces hacks ?

Les économies varient selon l'usage, mais en moyenne :

- **Sessions courtes (<10 messages)** : 20-30 % d'économie (hacks 1-3 suffisent)
- **Sessions moyennes (10-30 messages)** : 40-60 % d'économie (hacks 1-9)
- **Sessions longues (30+ messages)** : 60-80 % d'économie (tous les hacks)

Le gain principal vient du **regroupement des prompts** (hack #3) et du **compactage manuel** (hack #12).

### Q6 : Puis-je utiliser ce projet sans OpenCode ?

Oui. Les 18 hacks et le wrapper Python (`qwen_optimizer.py`) sont utilisables avec **n'importe
quel client API OpenAI-compatible**. OpenCode n'est qu'une interface pratique. Vous pouvez
intégrer les hacks directement dans vos scripts Python, vos applications, ou tout autre outil
qui consomme l'API OpenRouter.

### Q7 : Le fichier `.promptor_starter.md` consomme-t-il des tokens à chaque message ?

Oui, comme tout fichier chargé en contexte système. C'est pourquoi la version incluse dans ce
projet est optimisée pour être **la plus concise possible** tout en conservant toutes les
fonctionnalités. Si vous avez besoin d'une version encore plus légère, utilisez l'option
`[FOOTER:MIN]` dans vos interactions avec Promptor.

### Q8 : Comment contribuer à ce projet ?

1. Forkez le dépôt
2. Créez une branche : `git checkout -b feat/ma-fonctionnalite`
3. Committez : `git commit -m "feat: ajout de [description]"`
4. Poussez : `git push origin feat/ma-fonctionnalite`
5. Ouvrez une Pull Request vers `dev`

Voir la section [Contribuer](#-contribuer) pour les détails.

### Q9 : Ce projet est-il gratuit ?

Oui, distribué sous **licence MIT**. Vous pouvez l'utiliser, le modifier et le distribuer
librement, y compris pour un usage commercial. Voir le fichier [LICENSE](LICENSE) pour les détails.

### Q10 : Où trouver la vidéo originale ?

[18 Claude Code Hacks You NEED to Know About](https://youtu.be/WSL8730oQ8A?si=N6gA07gIgN3YlLjX)
sur YouTube. Cette vidéo est la source d'inspiration technique de ce projet. Regardez-la pour
comprendre les hacks dans leur contexte Claude Code original.

### Q11 : Qu'est-ce que le LLM Council et quand l'utiliser ?

Le **LLM Council** (Promptor v3 Council Edition) est un système de validation multi-perspective optionnel qui soumet votre prompt à 5 advisors indépendants :

- **The Contrarian** cherche les failles et points de rupture
- **The First Principles Thinker** vérifie si vous posez la bonne question
- **The Expansionist** détecte les opportunités manquées
- **The Outsider** révèle la "curse of knowledge" (jargon opaque)
- **The Executor** évalue l'exécutabilité réelle ("utilisable lundi matin ?")

Après leurs analyses, un **peer review aveugle** identifie les angles morts, puis un **Chairman** synthétise un verdict structuré avec recommandations et action immédiate.

**Quand l'utiliser :**
- ✅ Prompts pour production critique (security, compliance, legal)
- ✅ Auto-critique Promptor < 3/5
- ✅ Premier prompt d'un domaine complexe
- ✅ Impact business élevé (système client-facing, infrastructure)

**Quand le skip :**
- ❌ Prompt expérimental/interne
- ❌ Itération rapide (A/B testing)
- ❌ Auto-critique >= 4/5 sur domaine non-critique
- ❌ Budget/temps contraint

**Coût :** ~11x plus cher que le pipeline standard (5 advisors + 5 reviewers + 1 chairman)
**Temps :** +2-3 minutes vs ~20-30s standard

**Exemple :** Un prompt de modération de contenu avec Council a révélé 5 angles morts critiques (GDPR compliance, échelle multilingue, coût humain des escalations) que l'auto-critique seule avait manqués. Voir [examples/council-example-moderation.md](examples/council-example-moderation.md).

---

## 🤝 Contribuer

### Stratégie de Branches

```text
main   ← Branche de production (stable, taguée)
  │
  └── dev  ← Branche d'intégration (prochaine version)
        │
        ├── feat/add-webhook-alerts    ← Nouvelle fonctionnalité
        ├── fix/token-count-overflow   ← Correction de bug
        └── docs/update-readme         ← Mise à jour documentation
```

### Workflow de Contribution

1. **Forker** le dépôt depuis GitHub
2. **Créer une branche** depuis `dev` :

   ```powershell
   git checkout dev
   git checkout -b feat/ma-nouvelle-fonctionnalite
   ```

3. **Commiter** avec un message conventionnel :

   ```powershell
   git commit -m "feat: ajout de [description]"
   ```

4. **Pusher** la branche :

   ```powershell
   git push origin feat/ma-nouvelle-fonctionnalite
   ```

5. **Ouvrir une Pull Request** vers `dev` via `gh pr create` ou l'interface GitHub

### Conventions de Commit

| Préfixe | Usage | Exemple |
| ------- | ----- | ------- |
| `feat:` | Nouvelle fonctionnalité | `feat: ajout alertes webhook Discord` |
| `fix:` | Correction de bug | `fix: comptage tokens incorrect` |
| `docs:` | Documentation | `docs: mise à jour section FAQ` |
| `refactor:` | Refactoring sans changement fonctionnel | `refactor: simplification du router` |
| `perf:` | Optimisation de performance | `perf: réduction overhead tools` |
| `test:` | Ajout ou modification de tests | `test: couverture du wrapper Python` |

---

## 📜 Licence

Distribué sous la licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus d'informations.

```text
MIT License

Copyright (c) 2026 valorisa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

<!-- markdownlint-enable MD013 -->
