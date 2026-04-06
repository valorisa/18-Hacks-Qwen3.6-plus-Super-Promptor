"""
Exemple concret d'agent générateur de contenu utilisant le wrapper Qwen36Optimizer.
Démontre le routing de modèle, le tracking de tokens et le compactage automatique.

Utilisation :
    export OPENROUTER_API_KEY="sk-or-v1-xxx"
    python content-agent-example.py
"""

import os
import sys

# Ajoute le répertoire courant au path pour importer qwen_optimizer
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from qwen_optimizer import Qwen36Optimizer


def run_content_agent():
    """Lance un agent de génération de contenu optimisé.

    Workflow :
        1. Initialisation de l'optimiseur avec la clé API OpenRouter.
        2. Démarrage d'une nouvelle session de génération.
        3. Envoi de la requête avec routing vers le modèle adapté.
        4. Affichage des résultats et de la consommation.
    """
    print("\n" + "=" * 60)
    print("🚀 DÉMARRAGE AGENT GÉNÉRATEUR DE CONTENU (Qwen3.6+ Optimisé)")
    print("=" * 60 + "\n")

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ Variable OPENROUTER_API_KEY non définie.")
        print("   Exporte-la : export OPENROUTER_API_KEY='sk-or-v1-xxx'")
        return

    opt = Qwen36Optimizer(api_key=api_key)

    prompt = (
        "Génère un article de blog sur 'Optimisation des tokens LLM en Python'. "
        "Structure : Intro, 3 techniques avancées, Conclusion, FAQ."
    )

    print("📝 Génération en cours...")
    result = opt.safe_call(prompt, task_type="default")

    if result:
        print("\n✅ Article généré avec succès.")
        print("-" * 40)
        print(result)
    else:
        print("🚫 Échec de la génération (boucle ou erreur API).")

    pct = (opt.current_prompt_tokens / opt.session_limit) * 100
    print(f"\n📊 USAGE FINAL: {opt.current_prompt_tokens:,} tokens")
    print(f"📈 % CONTEXTE UTILISÉ: {pct:.1f}%\n")


if __name__ == "__main__":
    run_content_agent()
