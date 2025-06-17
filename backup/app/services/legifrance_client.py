import httpx
from typing import Dict, Any
import os
from dotenv import load_dotenv
from ..core.oauth import LegifranceAuth
from datetime import datetime

load_dotenv()

class LegifranceClient:
    def __init__(self):
        self.auth = LegifranceAuth()
        self.base_url = os.getenv("LEGIFRANCE_API_ENDPOINT")

    async def get_headers(self) -> Dict[str, str]:
        token = await self.auth.get_token()
        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    async def get_codes(self) -> Dict[str, Any]:
        """Récupère la liste des codes disponibles"""
        async with httpx.AsyncClient() as client:
            headers = await self.get_headers()
            data = {
                "recherche": {
                    "champs": [],
                    "filtres": [],
                    "pageNumber": 1,
                    "pageSize": 100,
                    "operateur": "ET",
                    "sort": "PERTINENCE",
                    "typePagination": "ARTICLE"
                },
                "fond": "CODE_DATE"
            }
            response = await client.post(
                f"{self.base_url}/search",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            return response.json()

    async def search_code(self, code_id: str) -> Dict[str, Any]:
        """Recherche un code spécifique"""
        async with httpx.AsyncClient() as client:
            headers = await self.get_headers()
            data = {
                "id": code_id
            }
            response = await client.post(
                f"{self.base_url}/consult/getArticle",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            return response.json()
