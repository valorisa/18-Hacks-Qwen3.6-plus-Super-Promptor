# 📚 18 Hacks Optimisation Tokens — Qwen3.6+ / OpenRouter

### 💡 Principe Fondamental
Le coût est exponentiel, pas linéaire. À chaque message, Qwen relit **tout** l'historique (98.5% de la conso est l'historique + overhead).
Règle d'or : Hygiène de contexte = Économie de tokens + Meilleure qualité (évite le "lost in the middle").

## 🔹 NIVEAU 1 : FONDAMENTAUX (Hacks 1-9)

1. **Nouvelle session par tâche** : Reset explicite de l'historique. Pas de `/clear` natif sous OpenRouter.
2. **Désactive outils/MCP inutiles** : Chaque outil connecté charge sa définition (~5-15k tokens) à chaque appel API.
3. **Regroupe les prompts** : 1 message combiné = 3x moins cher que 3 follow-ups.
4. **Plan Mode (95% confiance)** : Exige un plan structuré avant exécution. Ne génère pas de code tant que le plan n'est pas validé.
5. **Monitoring natif** : Parse `prompt_tokens`, `completion_tokens`, `cached_tokens` pour tracker la conso.
6. **Status Line** : Calcule `% contexte utilisé` = `(prompt_tokens / 1_000_000) * 100`.
7. **Dashboard OpenRouter** : Vérifie la conso sur openrouter.ai/activity toutes les 20-30 min.
8. **Injection chirurgicale** : Ne colle jamais un fichier entier si une section suffit.
9. **Surveillance active** : Détecte les répétitions. Interruption si boucle détectée.

## 🔸 NIVEAU 2 : INTERMÉDIAIRE (Hacks 10-14)

10. **System prompt < 200 lignes** : Traite-le comme un INDEX, pas un dump. Pointe vers les fichiers, ne charge pas le contenu brut.
11. **Références précises** : Utilise `@fichier:L45-L120` (lignes spécifiques) au lieu de "cherche dans tout le repo".
12. **Compact manuel à 60%** : Le contexte à 95% est dégradé (lost in the middle). Demande un résumé structuré, reset, réinjecte résumé + tâche courante.
13. **Gestion pauses >5 min** : Le cache prefix OpenRouter expire après ~5 min d'inactivité. Compacte avant une pause.
14. **Troncature outputs shell** : Limite les logs/CLI à 50 lignes max. Garde le début + fin, omets le milieu.

## 🔺 NIVEAU 3 : EXPERT (Hacks 15-18)

15. **Router de modèles** :
    - `qwen/qwen3.6-plus` : Par défaut (équilibre qualité/coût)
    - `qwen/qwen-flash` : Sous-tâches rapides, formatage, pas cher
    - `qwen/qwen-max` : Architecture complexe, planification lourde
    → Gain : 40-60% de coût en évitant de sur-provisionner.
16. **Sous-agents limités** : 1 sous-agent = contexte complet rechargé (7-10x plus cher). Limite à 2-3 max en parallèle.
17. **Off-Peak Scheduling** :
    - Peak (cher/lent) : 14h-20h CET (jours de semaine)
    - Off-Peak (optimal) : Après 20h + Weekend
    → Groupe les tâches lourdes hors pic.
18. **Source de vérité persistante** : Utilise un fichier de progression pour les décisions stables et règles d'archi. Ne jamais y stocker des logs de conversation.

## 🎯 Instructions pour l'IA
Quand tu génères un prompt ou guides l'utilisateur :
- Consulte mentalement cette liste.
- Privilégie les hacks #3, #4, #11, #12, #15.
- Mentionne explicitement les hacks activés dans ta réponse.
- Si une feature Qwen3.6+ n'est pas documentée, marque `[À CLARIFIER]`.
