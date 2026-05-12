# Promptor v3 Council Edition — Documentation d'Intégration

## Vue d'ensemble

Cette version étend Promptor v3 avec une **délibération LLM Council optionnelle** basée sur la méthodologie d'Andrej Karpathy. Elle combine :

- **Pipeline standard** : 5 Cercles + 18 Hacks + livraison A-B-C-D (identique à v3)
- **Council optionnel** : Audit multi-perspective par 5 advisors indépendants avec peer review aveugle

## Architecture comparative

### v3 Standard (mono-agent)

```
User Request → C1-C5 → 18 Hacks → A-B-C-D → Output
                                      ↓
                              Auto-critique 0-5
```

**Limites :**
- Même modèle = mêmes biais potentiels
- Risque de confirmation bias
- Angles morts non détectés

### v3 Council Edition (hybride)

```
User Request → C1-C5 → 18 Hacks → A-B-C-D → Output
                                      ↓
                              Auto-critique 0-5
                                      ↓
                          [COUNCIL] trigger ou proposition
                                      ↓
                    ┌─────────────────┴─────────────────┐
                    │      COUNCIL DÉLIBÉRATION         │
                    │                                   │
                    │  5 Advisors (parallèle)           │
                    │  ├─ The Contrarian                │
                    │  ├─ First Principles Thinker      │
                    │  ├─ The Expansionist              │
                    │  ├─ The Outsider                  │
                    │  └─ The Executor                  │
                    │            ↓                      │
                    │  5 Reviewers (anonymisé)          │
                    │            ↓                      │
                    │  Chairman Synthesis               │
                    │            ↓                      │
                    │  HTML Report + MD Transcript      │
                    └───────────────────────────────────┘
                                      ↓
                        Verdict + Recommandations
```

**Avantages :**
- 5 perspectives indépendantes avec styles de pensée opposés
- Détection de blind spots via peer review
- Audit objectif externe
- Synthesis par Chairman qui tranche les désaccords

**Coût :**
- Temps : +2-3 minutes
- Tokens : ~11x (5 advisors + 5 reviewers + 1 chairman)

## Fichiers créés

### 1. Meta-prompt principal

**Fichier :** `config/opencode/commands/promptor-arbre-decisionnel-consolide-v3-council.md`

**Contenu :**
- Toute la logique v3 (5 Cercles, 18 Hacks, A-B-C-D)
- Phase 4 Council ajoutée (optionnelle)
- Prompts templates pour advisors, reviewers, chairman
- Logique de framing et génération artefacts
- Arbre décisionnel mis à jour

**Taille :** ~25 KB (vs ~17 KB pour v3 standard)

### 2. Skill Claude Code

**Fichier :** `/Users/valorisa/.claude/skills/promptor-council/skill.md`

**Fonction :**
- Documentation concise pour invocation via `/promptor-council`
- Résumé architecture et workflow
- Guidelines d'utilisation (quand activer Council)
- Exemples d'utilisation

**Invocation :**
```bash
# Dans Claude Code
/promptor-council
```

### 3. Documentation intégration

**Fichier :** `COUNCIL_INTEGRATION.md` (ce fichier)

**Contenu :**
- Comparaison v3 vs v3 Council Edition
- Architecture détaillée
- Matrice décisionnelle
- Exemples d'usage
- FAQ

## Matrice décisionnelle : Quand utiliser le Council ?

| Critère | Standard (v3) | Council (v3 + Phase 4) |
|---------|---------------|------------------------|
| **Auto-critique** | >= 4/5 | < 4/5 |
| **Domaine** | Non-critique (expérimental, interne) | Critique (security, compliance, production, legal) |
| **Impact** | Faible (prototype, A/B test) | Élevé (prod, business impact) |
| **Coût acceptable** | 1x | ~11x |
| **Temps disponible** | Immédiat | +2-3 min OK |
| **Exploration** | Domaine maîtrisé | Premier prompt d'un domaine complexe |
| **Trigger** | Aucun | `[COUNCIL]` explicite ou confirmation proposition |

### Règle simple

**Utiliser Council si :**
```
(auto_critique < 4/5 ET domaine_critique) OU trigger_explicite
```

**Skip Council si :**
```
auto_critique >= 4/5 ET domaine_non_critique ET budget_contraint
```

## Les 5 Advisors — Profils détaillés

### 1. The Contrarian
**Fonction :** Chercher activement les failles, points de rupture, cas limites non couverts.

**Style de pensée :**
- "Qu'est-ce qui peut échouer ?"
- "Quel angle mort critique est invisible ici ?"
- "Si je devais casser ce prompt, comment ferais-je ?"

**Ne PAS confondre avec :** Pessimisme. Le Contrarian n'est pas contre l'idée, il teste sa robustesse.

**Exemple de sortie :**
> "Ce prompt suppose que l'utilisateur fournit toujours du contexte. Mais 40% des cas réels seront sans contexte. Le prompt crashera silencieusement en générant du générique inutilisable."

### 2. The First Principles Thinker
**Fonction :** Vérifier si la question posée est la bonne question. Décomposer à la racine.

**Style de pensée :**
- "Qu'essayons-nous réellement de résoudre ?"
- "Cette approche découle-t-elle des premiers principes ou d'une convention ?"
- "Y a-t-il une reformulation qui rendrait le problème trivial ?"

**Ne PAS confondre avec :** Philosophie abstraite. Le First Principles Thinker est pragmatique : il cherche la solution la plus simple en décomposant le problème.

**Exemple de sortie :**
> "On optimise un prompt pour 'résumer des articles'. Mais pourquoi résumer ? Si l'objectif est de décider lesquels lire, un prompt de classification (pertinent/non) serait 3x plus rapide et précis."

### 3. The Expansionist
**Fonction :** Identifier opportunités manquées, leviers sous-exploités, ce qui pourrait être plus ambitieux.

**Style de pensée :**
- "Qu'est-ce qui est sous-dimensionné ici ?"
- "Quelle opportunité adjacente manque-t-on ?"
- "Si ce prompt marchait mieux que prévu, que débloquerait-il ?"

**Ne PAS confondre avec :** Feature creep. L'Expansionist ne propose pas d'ajouter des features inutiles, il détecte les opportunités high-leverage ignorées.

**Exemple de sortie :**
> "Ce prompt génère du contenu. Mais il pourrait également structurer des métadonnées (tags, difficulty_level, target_audience) qui rendraient le contenu 10x plus réutilisable. Opportunité : ajouter 3 lignes pour débloquer un système de taxonomie."

### 4. The Outsider
**Fonction :** Réagir avec zéro contexte préalable. Détecter la curse of knowledge.

**Style de pensée :**
- "Si je débarque sans contexte, qu'est-ce qui est opaque ?"
- "Quels termes supposent une connaissance que je n'ai pas ?"
- "Où est-ce que je serais bloqué en tant que débutant ?"

**Ne PAS confondre avec :** Ignorance volontaire. L'Outsider simule le regard d'un nouvel utilisateur réel pour détecter les frictions invisibles aux experts.

**Exemple de sortie :**
> "Le prompt dit 'utilise le format canonique'. Qu'est-ce qu'un format canonique ? Si moi je ne le sais pas, 60% de vos utilisateurs non plus. Résultat : ils vont inventer leur propre interprétation et vous aurez 10 formats différents."

### 5. The Executor
**Fonction :** Évaluer l'exécutabilité réelle. "Peut-on utiliser ce prompt lundi matin ?"

**Style de pensée :**
- "Quelle est la première action concrète ?"
- "Quelles dépendances doivent exister pour que ça marche ?"
- "Combien de temps avant d'avoir un résultat utilisable ?"

**Ne PAS confondre avec :** Court-termisme. L'Executor ne dit pas "fais vite et mal", il vérifie qu'il existe un chemin d'exécution clair, pas seulement une stratégie.

**Exemple de sortie :**
> "Ce prompt nécessite un dataset pré-nettoyé. Mais qui le nettoie ? Combien de temps ça prend ? Si le dataset n'existe pas lundi, ce prompt est théorique. Manque : soit fournir le dataset, soit ajouter une étape de nettoyage au prompt."

## Tensions créées par les 5 Advisors

L'architecture Council fonctionne grâce à **3 tensions naturelles** :

### Tension 1 : Contrarian ↔ Expansionist
- **Contrarian** : "Qu'est-ce qui peut échouer ?"
- **Expansionist** : "Qu'est-ce qui pourrait être plus grand ?"
- **Résolution Chairman** : Équilibre entre robustesse et ambition

### Tension 2 : First Principles ↔ Executor
- **First Principles** : "Repensons tout depuis la base"
- **Executor** : "Qu'est-ce qu'on fait lundi matin ?"
- **Résolution Chairman** : Équilibre entre réflexion profonde et exécution rapide

### Tension 3 : Outsider (modérateur)
- **Fonction** : Garde-fou contre la complexité excessive
- **Effet** : Force les 4 autres à expliquer clairement
- **Résolution Chairman** : Si l'Outsider est perdu, le prompt est trop opaque

## Workflow détaillé Phase 4 (Council)

### Étape 1 : Framing enrichi

**Objectif :** Donner aux advisors le maximum de contexte pertinent sans les noyer.

**Actions :**
1. Collecter artefacts Promptor :
   - Prompt optimisé (sortie B)
   - Auto-critique (sortie C avec score)
   - Traces JSON C1-C5
   - DOMAIN, FOCUS_HACKS, USER_PROFILE

2. Scanner workspace (max 30 secondes) :
   ```bash
   # Ordre de priorité
   1. CLAUDE.md ou claude.md (préférences, contraintes)
   2. memory/ (audience, voice, décisions passées)
   3. Fichiers référencés explicitement
   4. Transcripts Council antérieurs (éviter redondance)
   ```

3. Framer question pour advisors :
   ```markdown
   Question soumise au Council :
   "Ce prompt est-il solide pour {{DOMAIN}} ? Identifier les faiblesses, angles morts et risques non détectés par l'auto-critique ({{score}}/5)."
   
   Context package : [voir template complet dans v3-council.md]
   ```

### Étape 2 : Convocation (5 sub-agents parallèles)

**IMPORTANT :** Spawning TOUJOURS parallèle, JAMAIS séquentiel.

```python
# Pseudo-code
spawn_parallel([
    Advisor("The Contrarian", framed_question),
    Advisor("The First Principles Thinker", framed_question),
    Advisor("The Expansionist", framed_question),
    Advisor("The Outsider", framed_question),
    Advisor("The Executor", framed_question)
])
```

**Durée :** ~30-60 secondes (parallèle)

**Output attendu :** 5 réponses indépendantes, 150-300 mots chacune

### Étape 3 : Peer Review (5 sub-agents parallèles, anonymisés)

**Anonymisation :**
```python
responses = collect_advisor_responses()
shuffled = shuffle(responses)  # Ordre aléatoire
anonymized = {
    "Response A": shuffled[0],
    "Response B": shuffled[1],
    "Response C": shuffled[2],
    "Response D": shuffled[3],
    "Response E": shuffled[4]
}
mapping = store_mapping(shuffled)  # Pour dé-anonymiser plus tard
```

**Questions aux reviewers :**
1. Quelle réponse est la plus forte ? Pourquoi ?
2. Quelle réponse a le plus gros angle mort ? Lequel ?
3. Qu'est-ce que TOUTES les réponses ont manqué ?

**Spawning parallèle :**
```python
spawn_parallel([
    Reviewer(advisor_1_context, anonymized_responses),
    Reviewer(advisor_2_context, anonymized_responses),
    Reviewer(advisor_3_context, anonymized_responses),
    Reviewer(advisor_4_context, anonymized_responses),
    Reviewer(advisor_5_context, anonymized_responses)
])
```

**Durée :** ~30-60 secondes (parallèle)

### Étape 4 : Chairman Synthesis

**Input :**
- Question framée + contexte
- 5 réponses advisors (dé-anonymisées, noms révélés)
- 5 peer reviews

**Output structure (imposée) :**
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

**Durée :** ~20-30 secondes

### Étape 5 : Génération artefacts

**HTML Report :**
- Template : Design clean, fond blanc, typo système
- Sections : Question → Verdict → Matrice → Détails (collapsé)
- Auto-ouverture : `open council-report-{{timestamp}}.html`

**Markdown Transcript :**
- Complet : Question → Advisors → Reviews → Synthesis
- Usage : Référence pour future itération ou audit

**Durée :** ~5 secondes

### Étape 6 : Livraison

**Output utilisateur :**
```markdown
🏛️ **COUNCIL DÉLIBÉRATION ACTIVÉE**

[...]

✅ **Council verdict disponible**

📄 Rapport visuel : council-report-20260512-170230.html (ouvert)
📋 Transcript complet : council-transcript-20260512-170230.md

**Résumé du verdict :**
Le Council converge sur [X]. Divergence sur [Y] : Contrarian veut [A], Expansionist préfère [B].
Angle mort détecté : [Z] (révélé par Outsider en peer review).

Recommandation : [action claire]
Action immédiate : [une chose concrète]

Veux-tu que j'intègre ces recommandations dans une v2 du prompt ?
```

## Exemples d'usage complets

### Exemple 1 : Standard (pas de Council)

**Input utilisateur :**
```
Crée un prompt pour résumer des articles de blog tech
```

**Flow :**
1. Promptor identifie : DOMAIN=technical, PROFILE=intermédiaire, FOCUS=quality
2. C1-C5 exécutés → détecte 3 risques (hallucinations, perte de nuances, formatage)
3. 18 Hacks appliqués (#4, #8, #10, #11, #18)
4. A-B-C-D générés
5. Auto-critique : 4/5 ("Bon équilibre concision/précision, manque gestion des articles très longs")

**Output :**
- Prompt optimisé (bloc copier-coller)
- Auto-critique avec suggestion ("Ajouter un paramètre max_length optionnel")
- 2 questions pour itérer

**Temps total :** ~20-30 secondes

**Coût relatif :** 1x

### Exemple 2 : Council activé (trigger explicite)

**Input utilisateur :**
```
Crée un prompt pour modérer du contenu utilisateur sur notre plateforme de forums [COUNCIL]
```

**Flow :**
1. Promptor identifie : DOMAIN=security, PROFILE=expert, FOCUS=security
2. C1-C5 exécutés → détecte 3 risques (faux positifs, contextes ambigus, évolution du langage toxique)
3. 18 Hacks appliqués (#1, #4, #9, #11, #18)
4. A-B-C-D générés
5. Auto-critique : 3/5 ("Ambiguïté sur contenus limites, pas de guidelines pour cas gris")
6. **Trigger [COUNCIL] détecté** → Phase 4 activée
7. Framing enrichi (scan CLAUDE.md → trouve politique modération existante)
8. 5 Advisors spawned :
   - Contrarian : "Laisse passer toxicité indirecte (sarcasme, dogwhistles)"
   - First Principles : "Vraie question = quel taux faux positifs/négatifs acceptable ?"
   - Expansionist : "Ajouter système confiance utilisateur (comptes établis vs nouveaux)"
   - Outsider : "Qu'est-ce qu'un 'contenu limite' ? Trop vague."
   - Executor : "Manque matrice 10 cas concrets pour modérateurs juniors"
9. Peer review → tous identifient manque d'exemples concrets
10. Chairman synthesis :
    - Convergence : Manque guidelines pour cas ambigus
    - Divergence : Contrarian veut plus règles, Expansionist veut contexte utilisateur
    - Angle mort : Jargon "contenu limite" opaque (Outsider)
    - Recommandation : Matrice "Scénario | Décision | Justification" avec 10 cas réels
    - Action immédiate : Créer tableau avec 10 lignes (harcèlement indirect, humour offensant, critique vs attaque)
11. Artefacts générés + ouverts

**Output :**
- Tout le standard +
- HTML report avec verdict complet
- Transcript MD
- Résumé Chairman
- Proposition intégration v2

**Temps total :** ~3 minutes

**Coût relatif :** ~11x

### Exemple 3 : Council proposé mais refusé

**Input utilisateur :**
```
Crée un prompt pour générer des descriptions de produits e-commerce
```

**Flow :**
1. Promptor identifie : DOMAIN=creative, PROFILE=débutant, FOCUS=speed
2. C1-C5 → 3 risques (générique, manque brand voice, SEO ignoré)
3. A-B-C-D générés
4. Auto-critique : 3/5 ("Fonctionnel mais manque personnalisation brand voice")
5. **Proposition Council** (auto-critique < 4/5) :
   > Veux-tu un audit externe par le LLM Council ? [Coût ~11x, +2-3min]
6. **Utilisateur répond :** "Non merci, je veux juste tester rapidement"
7. **Council skipped** → livraison standard

**Output :**
- Prompt optimisé
- Auto-critique avec suggestion
- Questions pour itérer

**Temps total :** ~20-30 secondes

**Coût relatif :** 1x

## Différences clés v3 vs v3 Council Edition

| Aspect | v3 Standard | v3 Council Edition |
|--------|-------------|-------------------|
| **Fichier** | `promptor-arbre-decisionnel-consolide-v3.md` | `promptor-arbre-decisionnel-consolide-v3-council.md` |
| **Taille** | ~17 KB | ~25 KB |
| **Phases** | 3 (C1-C5, Hacks, A-B-C-D) | 4 (+ Council optionnel) |
| **Validation** | Auto-critique seule | Auto-critique + Council optionnel |
| **Blind spots detection** | Limitée | Peer review aveugle + 5 perspectives |
| **Artefacts** | Prompt uniquement | Prompt + HTML + MD (si Council) |
| **Coût baseline** | 1x | 1x |
| **Coût max** | 1x | ~11x (si Council activé) |
| **Temps baseline** | ~20-30s | ~20-30s |
| **Temps max** | ~20-30s | ~3 minutes (si Council activé) |
| **Trigger Council** | N/A | `[COUNCIL]` flag ou confirmation |
| **Cas d'usage** | Tous prompts | Standard + haute criticité |
| **Architecture** | Mono-agent | Hybride (mono default, multi si Council) |
| **Chairman** | N/A | Synthesis finale multi-perspective |

## FAQ

### Quand utiliser v3 Council vs v3 standard ?

**Utiliser v3 Council si :**
- Vous travaillez sur des prompts critiques (prod, security, compliance)
- Vous voulez l'option d'audit externe sans toujours l'activer
- Vous êtes prêt à payer 11x sur certains prompts stratégiques

**Utiliser v3 standard si :**
- Tous vos prompts sont non-critiques
- Budget très contraint (pas de marge pour 11x)
- Vous n'aurez jamais besoin d'audit multi-perspective

### Le Council remplace-t-il l'auto-critique ?

**Non.** Le Council est **complémentaire** :
- **Auto-critique** : Contrôle qualité continu (100% des prompts)
- **Council** : Audit externe profond (5-10% des prompts critiques)

Le Council se déclenche **après** l'auto-critique, jamais à la place.

### Peut-on forcer le Council sur tous les prompts ?

**Techniquement oui, mais c'est déconseillé.**

Ajouter `[COUNCIL]` force l'activation, mais :
- Coût multiplié par 11 sur tous les prompts
- Temps multiplié par 6-9 (20s → 3min)
- Overhead inutile sur prompts simples

**Recommandation :** Laisser Promptor proposer le Council quand justifié (auto-critique < 4 + domaine critique).

### Comment interpréter un désaccord entre advisors ?

**Désaccord = signal précieux, pas bug.**

Exemple :
- **Contrarian** : "Cette approche a trop de points de rupture"
- **Expansionist** : "Cette approche est trop conservatrice, manque d'ambition"

**Interprétation Chairman :**
> "Le désaccord révèle un trade-off robustesse vs ambition. La recommandation dépend du contexte : si prod critique → suivre Contrarian. Si prototype exploratoire → suivre Expansionist."

Le Chairman tranche en **expliquant le contexte de décision**, pas en votant.

### Les advisors sont-ils de vrais sub-agents ou simulés ?

**Vrais sub-agents.**

Chaque advisor est un appel agent distinct avec son propre context window et instructions. Ce ne sont pas des "rôles simulés" dans un seul prompt.

**Avantage :** Vraie indépendance, pas de contamination croisée.

**Preuve :** Le peer review anonymisé ne fonctionnerait pas avec simulation (le modèle "saurait" ce qu'il a dit dans chaque rôle).

### Peut-on personnaliser les 5 advisors ?

**Pas dans v3 Council Edition actuelle.**

Les 5 advisors sont figés (Contrarian, First Principles, Expansionist, Outsider, Executor) car leur sélection découle de la méthodologie Karpathy validée.

**Future extension possible :**
- Advisors spécialisés par domaine (ex: SEO Specialist pour prompts marketing)
- Nombre d'advisors variable (3, 5, 7)
- Template advisor customisable

**Priorité actuelle :** Stabiliser l'implémentation de base avant personnalisation.

### Comment éviter le coût 11x si on veut juste un "deuxième avis" ?

**Option 1 :** Utiliser uniquement 1-2 advisors au lieu de 5

Modifier le trigger :
- `[COUNCIL:LIGHT]` → spawn uniquement Contrarian + Outsider
- Coût : ~3x au lieu de 11x
- Temps : ~1 min au lieu de 3 min

**Option 2 :** Skip peer review

Modifier le workflow :
- `[COUNCIL:FAST]` → 5 advisors, pas de peer review, Chairman direct
- Coût : ~6x au lieu de 11x
- Temps : ~1.5 min au lieu de 3 min

**Note :** Ces modes ne sont pas implémentés dans v3 Council Edition actuelle. À considérer pour v3.1.

### Le Council peut-il être utilisé hors Promptor ?

**Oui, il est portable.**

L'architecture Council (5 advisors → peer review → chairman) peut être extraite et appliquée à n'importe quelle décision/question, pas seulement des prompts.

**Exemples :**
- "Council this: Should I launch a $97 workshop or a $497 course?"
- "Council this: Which of these 3 positioning angles is strongest?"
- "Council this: I'm thinking of pivoting from X to Y. Am I crazy?"

**Référence :** Voir `llm-council-skill` de tenfoldmarc pour implémentation standalone.

## Roadmap

### v3 Council Edition 1.0 (actuel)

- [x] Intégration Council optionnel dans pipeline Promptor v3
- [x] 5 advisors fixés avec peer review aveugle
- [x] Chairman synthesis structuré
- [x] Génération artefacts (HTML report + MD transcript)
- [x] Skill Claude Code `/promptor-council`
- [x] Documentation complète

### v3 Council Edition 1.1 (futur)

- [ ] Modes Council allégés (`[COUNCIL:LIGHT]`, `[COUNCIL:FAST]`)
- [ ] Advisors spécialisés par domaine
- [ ] Matrice visual agreement/disagreement plus riche (graphique)
- [ ] Export Council verdict vers formats additionnels (PDF, Notion, etc.)
- [ ] Métriques Council (taux convergence, advisors les plus influents, etc.)

### v3 Council Edition 2.0 (vision)

- [ ] Advisors customisables (nombre, rôles, prompts)
- [ ] Council orchestration externe (hors Promptor)
- [ ] Multi-model Council (Opus vs Sonnet vs Haiku)
- [ ] Learning loop (Council apprend des décisions passées)

## Contribution

### Feedback

Pour signaler un bug, proposer une amélioration, ou partager un cas d'usage Council :

1. Ouvrir une issue sur le repo GitHub (si public)
2. Ou documenter dans `examples/council-cases/` avec structure :
   ```markdown
   # Cas : [Titre]
   
   ## Context
   [Domaine, user request, enjeux]
   
   ## Auto-critique
   [Score + commentaire]
   
   ## Verdict Council
   [Résumé convergence/divergence/angles morts]
   
   ## Impact
   [Le Council a-t-il changé le prompt final ? Comment ?]
   
   ## Leçons
   [Qu'avons-nous appris de ce Council ?]
   ```

### Tests

Pour tester l'intégration Council :

**Test 1 : Standard (pas de Council)**
```
Input : "Crée un prompt pour [tâche simple non-critique]"
Expected : C1-C5 → A-B-C-D → auto-critique >= 4/5 → pas de proposition Council
```

**Test 2 : Council proposé**
```
Input : "Crée un prompt pour [tâche critique]"
Expected : C1-C5 → A-B-C-D → auto-critique < 4/5 → proposition Council
```

**Test 3 : Council forcé**
```
Input : "Crée un prompt pour [tâche quelconque] [COUNCIL]"
Expected : C1-C5 → A-B-C-D → Phase 4 activée → artefacts générés
```

**Test 4 : Council refusé**
```
Input : "Crée un prompt pour [tâche critique]"
→ Proposition Council
Input 2 : "Non merci"
Expected : Livraison standard sans Council
```

## Licence

Même licence que Promptor v3 (voir LICENSE du repo principal).

## Crédits

- **Promptor v3** : 18 Hacks Qwen3.6+ (validation A/B aveugle 8/10 vs baseline)
- **LLM Council méthodologie** : Andrej Karpathy
- **Council implementation reference** : tenfoldmarc/llm-council-skill
- **Intégration v3 Council Edition** : valorisa (2026-05-12)

---

*Documentation créée le 2026-05-12*
*Promptor v3 Council Edition — Prompt Engineering avec délibération multi-perspective optionnelle*
