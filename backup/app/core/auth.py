from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
import os
from dotenv import load_dotenv

load_dotenv()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API Key manquante"
        )
    if api_key != os.getenv("CLIENT_API_KEY"):
        raise HTTPException(
            status_code=403,
            detail="API Key invalide"
        )
    return api_key
