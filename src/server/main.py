from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from ..models.schemas import CodeSearchParams, TexteLegalSearchParams, JurisprudenceSearchParams
from ..utils.legifrance_client import LegifranceClient
from ..utils.transformers import (
    transform_code_response,
    transform_texte_legal_response,
    transform_jurisprudence_response
)
from typing import Dict, Any
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration de l'authentification
API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

app = FastAPI(
    title="API Légifrance",
    description="API pour accéder aux données juridiques françaises",
    version="1.0.0",
    openapi_tags=[
        {"name": "legifrance", "description": "Opérations sur les données juridiques"}
    ]
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Client Légifrance
legifrance_client = LegifranceClient()

@app.post("/tools/rechercher_code", tags=["legifrance"])
async def rechercher_code(
    params: CodeSearchParams,
    api_key: str = Depends(API_KEY_HEADER)
) -> Dict[str, Any]:
    """
    Recherche dans les codes juridiques français.
    """
    try:
        logger.info(f"Recherche dans les codes avec paramètres: {params}")
        api_response = await legifrance_client.rechercher_code(params.dict())
        logger.info(f"Réponse brute API: {api_response}")  # <-- Ajout du log ici
        articles = transform_code_response(api_response)
        return {"articles": articles}
    except Exception as e:
        logger.error(f"Erreur lors de la recherche dans les codes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/rechercher_texte_legal", tags=["legifrance"])
async def rechercher_texte_legal(
    params: TexteLegalSearchParams,
    api_key: str = Depends(API_KEY_HEADER)
) -> Dict[str, Any]:
    """
    Recherche dans les textes légaux.
    """
    try:
        logger.info(f"Recherche de texte légal avec paramètres: {params}")
        api_response = await legifrance_client.rechercher_texte_legal(params.dict())
        logger.info(f"Réponse brute API: {api_response}")  # <-- Ajout du log ici
        textes = transform_texte_legal_response(api_response)
        return {"textes": textes}
    except Exception as e:
        logger.error(f"Erreur lors de la recherche de texte légal: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/rechercher_jurisprudence_judiciaire", tags=["legifrance"])
async def rechercher_jurisprudence_judiciaire(
    params: JurisprudenceSearchParams,
    api_key: str = Depends(API_KEY_HEADER)
) -> Dict[str, Any]:
    """
    Recherche dans la jurisprudence judiciaire.
    """
    try:
        logger.info(f"Recherche de jurisprudence avec paramètres: {params}")
        api_response = await legifrance_client.rechercher_jurisprudence(params.dict())
        logger.info(f"Réponse brute API: {api_response}")  # <-- Ajout du log ici
        decisions = transform_jurisprudence_response(api_response)
        return {"decisions": decisions}
    except Exception as e:
        logger.error(f"Erreur lors de la recherche de jurisprudence: {e}")
        raise HTTPException(status_code=500, detail=str(e))
