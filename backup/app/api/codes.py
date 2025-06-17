from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from ..services.legifrance_client import LegifranceClient
from ..core.auth import verify_api_key

router = APIRouter(prefix="/tools", tags=["legifrance"])

@router.post("/rechercher_code")
async def rechercher_code(
    search: Optional[str] = None,
    code_name: Optional[str] = None,
    champ: Optional[str] = "ALL",
    sort: Optional[str] = "PERTINENCE",
    type_recherche: Optional[str] = "TOUS_LES_MOTS_DANS_UN_CHAMP",
    page_size: Optional[int] = 10,
    fetch_all: Optional[bool] = False,
    api_key: str = Depends(verify_api_key)
):
    """
    Recherche dans les codes juridiques français.
    Paramètres identiques au projet mcp-server-legifrance
    """
    try:
        client = LegifranceClient()
        return await client.rechercher_code(
            search=search,
            code_name=code_name,
            champ=champ,
            sort=sort,
            type_recherche=type_recherche,
            page_size=page_size,
            fetch_all=fetch_all
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/rechercher_texte_legal")
async def rechercher_texte_legal(
    text_id: Optional[str] = None,
    search: Optional[str] = None,
    champ: Optional[str] = "ALL",
    type_recherche: Optional[str] = "TOUS_LES_MOTS_DANS_UN_CHAMP",
    page_size: Optional[int] = 10,
    api_key: str = Depends(verify_api_key)
):
    """
    Recherche des articles dans les textes légaux (lois, ordonnances, décrets, arrêtés)
    """
    try:
        client = LegifranceClient()
        return await client.rechercher_texte_legal(
            text_id=text_id,
            search=search,
            champ=champ,
            type_recherche=type_recherche,
            page_size=page_size
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/rechercher_jurisprudence_judiciaire")
async def rechercher_jurisprudence_judiciaire(
    search: Optional[str] = None,
    publication_bulletin: Optional[str] = None,
    sort: Optional[str] = "DATE_DESC",
    champ: Optional[str] = "ALL",
    type_recherche: Optional[str] = "TOUS_LES_MOTS_DANS_UN_CHAMP",
    page_size: Optional[int] = 10,
    fetch_all: Optional[bool] = False,
    api_key: str = Depends(verify_api_key)
):
    """
    Recherche dans la base de jurisprudence judiciaire
    """
    try:
        client = LegifranceClient()
        return await client.rechercher_jurisprudence(
            search=search,
            publication_bulletin=publication_bulletin,
            sort=sort,
            champ=champ,
            type_recherche=type_recherche,
            page_size=page_size,
            fetch_all=fetch_all
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
