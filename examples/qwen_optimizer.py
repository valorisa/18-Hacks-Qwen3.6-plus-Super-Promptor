"""
Wrapper Python modulaire pour optimiser les appels Qwen3.6+ via OpenRouter.
Applique automatiquement les hacks de gestion de tokens (compactage, alertes, routing).
"""

import os
import time
import logging
from typing import List, Dict, Any, Optional
from openai import OpenAI

# Configuration du logger
logging.basicConfig(
    level=os.getenv("QWEN_LOG_LEVEL", "INFO"),
    format="%(asctime)s | [QWEN-OPT] %(levelname)s | %(message)s"
)


class Qwen36Optimizer:
    """Optimiseur de contexte et de coûts pour Qwen3.6+.

    Args:
        api_key: Clé API OpenRouter.
        session_limit: Limite maximale de tokens par session (défaut: 1_000_000).

    Attributes:
        client: Instance OpenAI configurée pour OpenRouter.
        current_prompt_tokens: Nombre de tokens consommés dans la session courante.
        messages: Historique des messages de la session.
        last_activity: Timestamp de la dernière activité (pour détection de pause).
    """

    def __init__(self, api_key: str, session_limit: int = 1_000_000):
        self.client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
        self.session_limit = session_limit
        self.current_prompt_tokens = 0
        self.messages: List[Dict[str, Any]] = []
        self.last_activity = time.time()

    def track_usage(self, response: Any) -> Dict[str, int]:
        """Suit la consommation de tokens et déclenche les alertes.

        Args:
            response: Objet réponse de l'API OpenAI.

        Returns:
            Dictionnaire contenant prompt, completion et cached tokens.
        """
        usage = getattr(response, "usage", None)
        if not usage:
            return {}

        prompt = getattr(usage, "prompt_tokens", 0)
        completion = getattr(usage, "completion_tokens", 0)
        cached = getattr(usage, "cached_tokens", 0)
        self.current_prompt_tokens = prompt
        self._check_alerts()
        return {"prompt": prompt, "completion": completion, "cached": cached}

    def _check_alerts(self) -> None:
        """Vérifie les seuils d'alerte (70% warning, 90% critique)."""
        pct = (self.current_prompt_tokens / self.session_limit) * 100
        if pct >= 90:
            logging.critical(
                "🚨 ALERTE 90%% | Contexte saturé (%.1f%%). "
                "Compactage/Reset IMMÉDIAT requis.", pct
            )
        elif pct >= 70:
            logging.warning(
                "⚠️ ALERTE 70%% | Contexte élevé (%.1f%%). "
                "Prépare un résumé ou un reset.", pct
            )

    def manual_compact(self, threshold: float = 0.6) -> bool:
        """Compacte manuellement le contexte si le seuil est atteint.

        Args:
            threshold: Pourcentage du contexte pour déclencher le compactage.

        Returns:
            True si un compactage a été effectué, False sinon.
        """
        if self.current_prompt_tokens >= self.session_limit * threshold:
            logging.info("📦 Compactage manuel activé. Historique réinitialisé proprement.")
            self.messages = []
            self.current_prompt_tokens = 5000
            return True
        return False

    def safe_call(
        self,
        prompt: str,
        task_type: str = "default",
        max_tokens: int = 4096,
    ) -> Optional[str]:
        """Effectue un appel API sécurisé avec tracking, alertes et routing.

        Args:
            prompt: Requête utilisateur.
            task_type: Type de tâche pour le routing (default, subtask, complex).
            max_tokens: Limite maximale de tokens de sortie.

        Returns:
            Contenu de la réponse ou None en cas d'erreur.
        """
        routing_map = {
            "default": "qwen/qwen3.6-plus",
            "subtask": "qwen/qwen-flash",
            "complex": "qwen/qwen-max",
        }
        model = routing_map.get(task_type, routing_map["default"])

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=self.messages + [{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
            )
            text = response.choices[0].message.content
            self.track_usage(response)
            self.messages.extend([
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": text},
            ])
            self.last_activity = time.time()
            self.manual_compact()
            return text
        except Exception as e:
            logging.error("❌ Erreur API : %s", e)
            return None
