# Exemple Council : Prompt de Modération de Contenu

## Contexte

**Demande utilisateur :**
> "Créer un prompt pour modérer du contenu utilisateur sur notre plateforme de forums communautaires. Production critique. [COUNCIL]"

**Détection automatique :**
- DOMAIN : security
- USER_PROFILE : expert
- FOCUS_HACKS : security
- Trigger [COUNCIL] : explicite

---

## Phase 1-2 : Pipeline Standard (C1-C5 + 18 Hacks)

### C1 STOP — Validation

```json
{
  "circle": "C1",
  "status": "pass",
  "evidence": "Domaine security détecté, profil expert confirmé, 3 risques identifiés",
  "hacks_applied": ["#1", "#9"]
}
```

**Risques identifiés :**
1. Faux positifs élevés → perte de confiance utilisateurs
2. Faux négatifs → exposition légale (harcèlement, contenus illégaux)
3. Évolution du langage toxique (slang, codes, dogwhistles)

### C2 RECHERCHE — Standards

```json
{
  "circle": "C2",
  "status": "pass",
  "evidence": "3 patterns reconnus : Perspective API (Google), Trust & Safety best practices (Meta), EU DSA compliance",
  "hacks_applied": ["#2", "#11", "#15"]
}
```

**Benchmarks :**
- Perspective API : scoring multi-dimensionnel (toxicity, severe_toxicity, identity_attack)
- Meta Trust & Safety : gradation severity (warning, remove, ban)
- EU Digital Services Act : délais de traitement (24h contenus illégaux, 7j notifications)

### C3 GRILLE — Checklist binaire

```json
{
  "circle": "C3",
  "status": "pass",
  "evidence": "5 critères pass/fail définis avec hacks intégrés",
  "hacks_applied": ["#3", "#4", "#12", "#18"]
}
```

| Critère | Pass/Fail | Hack |
|---------|-----------|------|
| Le prompt gère-t-il les cas ambigus avec guidelines explicites ? | À tester | #11 |
| Le prompt inclut-il >= 10 exemples concrets ? | À tester | #8 |
| Le prompt définit-il des seuils de confiance clairs ? | À tester | #4 |
| Le prompt intègre-t-il un fallback humain ? | À tester | #16 |
| Le prompt est-il auditble (log des décisions) ? | À tester | #18 |

### C4 TRIBUNAL — Évaluation stricte

```json
{
  "circle": "C4",
  "status": "fail",
  "evidence": "3/5 critères en FAIL",
  "hacks_applied": ["#5", "#6", "#14"]
}
```

| Critère | Résultat | Preuve | Hack # |
|---------|----------|--------|--------|
| Guidelines cas ambigus | FAIL | Aucune mention dans USER_REQUEST | #11 |
| >= 10 exemples | FAIL | Non spécifié | #8 |
| Seuils confiance | PASS | Implicite (modération binaire) | #4 |
| Fallback humain | FAIL | Non mentionné | #16 |
| Auditabilité | PASS | Production → assume logging | #18 |

### C5 FIX — Corrections

```json
{
  "circle": "C5",
  "status": "pass",
  "evidence": "3 corrections appliquées, itération 1/3",
  "hacks_applied": ["#7", "#13", "#16"]
}
```

**Corrections :**
1. Ajouter section "Cas Limites" avec 10 scénarios
2. Intégrer matrice scoring multi-niveau (safe, review, remove, ban)
3. Définir trigger fallback humain (confidence < 0.7)

---

## Phase 3 : Livraison (A-B-C-D)

### A — Calibrage

- Logique : Scoring multi-niveau avec fallback humain pour cas ambigus
- Domaine : Security (modération contenu)
- Focus : Security hacks (#1, #9, #14, #18) + Quality (#4, #11)

### B — Prompt Optimisé

```markdown
# Prompt : Modération de Contenu Forums Communautaires

Tu es un modérateur de contenu pour une plateforme de forums. Ton rôle est d'évaluer si un message utilisateur respecte nos Community Guidelines.

## Community Guidelines (résumé)

- ✅ Autorisé : Débats respectueux, critiques constructives, humour léger
- ⚠️ Review nécessaire : Langage limite, sarcasme agressif, critique personnelle
- ❌ Interdit : Harcèlement, propos haineux, menaces, contenus illégaux, spam

## Ton Processus

Pour chaque message, évalue ces dimensions (score 0-1) :

1. **Toxicity** : Langage insultant, agressif, dégradant
2. **Harassment** : Attaque ciblée, pile-on, dogpiling
3. **Hate Speech** : Discrimination basée sur identité (race, genre, religion, etc.)
4. **Threats** : Menaces explicites ou implicites de violence
5. **Spam** : Contenu promotionnel non sollicité, répétitif

## Matrice de Décision

| Score moyen | Action | Justification |
|-------------|--------|---------------|
| 0.0 - 0.3 | SAFE | Contenu conforme, publier |
| 0.3 - 0.7 | REVIEW | Cas ambigu, escalade humaine |
| 0.7 - 0.9 | REMOVE | Violation claire, retirer + warning |
| 0.9 - 1.0 | BAN | Violation grave, ban immédiat |

## 10 Cas Limites (Guidelines)

| Scénario | Décision | Justification |
|----------|----------|---------------|
| Critique virulente d'une décision politique | SAFE | Opinion forte ≠ harcèlement si pas ciblé |
| Sarcasme agressif ("T'es vraiment un génie...") | REVIEW | Contexte nécessaire (relation users, historique) |
| Blague sur stéréotype culturel | REVIEW | Intention vs impact (humour vs offense) |
| "Tu devrais te faire soigner" (santé mentale) | REMOVE | Attaque personnelle déguisée |
| Dogwhistle raciste ("13/50") | REMOVE | Code connu de rhétorique haineuse |
| All-caps répété ("LISEZ ÇA !!! IMPORTANT !!!") | REVIEW | Spam potentiel vs urgence légitime |
| Link vers site externe sans contexte | REVIEW | Spam vs source légitime |
| "Va te faire..." (insulte tronquée) | REMOVE | Intention claire malgré censure |
| Critique nommant un modérateur | REVIEW | Feedback légitime vs harcèlement |
| Copypasta meme offensant | REVIEW | Contexte communautaire (in-joke vs attaque) |

## Output Format

Pour chaque message, retourne :

\`\`\`json
{
  "message_id": "{{ID}}",
  "scores": {
    "toxicity": 0.0-1.0,
    "harassment": 0.0-1.0,
    "hate_speech": 0.0-1.0,
    "threats": 0.0-1.0,
    "spam": 0.0-1.0
  },
  "average_score": 0.0-1.0,
  "decision": "SAFE|REVIEW|REMOVE|BAN",
  "justification": "Explication claire de la décision (1-2 phrases)",
  "confidence": 0.0-1.0,
  "escalate_human": true|false
}
\`\`\`

## Règles Critiques

1. **Si confidence < 0.7** : Force `escalate_human: true` (fallback humain obligatoire)
2. **Si contexte manquant** : Défaut vers REVIEW (principe de prudence)
3. **Si multi-violations** : Prendre la plus grave (ex: toxicity 0.4 + threats 0.9 → BAN)
4. **Logs auditables** : Toutes décisions loggées pour review mensuelle

## Variables d'entrée

- `{{MESSAGE_CONTENT}}` : Le texte du message à évaluer
- `{{USER_HISTORY}}` (optionnel) : Historique infractions de l'utilisateur
- `{{CONTEXT}}` (optionnel) : Thread parent, relation entre users

## Exemple

**Input :**
\`\`\`
MESSAGE_CONTENT: "Encore une feature buguée... les devs sont vraiment incompétents sur ce projet"
USER_HISTORY: 0 infractions
CONTEXT: Thread sur un bug récurrent
\`\`\`

**Output :**
\`\`\`json
{
  "message_id": "msg_12345",
  "scores": {
    "toxicity": 0.5,
    "harassment": 0.3,
    "hate_speech": 0.0,
    "threats": 0.0,
    "spam": 0.0
  },
  "average_score": 0.16,
  "decision": "SAFE",
  "justification": "Critique forte mais dirigée vers le produit, pas les personnes. Pas de violation si contexte = bug report légitime.",
  "confidence": 0.75,
  "escalate_human": false
}
\`\`\`
```

### C — Auto-Critique

**Score : 3/5**

**Commentaire :**
- ✅ Forces : Matrice claire, 10 cas limites, fallback humain, output structuré
- ❌ Faiblesses :
  1. Pas de gestion de l'évolution du langage toxique (nouveaux slangs, codes)
  2. Manque d'exemples de dogwhistles actualisés (liste statique datée rapidement)
  3. Aucune mention de faux positifs sur communautés niche (jargon spécifique)

**Amélioration suggérée :**
Ajouter une section "Mise à jour Guidelines" avec :
- Process de review mensuel des cas REVIEW escaladés
- Liste dynamique des dogwhistles (mise à jour communautaire)
- Whitelist jargon par communauté (ex: termes techniques gaming vs harcèlement)

**Proposition Council :**

> 💡 **Veux-tu un audit externe par le LLM Council ?**
> 
> Auto-critique à 3/5 + domaine critique (security, production) → Council recommandé.
> 
> Le Council va soumettre ce prompt à 5 advisors indépendants pour détecter angles morts et faiblesses non visibles en auto-critique.
> 
> - Coût estimé : ~11x
> - Temps : +2-3 minutes
> 
> Ajoute `[COUNCIL]` à ta prochaine réponse pour activer.

**Utilisateur :** *Trigger [COUNCIL] déjà présent dans la requête initiale → Phase 4 activée*

---

## Phase 4 : Council Délibération

### Étape 1 : Framing enrichi

**Context scan workspace (30s) :**
- ✅ Trouvé : `CLAUDE.md` → Politique modération existante (3-strike system, délais traitement 24h)
- ✅ Trouvé : `memory/audience_profile.md` → Communauté tech francophone, 18-45 ans, jargon gaming fréquent
- ❌ Pas trouvé : Transcripts Council antérieurs sur modération

**Question framée pour advisors :**

```markdown
Question soumise au Council :
"Ce prompt de modération de contenu est-il solide pour une plateforme de forums en production ? Identifier les faiblesses, angles morts et risques non détectés par l'auto-critique (3/5)."

Context package :
- Domain : security (modération contenu)
- User Profile : expert
- Focus : security
- Auto-critique score : 3/5 — "Manque gestion évolution langage toxique, dogwhistles datés, faux positifs sur jargon niche"
- Hacks appliqués : #1, #4, #8, #9, #11, #16, #18
- Risques identifiés en C1 : Faux positifs, faux négatifs, évolution slang
- Critères C3 FAIL : Guidelines cas ambigus (initialement), exemples concrets (corrigé), fallback humain (corrigé)

Politique existante (CLAUDE.md) :
- 3-strike system (warning → 7d ban → permanent)
- Délai traitement : 24h max pour contenus signalés
- Escalade vers Trust & Safety team si menace réelle

Audience (memory) :
- Communauté tech francophone
- 18-45 ans, jargon gaming fréquent ("noob", "tryhard", "FF", etc.)
- Historique faux positifs sur termes techniques ("kill process", "slave/master", etc.)

[Prompt optimisé B à auditer]
[... voir section B ci-dessus ...]
```

### Étape 2 : 5 Advisors (parallèle, 30-60s)

#### Response 1 — The Contrarian

**Score : 2.5/5 (FAIL sur robustesse)**

Ce prompt échouera sur 3 axes critiques :

1. **Dogwhistles évolutifs** : La liste "13/50" est statique. Dans 3 mois, elle sera obsolète. Les communautés haineuses mutent leur vocabulaire toutes les 6-8 semaines (ex: passage de "1488" à des variants comme "88", puis emojis 🐸). Le prompt n'a aucun mécanisme d'adaptation.

2. **Gaming du système** : Les utilisateurs malveillants vont rapidement identifier le seuil 0.7 et craft des messages à 0.69. Exemple : "Tu es clairement une personne de faible intelligence" (0.68 toxicity) vs "T'es con" (0.95). Le premier passe, le second non, alors que l'impact est identique.

3. **Context window insuffisant** : Le prompt demande `{{USER_HISTORY}}` et `{{CONTEXT}}`, mais ne spécifie pas la taille de ces inputs. Si context = 50 messages de thread, le prompt va truncate les premiers et manquer l'escalade progressive (user qui devient de plus en plus agressif sur 30 messages).

**Faille fatale :** Aucune gestion des attaques multi-comptes. Un harceleur peut spawn 10 comptes, chacun envoyant des messages à 0.5 toxicity (individuellement SAFE), mais collectivement c'est du dogpiling. Le prompt évalue message par message, jamais en cluster.

**Recommandation :** Ajouter détection pattern temporel (même cible + X messages en Y minutes) et scoring cumulatif cross-comptes (si IP/fingerprint similaire).

---

#### Response 2 — The First Principles Thinker

**Question fondamentale non posée : "Qu'est-ce qu'on essaie vraiment d'optimiser ?"**

Ce prompt assume que le goal est "détecter violations". Mais c'est faux. Le vrai goal est **maintenir une communauté saine** (retention users positifs, croissance, trust).

**Implications :**
- Un faux positif sur un contributeur actif (ban injustifié) coûte 100x plus qu'un faux négatif sur un troll (message toxique passé).
- Le prompt devrait donc intégrer `{{USER_VALUE}}` (karma, contributions, ancienneté) dans la décision.

**Exemple :**
- User A (nouveau, 0 posts) : "T'es nul" → BAN (risque faible)
- User B (5 ans, 10K karma, 0 infractions) : "T'es nul" → REVIEW + contexte (risque élevé de faux positif)

Le prompt actuel traite tous les users également. C'est une erreur de first principles.

**Autre angle :** Pourquoi séparer "modération" et "éducation" ? La vraie question est "comment transformer un comportement limite en comportement positif ?". Le prompt devrait inclure une sortie `suggested_educational_response` pour les cas REVIEW (ex: "Rappel : critiques OK, attaques personnelles non").

**Recommandation :** Reframer comme "Community Health Optimizer" plutôt que "Content Moderator". Inclure user value, intent éducatif, et coût des erreurs dans la matrice.

---

#### Response 3 — The Expansionist

**Ce prompt est sous-dimensionné. Opportunités manquées :**

1. **Sentiment analysis bidirectionnel** : Actuellement, le prompt détecte uniquement toxicity. Mais pourquoi ne pas aussi scorer positivité ? Un message avec toxicity 0.2 + helpfulness 0.9 (aide technique) devrait être boosté en visibilité, pas juste "autorisé". Le prompt rate une opportunité de surface le meilleur contenu, pas seulement filtrer le pire.

2. **Predictive escalation** : Le prompt réagit (message déjà posté). Pourquoi ne pas prédire ? Si user_history montre une escalade (scores moyens : 0.1 → 0.3 → 0.5 sur 3 derniers messages), le prochain message devrait trigger un pre-emptive warning AVANT posting : "Ton message semble agressif. Révise avant de poster."

3. **Community-specific calibration** : Le prompt est universel. Mais chaque sous-forum a sa propre culture. Le jargon gaming ("rekt", "pwned") est safe dans r/gaming, toxique dans r/support. Le prompt devrait accepter `{{COMMUNITY_ID}}` et ajuster seuils dynamiquement.

4. **Meta-learning loop** : Chaque décision REVIEW escaladée devient training data. Après 1000 reviews, le prompt pourrait auto-améliorer ses seuils via feedback humain. Manque : aucun hook pour "learn from escalations".

**Biggest missed opportunity :** Ce prompt pourrait générer des **insights produit**. Les patterns de toxicity révèlent des pain points (ex: spike toxicity sur feature X = UX frustrant). Le prompt devrait output un `product_signal` pour PM team.

**Recommandation :** Étendre vers "Community Intelligence System" : modération + insights + éducation + prédiction.

---

#### Response 4 — The Outsider

**Je ne sais pas ce qu'est un "dogwhistle". Le prompt dit :"Dogwhistle raciste ('13/50')" comme si c'était évident. Ça ne l'est pas.**

Si moi, lecteur externe, je ne comprends pas, un modérateur junior dans 6 mois ne comprendra pas non plus. Résultat : il va skip cette règle ou la mal appliquer.

**Autres termes opaques :**
- "Pile-on" / "dogpiling" : Pas défini. Est-ce que 3 personnes qui critique la même chose = dogpiling ? Ou faut-il 10 ? 50 ?
- "Contexte communautaire (in-joke vs attaque)" : Comment un modérateur distingue-t-il ? Pas d'exemple concret.
- "Copypasta meme offensant" : Qu'est-ce qu'un copypasta ? Pourquoi est-ce parfois OK, parfois pas ?

**Le prompt suppose un niveau d'expertise que les utilisateurs n'ont pas.**

Autre point : le tableau "10 Cas Limites" utilise des scénarios réalistes, mais les justifications sont trop courtes. "Intention vs impact" ne dit pas COMMENT évaluer l'intention. Un modérateur humain va être bloqué.

**Test du "nouvel arrivant" :**
Si je donne ce prompt à quelqu'un qui n'a jamais fait de modération, peut-il l'utiliser immédiatement ? Non. Il va devoir googler 5-6 termes et improviser sur les cas ambigus.

**Recommandation :** Ajouter un glossaire avec définitions + exemples visuels. Transformer chaque ligne du tableau cas limites en mini-guide (3-4 phrases au lieu d'une).

---

#### Response 5 — The Executor

**Question : Peut-on utiliser ce prompt lundi matin en production ?**

**Réponse : Non. Bloqueurs :**

1. **Variables d'entrée non spécifiées** : Le prompt demande `{{USER_HISTORY}}` et `{{CONTEXT}}`, mais d'où viennent ces données ? Quel format ? Quelle API ? Si je suis un backend dev qui doit implémenter ça, je suis bloqué. Manque : specs techniques (JSON schema, API endpoints, rate limits).

2. **Performance non adressée** : Latence acceptable ? Si scoring = 500ms par message et on a 1000 messages/minute, le système crash. Manque : fallback fast-path (ex: si message < 50 chars, skip scoring complet, juste keyword match).

3. **Output non intégrable** : Le prompt retourne du JSON. OK. Mais où va ce JSON ? Qui le consomme ? Quelle action automatique est triggerée ? Manque : workflow complet (JSON → Queue → Action service → Notification user → Log audit).

4. **Rollback strategy absente** : Si le prompt génère un spike de faux positifs (ex: mise à jour change behavior), comment rollback ? Manque : versioning prompt + A/B testing setup + kill switch.

5. **Monitoring non défini** : Quelles métriques track-on ? Faux positifs rate ? Latence ? Escalation rate ? Manque : dashboard metrics + alertes (ex: si escalation_rate > 20%, page oncall).

**Le prompt est une spec fonctionnelle, pas une implémentation prête.**

Pour le rendre exécutable lundi :
1. Définir API contract (OpenAPI spec)
2. Ajouter performance budget (p95 latency < 200ms)
3. Créer integration tests (50 messages labellisés)
4. Setup monitoring (Datadog dashboard)
5. Documenter rollback procedure

**Temps estimé dev → prod : 2-3 sprints (4-6 semaines), pas "prêt lundi".**

---

### Étape 3 : Peer Review (anonymisé, 30-60s)

**Anonymisation :**
- Response A : The Executor
- Response B : The First Principles Thinker
- Response C : The Contrarian
- Response D : The Expansionist
- Response E : The Outsider

#### Reviewer 1 (The Contrarian reviews others)

1. **Réponse la plus forte : Response B (First Principles)**
   - Pourquoi : Seule à questionner l'objectif fondamental ("maintenir communauté saine" vs "détecter violations"). Change la frame entière.

2. **Plus gros angle mort : Response D (Expansionist)**
   - Quoi : Suggère plein d'extensions (positivité, prédiction, meta-learning) mais ignore complètement les risques de complexité. Ajouter 5 features = 5x plus de surface d'attaque et bugs.

3. **Toutes les réponses ont manqué : La dimension légale**
   - GDPR : Le prompt log des décisions contenant potentiellement des données sensibles (ex: message = insulte raciste). Qui a accès aux logs ? Combien de temps on garde ? Droit à l'oubli ?
   - EU DSA : Obligation de transparence sur les décisions de modération. Le prompt doit retourner `appealable: true/false` et `appeal_instructions`.

---

#### Reviewer 2 (First Principles reviews others)

1. **Réponse la plus forte : Response C (Contrarian)**
   - Pourquoi : Identifie les 3 failles techniques les plus critiques (dogwhistles statiques, gaming du système, attaques multi-comptes). Concrètes et actionnables.

2. **Plus gros angle mort : Response E (Outsider)**
   - Quoi : Juste critique le jargon, mais ne propose aucune solution alternative. "Ajouter glossaire" est lazy. Le vrai problème est que le prompt assume trop de contexte. Il faut le réécrire plus simple, pas juste ajouter une doc à côté.

3. **Toutes les réponses ont manqué : Le coût humain du fallback**
   - Chaque décision REVIEW escaladée = charge cognitive pour un humain. Si 30% des messages vont en REVIEW, l'équipe Trust & Safety va crouler. Aucune réponse ne quantifie le volume attendu d'escalations ni propose de filtrage pré-escalade.

---

#### Reviewer 3 (Expansionist reviews others)

1. **Réponse la plus forte : Response D (moi-même, mais je dois choisir une autre... donc Response A — Executor)**
   - Pourquoi : Seule réponse qui pense "implémentation réelle". Les autres parlent de "ce qui devrait être", l'Executor parle de "ce qui bloque la mise en prod".

2. **Plus gros angle mort : Response B (First Principles)**
   - Quoi : Suggère d'intégrer `{{USER_VALUE}}` dans les décisions. Mais ça crée un système à deux vitesses : users VIP (anciens) vs users jetables (nouveaux). Risque de backlash communautaire ("les mods protègent leurs copains"). Dimension éthique ignorée.

3. **Toutes les réponses ont manqué : L'échelle internationale**
   - Le prompt est en anglais, détecte du contenu potentiellement multilingue (français dans memory/audience), mais ne mentionne jamais la langue. Comment scorer toxicity en français ? En arabe ? Les seuils sont-ils universels ? Grosse lacune.

---

#### Reviewer 4 (Outsider reviews others)

1. **Réponse la plus forte : Response E (moi-même, mais non... donc Response C — Contrarian)**
   - Pourquoi : Parce que c'est la seule que j'ai vraiment comprise sans relire 3 fois. Concrète, exemples clairs, pas de jargon.

2. **Plus gros angle mort : Response D (Expansionist)**
   - Quoi : Trop d'idées, impossible à suivre. "Community Intelligence System", "predictive escalation", "meta-learning loop" — c'est quoi concrètement ? Si moi je suis perdu, un PM qui doit prioriser va abandonner.

3. **Toutes les réponses ont manqué : La documentation utilisateur**
   - Les 5 réponses parlent toutes côté tech/modération. Mais qu'est-ce que les users voient quand leur message est retiré ? Un simple "Ton message viole nos règles" ? Ou une explication détaillée ? Le prompt ne produit rien de user-facing, juste du backend.

---

#### Reviewer 5 (Executor reviews others)

1. **Réponse la plus forte : Response A (moi-même... OK Response C — Contrarian)**
   - Pourquoi : Identifie des bugs exploitables (gaming seuil 0.7, attaques multi-comptes). Critique qui rend le prompt immédiatement meilleur si appliquée.

2. **Plus gros angle mort : Response B (First Principles)**
   - Quoi : Belle philosophie ("Community Health Optimizer"), mais zéro path d'exécution. Comment on mesure "community health" ? Quelle baseline ? Quel target ? C'est du hand-waving.

3. **Toutes les réponses ont manqué : La charge de maintenance**
   - Ce prompt va demander des updates constants (dogwhistles, cas limites, seuils). Qui maintient ? Quelle cadence ? Le prompt devrait inclure un `last_updated` timestamp et un process de review mensuel obligatoire.

---

### Étape 4 : Chairman Synthesis

#### Où le Council Converge (Haute Confiance)

Trois points d'accord multi-advisors émergent :

1. **Le prompt actuel est sous-spécifié pour une mise en production** (Contrarian, Executor)
   - Variables d'entrée non définies techniquement
   - Performance et latence non adressées
   - Workflow complet (input → output → action) manquant

2. **La gestion des cas limites est insuffisante** (Contrarian, Outsider, Executor)
   - Dogwhistles statiques vont dater rapidement
   - Termes opaques (pile-on, copypasta) non définis
   - Gaming du système (messages craftés à 0.69 toxicity) non anticipé

3. **Le prompt ne considère pas l'évolution temporelle** (Contrarian, Expansionist)
   - Pas de détection pattern multi-messages (escalade progressive)
   - Pas de mécanisme d'apprentissage des escalations humaines
   - Pas de maintenance process (updates dogwhistles, seuils)

#### Où le Council Diverge (Tensions Productives)

**Tension 1 : Simplicité vs Ambition**
- **Contrarian + Executor** : "Réduire la scope, fixer les bugs critiques, ship vite"
- **Expansionist + First Principles** : "Élargir la vision, penser long-terme, construire un système complet"

**Résolution Chairman :** Les deux ont raison, mais pour des phases différentes.
- **Phase 1 (MVP, 2 semaines)** : Suivre Contrarian/Executor → fixer bugs critiques, specs techniques, mise en prod minimale
- **Phase 2 (Expansion, 3 mois)** : Suivre Expansionist/First Principles → ajout scoring positivité, prédiction, meta-learning

**Tension 2 : Égalité vs Contexte**
- **First Principles** : "Intégrer user value (karma, ancienneté) dans décisions"
- **Expansionist** : "Risque de système à deux vitesses, backlash éthique"

**Résolution Chairman :** Compromis = utiliser user value uniquement pour **ajuster le seuil du fallback humain**, pas la décision finale.
- User nouveau (0 karma) : escalade si confidence < 0.7
- User établi (5K karma) : escalade si confidence < 0.5 (plus de marge d'erreur tolérée)
→ Réduit faux positifs sur contributeurs actifs sans créer de privilèges visibles.

#### Angles Morts Détectés (Émergence Peer Review)

Trois découvertes critiques via peer review :

1. **Dimension légale GDPR/DSA** (Reviewer 1 — Contrarian)
   - Logs contiennent données sensibles → durée rétention ? Accès ? Droit à l'oubli ?
   - EU DSA : obligation transparence → ajouter `appealable` + `appeal_instructions` dans output

2. **Coût humain des escalations** (Reviewer 2 — First Principles)
   - Si 30% messages → REVIEW, équipe Trust & Safety surchargée
   - Manque : quantification volume attendu + pré-filtrage avant escalade humaine

3. **Échelle multilingue** (Reviewer 3 — Expansionist)
   - Prompt en anglais, audience francophone (memory), contenu potentiellement multilingue
   - Comment scorer toxicity en français/arabe/chinois ? Seuils universels ou par langue ?

#### Recommandation Finale

**Position Chairman :** Ce prompt est une **bonne base fonctionnelle**, mais pas prêt pour production critique.

**Verdict :** Implémenter en 2 phases.

**Phase 1 — MVP Production-Ready (Priorité : Contrarian + Executor)**

Objectif : Version minimale viable, déployable en 2 semaines.

Actions :
1. **Specs techniques complètes** (Executor)
   - Définir API contract (OpenAPI spec)
   - JSON schema pour `{{USER_HISTORY}}`, `{{CONTEXT}}`
   - Performance budget : p95 latency < 200ms
   - Setup monitoring : faux positifs rate, escalation rate, latency

2. **Fixer bugs critiques** (Contrarian)
   - Anti-gaming : ajouter variance aléatoire ±0.05 aux seuils (empêche craft précis 0.69)
   - Détection multi-comptes : flag si N messages (N ≥ 3) sur même cible en T minutes (T ≤ 10)
   - Dogwhistles dynamiques : externaliser liste dans config JSON, update mensuel

3. **Clarification jargon** (Outsider)
   - Glossaire intégré avec définitions 2-3 phrases
   - Exemples visuels pour chaque cas limite (Before/After)

4. **Conformité légale** (Reviewer 1)
   - Ajouter dans output : `appealable`, `appeal_instructions`, `data_retention_days`
   - GDPR : anonymiser logs après 90 jours

**Phase 2 — Expansion Intelligence (Priorité : First Principles + Expansionist)**

Objectif : Transformation vers Community Intelligence System (3-6 mois).

Actions :
1. **Scoring bidirectionnel** (Expansionist)
   - Ajouter dimension `helpfulness`, `constructiveness`
   - Messages high-help + low-toxicity → boost visibilité

2. **User value contextuel** (First Principles)
   - Intégrer karma/ancienneté pour ajuster seuil fallback humain uniquement
   - Pas de privilèges visibles, juste tolérance erreur

3. **Prédiction escalade** (Expansionist)
   - Si user_history montre trend (0.1 → 0.3 → 0.5), pre-emptive warning avant post

4. **Meta-learning** (Expansionist)
   - Pipeline feedback : escalations humaines → training data → auto-ajustement seuils
   - Review mensuel automatique : "Top 10 faux positifs" pour calibration

5. **Multilingue** (Reviewer 3)
   - Détection langue automatique
   - Seuils ajustés par langue (toxicity français ≠ anglais)

#### Action Immédiate (Une Chose)

**Créer un document "Specs Techniques v1.0" avant d'itérer le prompt.**

**Contenu minimum :**
- API contract (OpenAPI YAML)
- JSON schemas pour inputs/output
- Performance requirements (latency, throughput)
- Monitoring metrics (5-7 KPIs)
- Rollback procedure
- Maintenance schedule (dogwhistles, seuils)

**Pourquoi cette action en premier :**
Sans specs techniques, toute itération du prompt reste théorique. Avec les specs, on peut implémenter, tester, mesurer, et itérer sur des données réelles au lieu de débattre dans l'abstrait.

**Owner :** Backend lead + Trust & Safety lead
**Deadline :** 3 jours
**Bloquant pour :** Toute mise en prod

---

### Étape 5-6 : Artefacts + Livraison

**Fichiers générés :**
- `council-report-20260512-170230.html` (ouvert automatiquement)
- `council-transcript-20260512-170230.md`

**Résumé livré à l'utilisateur :**

```
🏛️ **COUNCIL DÉLIBÉRATION ACTIVÉE**

[...]

✅ **Council verdict disponible**

📄 Rapport visuel : council-report-20260512-170230.html (ouvert)
📋 Transcript complet : council-transcript-20260512-170230.md

**Résumé du verdict :**

Le Council converge sur 3 points : (1) prompt sous-spécifié pour prod (manque specs techniques), (2) gestion cas limites insuffisante (dogwhistles statiques, gaming système), (3) pas d'évolution temporelle (maintenance, learning).

Divergence productive : Contrarian+Executor veulent MVP rapide vs Expansionist+First Principles veulent vision long-terme. Résolution : 2 phases (MVP 2 semaines → Expansion 3-6 mois).

Angles morts détectés : GDPR/DSA compliance (logs sensibles, appealability), coût humain escalations (si 30% REVIEW → surcharge), multilingue (scorer toxicity français ≠ anglais).

**Recommandation :** Implémenter en 2 phases. Phase 1 = production-ready MVP (specs techniques, bugs critiques, conformité). Phase 2 = Community Intelligence System (scoring bidirectionnel, prédiction, meta-learning).

**Action immédiate :** Créer doc "Specs Techniques v1.0" (API contract, schemas, performance, monitoring, rollback) avant toute itération prompt. Owner : Backend + T&S leads. Deadline : 3 jours.

Veux-tu que j'intègre les recommandations Phase 1 du Council dans une v2 du prompt ?
```

---

## Impact Council

### Changements vs auto-critique seule

**Auto-critique (3/5) a détecté :**
- Manque gestion évolution langage toxique
- Dogwhistles datés
- Faux positifs sur jargon niche

**Council a révélé en plus :**
1. **Bugs exploitables** (Contrarian) : Gaming seuil 0.7, attaques multi-comptes
2. **Reframe fondamental** (First Principles) : "Community health" vs "détection violations" change tout
3. **Bloqueurs prod** (Executor) : Specs techniques absentes, 4-6 semaines dev nécessaires
4. **Dimensions légales** (Peer Review) : GDPR, EU DSA compliance manquantes
5. **Échelle multilingue** (Peer Review) : Prompt anglais, audience multilingue, seuils par langue nécessaires

**Verdict :** Sans Council, le prompt aurait été itéré en surface (ajout glossaire dogwhistles). Avec Council, on découvre qu'il manque **une couche infrastructure complète** (specs, monitoring, conformité) et qu'il faut **2 phases de développement** (MVP → Expansion).

### Temps et coût

- **Temps total :** ~3 minutes (vs 20-30s standard)
- **Coût relatif :** ~11x (5 advisors + 5 reviewers + 1 chairman)
- **Valeur ajoutée :** Détection de 5 angles morts critiques qui auraient causé des incidents en production

**ROI :** Éviter un seul incident GDPR (amende 4% revenu annuel) ou un spike faux positifs (churn users VIP) justifie 100x le coût du Council.

---

## Leçons de ce cas

1. **Council est le plus utile quand auto-critique est moyenne (2-4/5)**
   - Auto-critique 5/5 : Council confirme, faible valeur ajoutée
   - Auto-critique 0-1/5 : Prompt cassé, fixer d'abord, Council après
   - **Auto-critique 2-4/5 : sweet spot** → Council révèle angles morts non-évidents

2. **Les tensions entre advisors créent de la valeur**
   - Contrarian vs Expansionist = robustesse vs ambition
   - First Principles vs Executor = vision vs exécution
   - Les désaccords forcent la clarification des trade-offs

3. **Le peer review détecte ce que les advisors manquent individuellement**
   - GDPR/DSA compliance : aucun advisor ne l'a mentionné directement
   - Émergé uniquement quand Reviewer 1 a comparé les 5 réponses et vu la lacune commune

4. **Le Chairman ne doit PAS chercher consensus mou**
   - Mauvais : "Les deux approches ont des mérites, à vous de choisir"
   - Bon : "Phase 1 = approche X, Phase 2 = approche Y, voici pourquoi"

5. **L'action immédiate doit être blocante et ungating**
   - "Créer specs techniques" est blocant → rien ne se passe tant que c'est pas fait
   - Ungate le reste du travail → une fois fait, toutes les autres actions deviennent possibles

---

*Exemple généré le 2026-05-12*
*Promptor v3 Council Edition — Cas d'usage : Modération de contenu en production*
