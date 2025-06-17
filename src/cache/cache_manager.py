from typing import Any, Optional
from datetime import datetime, timedelta
import json
from cachetools import TTLCache

class CacheManager:
    def __init__(self, ttl_seconds: int = 3600):
        """
        Initialise le gestionnaire de cache
        :param ttl_seconds: Durée de vie des entrées en secondes (par défaut 1 heure)
        """
        self.cache = TTLCache(maxsize=100, ttl=ttl_seconds)

    def get_key(self, prefix: str, params: dict) -> str:
        """
        Génère une clé de cache unique basée sur les paramètres
        :param prefix: Préfixe pour la clé (ex: 'code', 'jurisprudence')
        :param params: Dictionnaire des paramètres de la requête
        :return: Clé unique pour le cache
        """
        sorted_params = sorted(params.items())
        return f"{prefix}:{json.dumps(sorted_params)}"

    def get(self, key: str) -> Optional[Any]:
        """
        Récupère une valeur du cache
        :param key: Clé de cache
        :return: Valeur stockée ou None si non trouvée
        """
        return self.cache.get(key)

    def set(self, key: str, value: Any) -> None:
        """
        Stocke une valeur dans le cache
        :param key: Clé de cache
        :param value: Valeur à stocker
        """
        self.cache[key] = value

    def clear(self) -> None:
        """Vide le cache"""
        self.cache.clear()

    def remove(self, key: str) -> None:
        """
        Supprime une entrée spécifique du cache
        :param key: Clé à supprimer
        """
        if key in self.cache:
            del self.cache[key]

    def get_stats(self) -> dict:
        """
        Retourne des statistiques sur l'utilisation du cache
        :return: Dictionnaire avec les statistiques
        """
        return {
            "size": len(self.cache),
            "maxsize": self.cache.maxsize,
            "currsize": self.cache.currsize,
            "hits": getattr(self.cache, "hits", 0),
            "misses": getattr(self.cache, "misses", 0)
        }
