# 🗺️ Roadmap Promptor v3.2

**Version actuelle :** v3.1 (2026-05-12)  
**Version cible :** v3.2  
**Timeline estimé :** Q3 2026  
**Priorité :** Moyenne (amélioration progressive)

---

## 📋 Vue d'Ensemble

La v3.2 vise à **optimiser le Council** pour le rendre plus flexible et accessible dans différents contextes d'usage :
- **Modes allégés** : Réduire coût/temps pour audits moins critiques
- **Advisors spécialisés** : Expertise domain-specific (security, legal, UX, etc.)
- **Métriques Council** : Analytics pour comprendre patterns de convergence/divergence

---

## 🎯 Features Proposées

### 1. Modes Council Allégés

#### 1.1 Mode `[COUNCIL:LIGHT]` 

**Objectif :** Audit rapide avec coût réduit (~3x au lieu de ~11x)

**Architecture :**
```
2 Advisors seulement (au lieu de 5)
├─ The Contrarian : Cherche les failles
└─ The Outsider : Détecte jargon opaque

Peer Review : SKIP
Chairman Synthesis : Simplifié (convergence + 1 recommandation)

Coût relatif : ~3x
Temps : ~1 min (vs ~3 min)
```

**Quand utiliser :**
- Prompt non production-critical mais domaine sensible
- Budget/temps très contraint
- Itération rapide avec validation minimale

**Trigger :**
```
Crée un prompt pour [tâche] [COUNCIL:LIGHT]
```

**Output :**
- Pas de HTML report (Markdown only)
- 2 réponses advisors + chairman simplifié
- Verdict binaire : "Améliorations recommandées" ou "Acceptable en l'état"

---

#### 1.2 Mode `[COUNCIL:FAST]`

**Objectif :** Council complet mais sans peer review (~6x au lieu de ~11x)

**Architecture :**
```
5 Advisors (complet)
├─ The Contrarian
├─ First Principles Thinker
├─ The Expansionist
├─ The Outsider
└─ The Executor

Peer Review : SKIP (économie ~40% temps)
Chairman Synthesis : Complet

Coût relatif : ~6x
Temps : ~1.5 min (vs ~3 min)
```

**Quand utiliser :**
- Prompt production-critical mais deadline serrée
- Besoin 5 perspectives mais pas peer review
- Budget modéré

**Trigger :**
```
Crée un prompt pour [tâche critique] [COUNCIL:FAST]
```

**Output :**
- HTML report complet (sans section peer review)
- 5 réponses advisors + chairman synthesis
- Artefacts standards (HTML + MD)

---

### 2. Advisors Spécialisés par Domaine

#### Concept

Remplacer un advisor généraliste par un **expert domain-specific** quand le contexte le justifie.

#### 2.1 Mode `[COUNCIL:SECURITY]`

**Advisor remplacé :** The Expansionist → Security Expert

**Profil Security Expert :**
```markdown
Tu es **The Security Expert** dans un LLM Council.

**Ton expertise :** OWASP Top 10, threat modeling, secure by design, zero-trust architecture.

**Ton angle d'audit :**
- Surfaces d'attaque exploitables (injection, XSS, CSRF, etc.)
- Compliance frameworks (ISO 27001, SOC 2, GDPR Article 32)
- Defense in depth : missing security layers
- Secrets management, authentication, authorization
- Logging/monitoring pour détection incidents

**Ta question clé :** "Si j'étais un attaquant, comment je contournerais ce prompt ?"
```

**Quand utiliser :**
- Prompt pour système de sécurité (auth, scoring risque, modération)
- Domaine SECURITY détecté en C1
- Compliance security stricte requise

**Trigger :**
```
Crée un prompt pour [système security] [COUNCIL:SECURITY]
```

**Council composition :**
- The Contrarian
- First Principles Thinker
- **Security Expert** (remplace Expansionist)
- The Outsider
- The Executor

---

#### 2.2 Mode `[COUNCIL:LEGAL]`

**Advisor remplacé :** The Executor → Compliance Expert

**Profil Compliance Expert :**
```markdown
Tu es **The Compliance Expert** dans un LLM Council.

**Ton expertise :** RGPD, CCPA, HIPAA, Bâle III, EU AI Act, directives sectorielles.

**Ton angle d'audit :**
- Conformité réglementaire explicite (articles, obligations)
- Droit à l'explication, droit d'opposition, droit oubli
- Responsabilité légale (qui est accountable ?)
- Auditabilité et traçabilité forensique
- Procédures contestation/recours
- Documentation obligatoire (DPIA, registre traitements)

**Ta question clé :** "Face à un audit régulateur, quelles preuves manquent ?"
```

**Quand utiliser :**
- Prompt pour domaine régulé (finance, santé, RH)
- Domaine LEGAL/COMPLIANCE détecté en C1
- Risque sanctions élevé

**Trigger :**
```
Crée un prompt pour [système compliance] [COUNCIL:LEGAL]
```

**Council composition :**
- The Contrarian
- First Principles Thinker
- The Expansionist
- The Outsider
- **Compliance Expert** (remplace Executor)

---

#### 2.3 Mode `[COUNCIL:UX]`

**Advisor remplacé :** The Outsider → UX Specialist

**Profil UX Specialist :**
```markdown
Tu es **The UX Specialist** dans un LLM Council.

**Ton expertise :** User research, accessibility (WCAG), cognitive load, mental models, error states.

**Ton angle d'audit :**
- Compréhensibilité pour utilisateur final (pas dev/ops)
- Accessibility (screen readers, vision impairments)
- Error handling : messages d'erreur exploitables ?
- Onboarding : utilisateur débutant peut-il utiliser seul ?
- Charge cognitive : trop d'options/informations ?
- Feedback loops : utilisateur sait-il ce qu'il se passe ?

**Ta question clé :** "Si ma grand-mère utilisait ce prompt, que se passerait-il ?"
```

**Quand utiliser :**
- Prompt client-facing (chatbot, assistant)
- Interface conversationnelle grand public
- Accessibilité requise

**Trigger :**
```
Crée un prompt pour [interface utilisateur] [COUNCIL:UX]
```

**Council composition :**
- The Contrarian
- First Principles Thinker
- The Expansionist
- **UX Specialist** (remplace Outsider)
- The Executor

---

### 3. Métriques Council

#### Objectif

Analyser les patterns de convergence/divergence pour :
- Identifier advisors les plus influents
- Détecter domaines où Council apporte le plus de valeur
- Optimiser composition Council (quels advisors garder ?)

#### 3.1 Métriques par Session

**À logger après chaque Council :**

```json
{
  "session_id": "UUID",
  "timestamp": "ISO8601",
  "domain": "security|legal|technical|...",
  "auto_critique_score": 0-5,
  "council_mode": "FULL|LIGHT|FAST|SECURITY|LEGAL|UX",
  "advisors": ["Contrarian", "FirstPrinciples", ...],
  "metrics": {
    "convergence_areas": 3,
    "divergence_areas": 2,
    "blind_spots_detected": 5,
    "chairman_verdict": "DEPLOYABLE|NOT_DEPLOYABLE|CONDITIONAL",
    "user_accepted_recommendations": true|false
  },
  "cost_relative": 11.2,
  "duration_seconds": 180,
  "artifacts_generated": ["report.html", "transcript.md"]
}
```

#### 3.2 Dashboard Analytics

**Métriques agrégées (mensuel) :**

1. **Taux utilisation Council**
   - % prompts avec auto-critique < 4/5 qui activent Council
   - Trigger user explicite vs auto-proposition acceptée

2. **Distribution modes**
   - FULL : X%
   - LIGHT : Y%
   - FAST : Z%
   - Spécialisés (SECURITY, LEGAL, UX) : W%

3. **Advisors les plus influents**
   - Qui est le plus cité par Chairman dans recommandations finales ?
   - Qui détecte le plus d'angles morts uniques ?

4. **Domaines à forte valeur ajoutée**
   - Domaines où Council détecte > 5 angles morts : security, legal, finance
   - Domaines où Council détecte < 2 angles morts : creative, generic

5. **ROI Council**
   - Nombre incidents évités (estimé via user feedback)
   - Coût Council vs coût incident moyen

#### 3.3 Visualisation

**Graphiques proposés :**

- **Heatmap Convergence/Divergence** : 5x5 matrix (advisors vs advisors)
- **Timeline Blind Spots** : Quels angles morts détectés au fil du temps (learning curve)
- **Pareto Chart** : 80% valeur Council vient de 20% advisors ?

---

## 🛠️ Implémentation Technique

### Phase 1 : Modes Allégés (Priorité Haute)

**Effort estimé :** 1-2 semaines

**Modifications requises :**

1. **Meta-prompt (`promptor-arbre-decisionnel-consolide-v3-council.md`)**
   - Ajouter détection flags `[COUNCIL:LIGHT]`, `[COUNCIL:FAST]`
   - Adapter Phase 4 Étape 2 : 2 advisors si LIGHT, 5 si FAST
   - Adapter Phase 4 Étape 3 : Skip peer review si LIGHT ou FAST
   - Adapter Phase 4 Étape 4 : Chairman simplifié si LIGHT

2. **Artefacts**
   - LIGHT : Markdown only (pas de HTML)
   - FAST : HTML sans section peer review

**Tests validation :**
- Régénérer prompt scoring crédit avec `[COUNCIL:LIGHT]` : attendu 2 advisors, ~1 min, ~3x coût
- Régénérer prompt scoring crédit avec `[COUNCIL:FAST]` : attendu 5 advisors, ~1.5 min, ~6x coût

---

### Phase 2 : Advisors Spécialisés (Priorité Moyenne)

**Effort estimé :** 2-3 semaines

**Modifications requises :**

1. **Meta-prompt**
   - Ajouter détection flags `[COUNCIL:SECURITY]`, `[COUNCIL:LEGAL]`, `[COUNCIL:UX]`
   - Créer 3 nouveaux profils advisors (Security Expert, Compliance Expert, UX Specialist)
   - Adapter Phase 4 Étape 2 : Substituer advisor selon flag

2. **Documentation**
   - Ajouter section "Advisors Spécialisés" dans COUNCIL_INTEGRATION.md
   - Exemples d'usage pour chaque mode

**Tests validation :**
- Test SECURITY : Prompt système d'authentification → Security Expert doit détecter OWASP Top 10
- Test LEGAL : Prompt RH (recrutement) → Compliance Expert doit détecter discrimination/RGPD
- Test UX : Prompt chatbot support client → UX Specialist doit détecter accessibility/cognitive load

---

### Phase 3 : Métriques Council (Priorité Basse)

**Effort estimé :** 3-4 semaines

**Modifications requises :**

1. **Logging système**
   - Créer `council-sessions.jsonl` (append-only log)
   - Logger métrique JSON après chaque session Council

2. **Dashboard**
   - Script Python d'analyse : `analyze_council_metrics.py`
   - Génération rapport mensuel (Markdown + charts)
   - Optionnel : Dashboard web (Streamlit/Dash)

3. **Feedback loop**
   - Ajouter question post-Council : "Le Council a-t-il évité un incident ?"
   - Tracker user acceptance des recommandations

**Tests validation :**
- Simuler 50 sessions Council (replay historique)
- Vérifier métriques agrégées cohérentes

---

## 📊 Matrice Priorisation

| Feature | Impact | Effort | ROI | Priorité |
|---------|--------|--------|-----|----------|
| **LIGHT mode** | Élevé (accessibilité) | Faible | Très élevé | 🟢 P0 |
| **FAST mode** | Moyen (deadline serrée) | Faible | Élevé | 🟢 P0 |
| **SECURITY mode** | Élevé (domaine critique) | Moyen | Élevé | 🟡 P1 |
| **LEGAL mode** | Élevé (domaine critique) | Moyen | Élevé | 🟡 P1 |
| **UX mode** | Moyen (niche) | Moyen | Moyen | 🟡 P2 |
| **Métriques Council** | Faible (analytics) | Élevé | Faible | 🔴 P3 |

**Recommandation :** Implémenter dans l'ordre P0 → P1 → P2 → P3.

---

## 🧪 Critères de Succès v3.2

### Modes Allégés

✅ **LIGHT mode** :
- Coût < 4x baseline
- Temps < 90s
- 2 advisors + chairman simplifié
- User satisfaction ≥ 70% (sondage post-usage)

✅ **FAST mode** :
- Coût < 7x baseline
- Temps < 120s
- 5 advisors sans peer review
- Qualité verdict ≥ 80% vs mode FULL (comparaison aveugle)

### Advisors Spécialisés

✅ **SECURITY mode** :
- Security Expert détecte ≥ 3 angles morts OWASP sur 10 tests
- User feedback "plus pertinent que Expansionist" ≥ 70%

✅ **LEGAL mode** :
- Compliance Expert détecte ≥ 2 gaps réglementaires sur 10 tests
- Conformité validée par juriste externe ≥ 80%

✅ **UX mode** :
- UX Specialist détecte ≥ 2 problèmes accessibilité sur 10 tests
- WCAG compliance améliorée ≥ 60%

### Métriques Council

✅ **Logging** :
- 100% sessions Council loggées dans council-sessions.jsonl
- Aucune perte de données sur 100 sessions

✅ **Analytics** :
- Rapport mensuel généré automatiquement
- Dashboard accessible via localhost:8501 (Streamlit)
- Métriques exploitables pour décisions roadmap v3.3

---

## 🔄 Migration v3.1 → v3.2

### Pour utilisateurs

**Aucune action requise.** v3.2 est rétrocompatible :
- Mode FULL (défaut) reste inchangé
- Nouveaux modes disponibles via flags optionnels
- Prompts générés avec v3.1 restent valides

### Pour intégrateurs

Si vous utilisez le meta-prompt directement :
1. Mettre à jour vers v3.2 (chemin : `config/opencode/commands/promptor-arbre-decisionnel-consolide-v3-council.md`)
2. Vérifier gestion nouveaux flags : `[COUNCIL:LIGHT]`, `[COUNCIL:FAST]`, `[COUNCIL:SECURITY]`, `[COUNCIL:LEGAL]`, `[COUNCIL:UX]`
3. Optionnel : Activer logging métriques (créer `council-sessions.jsonl`)

---

## 📅 Timeline Estimé

```
Q3 2026
├─ Semaine 1-2 : P0 (Modes LIGHT + FAST)
│  ├─ Implémentation meta-prompt
│  ├─ Tests validation (10 prompts)
│  └─ Documentation COUNCIL_INTEGRATION.md

├─ Semaine 3-5 : P1 (Advisors SECURITY + LEGAL)
│  ├─ Création profils advisors
│  ├─ Tests validation (20 prompts : 10 security, 10 legal)
│  └─ Documentation exemples d'usage

├─ Semaine 6-7 : P2 (Advisor UX)
│  ├─ Création profil UX Specialist
│  ├─ Tests validation (10 prompts chatbot/interface)
│  └─ Documentation

└─ Semaine 8-11 : P3 (Métriques Council)
   ├─ Logging système
   ├─ Script analytics Python
   ├─ Dashboard Streamlit
   └─ Documentation métriques

Release v3.2 : Fin Q3 2026
```

---

## ❓ Questions Ouvertes

### 1. Advisors customisables ?

**Question :** Permettre à l'utilisateur de définir ses propres advisors (nombre, rôles, prompts) ?

**Pros :**
- Flexibilité maximale (ex: advisor "Marketing Copy Expert", "Accessibility Specialist")
- Adaptation contextes très niche

**Cons :**
- Complexité implémentation (UI configuration, validation profils)
- Risque dilution qualité (advisors mal définis)
- Coût support utilisateur

**Décision :** Reporter à v3.3. En v3.2, se limiter aux 3 modes spécialisés pré-définis (SECURITY, LEGAL, UX).

---

### 2. Multi-model Council ?

**Question :** Utiliser différents modèles LLM pour diversifier perspectives (ex: Opus pour Contrarian, Sonnet pour FirstPrinciples, Haiku pour Outsider) ?

**Pros :**
- Diversité cognitive réelle (pas juste prompts différents)
- Potentiel détection angles morts additionnels

**Cons :**
- Coût élevé (mix Opus + Sonnet + Haiku)
- Complexité orchestration (APIs multiples)
- Validation empirique nécessaire (multi-model > mono-model ?)

**Décision :** Expérimentation en v3.3. Tester sur 20 prompts : mono-model Sonnet vs multi-model mix. Si gain angles morts > 20%, intégrer.

---

### 3. Learning loop ?

**Question :** Council apprend-il des décisions passées ? (ex: si user rejette souvent recommandation Expansionist, réduire son poids ?)

**Pros :**
- Amélioration continue adaptative
- Personnalisation par utilisateur

**Cons :**
- Risque overfitting user biases
- Complexité ML (pondération dynamique advisors)
- Éthique : faut-il adapter Council aux préférences user ?

**Décision :** Discussion v3.3+. Évaluer si philosophiquement aligné avec objectif Council (détecter angles morts vs confirmer préférences user).

---

## 🔗 Ressources

- **COUNCIL_INTEGRATION.md** : Documentation complète v3.0 base
- **CHANGELOG_v3.1.md** : Leçons META intégrées v3.1
- **OPTION_1_2_COMPLETE.md** : Cycle vertueux test → correction → généralisation
- **council-report-20260512-175851.html** : Exemple test Council complet

---

## 🎯 Vision Long-Terme (v3.3+)

Au-delà de v3.2, explorer :
- **Council hiérarchique** : Meta-Council qui audite le verdict du Council (2 niveaux)
- **Council asynchrone** : Advisors indépendants contribuent sur plusieurs heures (pas temps réel)
- **Council collaboratif** : Advisors débattent entre eux avant chairman (pas juste peer review)
- **Council ouvert** : Communauté contribue advisors custom (marketplace)

---

*Roadmap v3.2 créée le 2026-05-12*  
*Promptor v3.1 Council Edition — Prompt Engineering avec délibération multi-perspective optionnelle*