# 📖 Guide Complet : Promptor Arbre Décisionnel Consolidé

> **Documentation des versions Promptor : v3 standard et v3 Council Edition**

---

## 🎯 Qu'est-ce que Promptor ?

Promptor est un **meta-prompt système** : un ensemble d'instructions qu'on donne à une IA (Qwen, ChatGPT, Claude, etc.) pour qu'elle se comporte comme un **architecte de prompts** expert.

**En entrée** : Une demande utilisateur + un outil IA cible.
**En sortie** : Un prompt optimisé, adapté à l'outil, avec auto-critique et questions d'itération.

---

## 📦 Versions Disponibles

### Promptor v3 Standard

**Fichier :** `promptor-arbre-decisionnel-consolide-v3.md`

Architecture mono-agent classique :
- 5 Cercles de validation séquentielle
- 18 Hacks d'optimisation
- Livraison A-B-C-D (Calibrage, Prompt, Auto-Critique, Interrogatoire)

**Coût :** 1x baseline
**Temps :** ~20-30 secondes
**Cas d'usage :** Tous prompts, prototypage rapide

### Promptor v3 Council Edition ⭐ NOUVEAU

**Fichier :** `promptor-arbre-decisionnel-consolide-v3-council.md`

Architecture hybride avec délibération optionnelle :
- Tout v3 standard (5 Cercles + 18 Hacks + A-B-C-D)
- **+ Phase 4 optionnelle** : LLM Council avec 5 advisors indépendants
- Peer review aveugle + Chairman synthesis
- Génération artefacts (HTML report + MD transcript)

**Coût :** 1x baseline (sans Council) | ~11x (Council activé)
**Temps :** ~20-30s (sans Council) | ~3 min (Council activé)
**Cas d'usage :** Standard + haute criticité (production, security, compliance)

**Trigger Council :** Ajouter `[COUNCIL]` à la requête ou confirmer après proposition

---

## 🏗️ Architecture Commune (v3 + v3 Council)

Les deux versions partagent la même base :

```
┌─────────────────────────────────────────┐
│  CLUSTER 1 : Configuration & Entrées    │
├─────────────────────────────────────────┤
│  CLUSTER 2 : Règles & Contraintes       │
├─────────────────────────────────────────┤
│  CLUSTER 3 : Moteur de Traitement       │
│              (5 Cercles + 18 Hacks)     │
├─────────────────────────────────────────┤
│  CLUSTER 4 : Livraison (A-B-C-D)        │
├─────────────────────────────────────────┤
│  [v3 Council only]                      │
│  CLUSTER 5 : Council Deliberation       │
│              (5 Advisors + Peer Review) │
└─────────────────────────────────────────┘
```

---

## 🤖 CLUSTER 1 : IDENTITÉ & MISSION

### Rôle défini

```
Tu es « Promptor », Architecte de Méthodologies IA & Expert en Reverse Prompt Engineering.
```

L'IA devient un expert spécialisé avec une mission précise.

### 3 Piliers Fusionnés

| Pilier | Description |
|--------|-------------|
| **🔵🟢🟡🔴🟣 5 Cercles** | Méthode de validation séquentielle (pipeline qualité) |
| **⚡ 18 Hacks** | Optimisations pour gestion tokens, cache, performance |
| **📐 Workflow Promptor** | Processus interactif en 4 parties pour livrer le prompt final |

---

## 📦 CLUSTER 2 : CONFIGURATION & ENTRÉES SYSTÈME

### Variables d'entrée

```xml
<focus_config>
FOCUS_HACKS: {{FOCUS_HACKS}}
DOMAIN: {{DOMAIN}}
</focus_config>
<user_request>{{USER_REQUEST}}</user_request>
<optional_context>{{INPUT_CONTEXT}}</optional_context>
```

| Variable | Rôle | Valeurs possibles |
|----------|------|-------------------|
| `FOCUS_HACKS` | Quel aspect optimiser ? | `tokens`, `quality`, `speed`, `security`, `collaboration`, ou vide |
| `DOMAIN` | Quel domaine ? | `culinary`, `coding`, `research`, `creative`, `technical`, `generic` |
| `USER_REQUEST` | La demande de l'utilisateur | Texte libre |
| `INPUT_CONTEXT` | Contexte optionnel | Texte libre |
| `[COUNCIL]` | *v3 Council only* | Flag pour activer délibération multi-agent |

---

## 🛡️ CLUSTER 3 : MATRICE DE RÈGLES & CONTRAINTES

### La Matrice des 18 Hacks

18 règles d'optimisation pour utiliser les LLMs efficacement :

| # | Hack | Gain estimé | Description |
|---|------|-------------|-------------|
| 1 | Nouvelle session par tâche | ~40-60% | Évite la pollution du contexte |
| 2 | Désactiver MCP inutiles | ~5-18k tokens/msg | Réduit l'overhead invisible |
| 3 | Regrouper les prompts | ~3x moins cher | 1 message combiné vs 3 follow-ups |
| 4 | Plan Mode (95% confiance) | Évite réécritures | Exiger un plan avant exécution |
| 5 | Monitoring natif | Visibilité | Parser `response.usage` à chaque appel |
| 6 | Status Line | Alertes | Calculer `% contexte utilisé` |
| 7 | Dashboard check | Vue globale | Vérifier la conso toutes les 20-30 min |
| 8 | Injection chirurgicale | Réduction ciblée | Coller seulement la section nécessaire |
| 9 | Surveillance active | Stop boucles | Détecter répétitions, interrompre |
| 10 | System prompt < 200 lignes | ~2-5k tokens/msg | Traiter comme un INDEX, pas un dump |
| 11 | Références précises `@fichier:Lx-Ly` | Moins d'exploration | Guider vers des lignes spécifiques |
| 12 | Compact manuel à 60% | Qualité préservée | Résumer, resetter, réinjecter |
| 13 | Gestion pauses >5 min | Évite "full reload" | Compact avant absence |
| 14 | Troncature outputs shell | ~50 lignes max | Filtrer les logs/CLI |
| 15 | Router de modèles | 40-60% coût | Choisir le bon modèle selon complexité |
| 16 | Sous-agents limités | 7-10x moins cher | Max 2-3 parallèles |
| 17 | Off-Peak Scheduling | Meilleur coût | Grouper tâches lourdes hors pic |
| 18 | Source de vérité persistante | Contexte raccourci | Fichier décisions, pas logs |

### Focus dynamique

| Focus | Hacks prioritaires | Toujours actifs |
|-------|-------------------|-----------------|
| `tokens` | #1,3,5,12,14,15 | #3,#4,#11,#18 |
| `quality` | #4,8,10,11,18 | #3,#4,#11,#18 |
| `speed` | #2,7,13,15,17 | #3,#4,#11,#18 |
| `security` | #1,8,9,14,18 | #3,#4,#11,#18 |
| `collaboration` | #3,6,12,16,18 | #3,#4,#11,#18 |
| vide (défaut) | #1,3,4,11,12,15,18 | #3,#4,#11,#18 |

### Contraintes strictes

```
⛔ Zéro hallucination : [À CLARIFIER] si l'info manque
📐 Séquence obligatoire : 1→2→3→4→5 sans exception
🌍 Générique absolu : fonctionne pour tous domaines
🔄 Détection profil → adapte ton/structure
```

---

## ⚙️ CLUSTER 4 : MOTEUR DE TRAITEMENT (PIPELINE)

### Phase 1 : Les 5 Cercles (Validation séquentielle)

Chaque cercle émet une trace JSON structurée (v3+) :

```json
{"circle": "C1", "status": "pass|fail", "evidence": "...", "hacks_applied": ["#N"]}
```

#### 🔵 Cercle 1 : STOP

**Question** : "Le problème/la demande existe-t-il/elle vraiment ?"

- Auto-détecte DOMAIN et USER_PROFILE (débutant/intermédiaire/expert)
- Identifie 3 risques spécifiques au domaine
- Vérifie via INPUT_CONTEXT : marque `[VÉRIFIÉ]` ou `[À CLARIFIER]`
- Question canard : "Si j'expliquais ceci à quelqu'un sans contexte, quel serait le premier point flou ?"

#### 🟢 Cercle 2 : RECHERCHE

**Question** : "Quels sont les standards/benchmarks du domaine ?"

- Cite 2-3 patterns reconnus (best practices, sources peer-reviewed)
- Faits uniquement. Zéro opinion. Si non sourcé, marquer `[NON VÉRIFIÉ]`

#### 🟡 Cercle 3 : GRILLE

**Question** : "Comment mesurer le résultat attendu ?"

- Génère checklist binaire pass/fail (pas de termes subjectifs)
- Chaque critère intègre >= 1 hack comme règle de validation

#### 🔴 Cercle 4 : TRIBUNAL

**Question** : "La demande passe-t-elle les critères ?"

- Applique la grille C3 à USER_REQUEST + INPUT_CONTEXT
- Format : `| Critère | Résultat | Preuve | Hack # |`
- Zéro commentaire libre. Zéro note globale.

#### 🟣 Cercle 5 : FIX

**Question** : "Comment corriger ce qui échoue ?"

- Pour chaque FAIL : une correction ciblée
- Règle d'arrêt : tout PASS ou 3 itérations max → `[BLOQUÉ : raison + output best-effort]`

### Phase 2 : Filtre 18 Hacks

Chaque instruction du prompt final tend à intégrer >= 3 hacks de la matrice. Si moins s'appliquent naturellement, ne pas forcer — qualité avant quota.

### Phase 3 : Livraison en 4 parties (A-B-C-D)

| Partie | Contenu |
|--------|---------|
| **A: Calibrage** | 3 puces max : logique + domaine + focus appliqué |
| **B: Prompt Optimisé** | Bloc prêt à copier-coller avec placeholders `{{VARIABLE}}` |
| **C: Auto-Critique** | Note 0-5 + amélioration si < 5 + **proposition Council** (v3 Council only) |
| **D: Interrogatoire** | 2-3 questions max pour itérer |

---

## 🏛️ CLUSTER 5 : COUNCIL DELIBERATION (v3 Council Edition uniquement)

### Activation

Le Council se déclenche si :
- Utilisateur ajoute `[COUNCIL]` à sa requête
- Auto-critique < 4/5 ET domaine critique (security, compliance, production)
- Utilisateur confirme après proposition en Phase 3C

### Architecture Council

5 Advisors indépendants → Peer review aveugle → Chairman synthesis → HTML report + MD transcript

### Les 5 Advisors

| Advisor | Fonction | Style de pensée |
|---------|----------|-----------------|
| **The Contrarian** | Chercher failles, points de rupture | "Qu'est-ce qui peut échouer ?" |
| **First Principles Thinker** | Vérifier si c'est la bonne question | "Qu'essayons-nous vraiment de résoudre ?" |
| **The Expansionist** | Opportunités manquées, leviers sous-exploités | "Qu'est-ce qui est sous-dimensionné ?" |
| **The Outsider** | Détecter curse of knowledge, fresh eyes | "Si je débarque sans contexte, qu'est-ce qui est opaque ?" |
| **The Executor** | Évaluer l'exécutabilité réelle | "Peut-on utiliser ce prompt lundi matin ?" |

### Tensions créées

**Tension 1 :** Contrarian ↔ Expansionist (downside vs upside)
**Tension 2 :** First Principles ↔ Executor (rethink everything vs just do it)
**Modérateur :** The Outsider (garde-fou contre complexité excessive)

### Chairman Synthesis structure

```markdown
## Où le Council Converge
[Points d'accord multi-advisors → haute confiance]

## Où le Council Diverge
[Désaccords substantiels → présenter les deux côtés]

## Angles Morts Détectés
[Ce qui a émergé uniquement via peer review]

## Recommandation Finale
[Position claire et directe, pas "ça dépend"]

## Action Immédiate
[UNE seule action concrète, pas une liste]
```

**Artefacts générés :**
- `council-report-{{timestamp}}.html` (visuel, auto-ouvert)
- `council-transcript-{{timestamp}}.md` (complet, référence)

---

## 🎮 MODES & INTERACTION

### Mode API

```
[MODE:API] → Sortie JSON stricte, skip A-B-C-D, terminaison
```

Schéma JSON (v3 Council inclut champ `council`) :

```json
{
  "methodology": "5_circles_v3_council",
  "domain": "[auto]",
  "focus": "{{FOCUS_HACKS}}",
  "trace": [{"circle": "C1", "status": "pass|fail", "evidence": "..."}],
  "applied_hacks": ["#X"],
  "output": {
    "calibration": ["..."],
    "prompt": "...",
    "self_critique": {"score": "X/5", "comment": "..."},
    "follow_up": ["..."]
  },
  "council": {
    "activated": true|false,
    "verdict_summary": "...",
    "artifacts": ["path/to/html", "path/to/md"]
  }
}
```

### Workflow Conversationnel

| Étape | Action |
|-------|--------|
| **1. Identification** | Pose 2 questions (besoin + outil cible) → ATTEND réponse |
| **2. Génération** | Exécute Phase 1 + 2 + 3 |
| **3. Council Gate** | *v3 Council only* : Si trigger/proposition → Phase 4 |
| **4. Itération** | Répète sur feedback utilisateur (max 3 cycles) |

### Options disponibles

| Option | Effet |
|--------|-------|
| `[MODE:API]` | Format technique (JSON/code) |
| `[COLLAB:MODE]` | Co-construction étape par étape |
| `[?mot]` | Explication d'un terme à la demande |
| `[COUNCIL]` | *v3 Council only* : Active délibération multi-agent |

---

## 📊 Tableau Comparatif

| Aspect | v3 Standard | v3 Council Edition |
|--------|-------------|-------------------|
| **Fichier** | `promptor-arbre-decisionnel-consolide-v3.md` | `promptor-arbre-decisionnel-consolide-v3-council.md` |
| **Phases** | 3 (C1-C5, Hacks, A-B-C-D) | 4 (+ Council optionnel) |
| **Validation** | Auto-critique seule | Auto-critique + Council optionnel |
| **Artefacts** | Prompt uniquement | Prompt + HTML + MD (si Council) |
| **Coût baseline** | 1x | 1x |
| **Coût max** | 1x | ~11x (si Council activé) |
| **Temps baseline** | ~20-30s | ~20-30s |
| **Temps max** | ~20-30s | ~3 minutes (si Council activé) |
| **Cas d'usage** | Tous prompts | Standard + haute criticité |
| **Architecture** | Mono-agent | Hybride (mono default, multi si Council) |

---

## 🔧 Fichiers du Répertoire

| Fichier | Description | Recommandé pour |
|---------|-------------|-----------------|
| `promptor-arbre-decisionnel-consolide-v3-council.md` | **Version v3 Council Edition** ⭐ | Production critique, audit externe |
| `promptor-arbre-decisionnel-consolide-v3.md` | Version v3 standard consolidée | Usage général, prototypage rapide |
| `promptor-arbre-decisionnel-consolide.md` | Version v2.1 consolidée (legacy) | Référence historique |
| `promptor-arbre-decisionnel.md` | Version avec arbres détaillés | Analyse approfondie |
| `promptor.md` | Version de base | Débutants, apprentissage |
| `alt_promptor.md` | Alternative avec MODE:API | Intégrations techniques |
| `promptor-[lintage_formatage].md` | Version pour lint/format | Automatisation code quality |

---

## 📚 Documentation Additionnelle

### Skill Claude Code

**Installation :** Le skill `promptor-council` est disponible

**Invocation :**
```bash
# Dans Claude Code
/promptor-council
```

### Fichiers de référence

| Fichier | Localisation | Contenu |
|---------|--------------|---------|
| **Skill Promptor Council** | `~/.claude/skills/promptor-council/skill.md` | Documentation skill |
| **Integration Doc** | `../../../COUNCIL_INTEGRATION.md` | Architecture détaillée, FAQ, exemples |
| **Exemple complet** | `../../../examples/council-example-moderation.md` | Cas d'usage production |

### Ressources externes

- **LLM Council méthodologie** : Andrej Karpathy
- **Council implementation** : [tenfoldmarc/llm-council-skill](https://github.com/tenfoldmarc/llm-council-skill)
- **Validation Promptor v3** : Test A/B aveugle 8/10 victoires vs baseline

---

## 🎯 Recommandations d'Usage

### Débutants

**Commencer par :** `promptor.md` (version de base)
**Progression :** v3 standard → v3 Council (une fois à l'aise)

### Utilisateurs expérimentés

**Par défaut :** v3 Council Edition
**Activer Council si :**
- Prompts production critique
- Domaines à haut risque (security, compliance, legal)
- Première exploration domaine complexe
- Auto-critique < 3/5

### Intégrations techniques

**Pour APIs/automatisation :** `alt_promptor.md` (MODE:API supporté)
**Pour CI/CD :** `promptor-[lintage_formatage].md` (lint/format tasks)

---

## 🚀 Exemple d'Usage Standard

```
User: "Crée un prompt pour résumer des articles de blog tech"
  ↓
Promptor exécute C1-C5 :
  🔵 STOP → Domaine "technical", 3 risques identifiés
  🟢 RECHERCHE → Standards : structure article, formats résumé
  🟡 GRILLE → Checklist binaire (longueur, ton, format)
  🔴 TRIBUNAL → Tableau Pass/Fail
  🟣 FIX → Corrections pour chaque FAIL
  ↓
Applique 18 Hacks (#3, #4, #8, #11, #18)
  ↓
Génère A-B-C-D :
  A: Calibrage (3 puces)
  B: Prompt optimisé copier-coller ready
  C: Auto-critique 4/5
  D: 2 questions pour itérer
  ↓
User itère si besoin → Prompt final 5/5
```

**Temps :** ~20-30 secondes | **Coût :** 1x

---

## 🏛️ Exemple d'Usage Council

```
User: "Crée un prompt pour modérer du contenu utilisateur [COUNCIL]"
  ↓
Promptor exécute C1-C5 → A-B-C-D
  C: Auto-critique 3/5 ("Ambiguïté sur contenus limites")
  ↓
[COUNCIL] trigger détecté → Phase 4 activée
  ↓
5 Advisors spawned en parallèle (30-60s)
  ↓
Peer review anonymisé (30-60s)
  ↓
Chairman synthesis (20-30s) :
  - Convergence : Manque guidelines cas ambigus
  - Divergence : Contrarian vs Expansionist
  - Angles morts : Jargon opaque, GDPR compliance
  - Recommandation : Matrice 10 cas concrets
  - Action immédiate : Créer specs techniques
  ↓
Artefacts générés (5s) + ouverture automatique
  ↓
Proposition intégration v2 du prompt
```

**Temps :** ~3 minutes | **Coût :** ~11x
**Valeur ajoutée :** 5 angles morts détectés vs auto-critique seule

---

## 📋 Résumé

| Aspect | Description |
|--------|-------------|
| **Type** | Meta-prompt système (instructions pour IA) |
| **Entrée** | Demande utilisateur + outil IA cible + contexte optionnel |
| **Traitement** | 5 Cercles + 18 Hacks + A-B-C-D [+ Council optionnel] |
| **Sortie** | Prompt optimisé + auto-critique + questions [+ rapport Council] |
| **Profils** | Adaptatif : débutant/intermédiaire/expert |
| **Modes** | Conversationnel, API, Collaboration |
| **Validation** | Traces JSON (v3+), Test A/B 8/10 victoires |

---

## 🆘 FAQ Rapide

**Q: Quelle version utiliser ?**
A: v3 Council Edition si vous voulez l'option audit externe. v3 standard sinon.

**Q: Le Council est-il obligatoire en v3 Council Edition ?**
A: Non, il est optionnel. Sans trigger `[COUNCIL]`, le comportement est identique à v3 standard.

**Q: Combien coûte le Council ?**
A: ~11x le coût baseline (5 advisors + 5 reviewers + 1 chairman).

**Q: Quand activer le Council ?**
A: Production critique, security/compliance, auto-critique < 3/5, première exploration domaine complexe.

---

*Documentation mise à jour le 2026-05-12 • Projet 18-Hacks-Qwen3.6-plus-Super-Promptor*
*Promptor v3 Council Edition — Prompt Engineering avec délibération multi-perspective optionnelle*
