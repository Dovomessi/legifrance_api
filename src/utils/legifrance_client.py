import httpx
from typing import Dict, Any, Optional
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from ..cache.cache_manager import CacheManager

# Charger les variables d'environnement
load_dotenv()

class LegifranceClient:
    def __init__(self):
        self.client_id = os.getenv("LEGIFRANCE_CLIENT_ID")
        self.client_secret = os.getenv("LEGIFRANCE_CLIENT_SECRET")
        self.base_url = os.getenv("LEGIFRANCE_API_ENDPOINT")
        self.token_url = "https://oauth.piste.gouv.fr/api/oauth/token"

        if not all([self.client_id, self.client_secret, self.base_url]):
            raise ValueError("Variables d'environnement manquantes. Vérifiez votre fichier .env")

        self.access_token = None
        self.token_expires = None
        self.cache = CacheManager()

    async def get_token(self) -> str:
        if self.is_token_valid():
            return self.access_token

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.token_url,
                    data={
                        "grant_type": "client_credentials",
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "scope": "openid"
                    },
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
                )
                response.raise_for_status()
                data = response.json()
                self.access_token = data["access_token"]
                self.token_expires = datetime.now() + timedelta(seconds=data["expires_in"] - 300)
                return self.access_token
            except Exception as e:
                raise RuntimeError(f"Erreur lors de l'obtention du token : {str(e)}")

    def is_token_valid(self) -> bool:
        if not self.access_token or not self.token_expires:
            return False
        return datetime.now() < self.token_expires

    async def get_headers(self) -> Dict[str, str]:
        token = await self.get_token()
        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    async def rechercher_code(self, params: dict) -> Dict[str, Any]:
        payload = {
            "recherche": {
                "champs": [],
                "filtres": [],
                "pageNumber": 1,
                "pageSize": params.get("page_size", 10),
                "operateur": "ET",
                "sort": params.get("sort", "PERTINENCE"),
                "typePagination": "ARTICLE"
            },
            "fond": "CODE_DATE"
        }

        if params.get("search"):
            payload["recherche"]["champs"].append({
                "type": params.get("champ", "ALL"),
                "text": params["search"],
                "typeRecherche": params.get("type_recherche", "TOUS_LES_MOTS_DANS_UN_CHAMP")
            })

        if params.get("code_name"):
            payload["recherche"]["filtres"].append({
                "type": "CODE",
                "text": params["code_name"]
            })

        cache_key = self.cache.get_key("code", params)
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result

        headers = await self.get_headers()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/code",
                headers=headers,
                json=payload
            )
            print("Status code:", response.status_code)
            print("Response text:", response.text)
            result = response.json()
            self.cache.set(cache_key, result)
            return result

    async def rechercher_texte_legal(self, params: dict) -> Dict[str, Any]:
        payload = {
            "recherche": {
                "champs": [],
                "filtres": [],
                "pageNumber": 1,
                "pageSize": params.get("page_size", 10),
                "operateur": "ET",
                "sort": params.get("sort", "PERTINENCE"),
                "typePagination": "ARTICLE"
            },
            "fond": "LODA"
        }

        if params.get("search"):
            payload["recherche"]["champs"].append({
                "type": params.get("champ", "ALL"),
                "text": params["search"],
                "typeRecherche": params.get("type_recherche", "TOUS_LES_MOTS_DANS_UN_CHAMP")
            })

        if params.get("text_id"):
            payload["recherche"]["filtres"].append({
                "type": "TEXT_ID",
                "text": params["text_id"]
            })

        cache_key = self.cache.get_key("texte_legal", params)
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result

        headers = await self.get_headers()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/loda",
                headers=headers,
                json=payload
            )
            print("Status code:", response.status_code)
            print("Response text:", response.text)
            result = response.json()
            self.cache.set(cache_key, result)
            return result

    async def rechercher_jurisprudence(self, params: dict) -> Dict[str, Any]:
        payload = {
            "recherche": {
                "champs": [],
                "filtres": [],
                "pageNumber": 1,
                "pageSize": params.get("page_size", 10),
                "operateur": "ET",
                "sort": params.get("sort", "DATE_DESC"),
                "typePagination": "DECISION"
            },
            "fond": "JURI"
        }

        if params.get("search"):
            payload["recherche"]["champs"].append({
                "type": params.get("champ", "ALL"),
                "text": params["search"],
                "typeRecherche": params.get("type_recherche", "TOUS_LES_MOTS_DANS_UN_CHAMP")
            })

        if params.get("publication_bulletin"):
            payload["recherche"]["filtres"].append({
                "type": "PUBLICATION_BULLETIN",
                "values": params["publication_bulletin"]
            })

        if params.get("juridiction_judiciaire"):
            payload["recherche"]["filtres"].append({
                "type": "JURIDICTION",
                "values": params["juridiction_judiciaire"]
            })

        cache_key = self.cache.get_key("jurisprudence", params)
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result

        headers = await self.get_headers()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/juri",
                headers=headers,
                json=payload
            )
            print("Status code:", response.status_code)
            print("Response text:", response.text)
            result = response.json()
            self.cache.set(cache_key, result)
            return result
