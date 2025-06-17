import httpx
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

class LegifranceAuth:
    def __init__(self):
        self.client_id = os.getenv("LEGIFRANCE_CLIENT_ID")
        self.client_secret = os.getenv("LEGIFRANCE_CLIENT_SECRET")
        self.token_url = f"{os.getenv('LEGIFRANCE_API_URL')}/token"
        self.access_token = None
        self.token_expires = None

    async def get_token(self) -> str:
        """Obtient ou renouvelle le token d'accès"""
        if self.is_token_valid():
            return self.access_token

        async with httpx.AsyncClient() as client:
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

    def is_token_valid(self) -> bool:
        if not self.access_token or not self.token_expires:
            return False
        return datetime.now() < self.token_expires
