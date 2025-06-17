from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class CodeSearchParams(BaseModel):
    search: Optional[str] = None
    code_name: Optional[str] = None
    champ: Optional[str] = Field(default="ALL")
    sort: Optional[str] = Field(default="PERTINENCE")
    type_recherche: Optional[str] = Field(default="TOUS_LES_MOTS_DANS_UN_CHAMP")
    page_size: Optional[int] = Field(default=10)
    fetch_all: Optional[bool] = Field(default=False)

class TexteLegalSearchParams(BaseModel):
    text_id: Optional[str] = None
    search: Optional[str] = None
    champ: Optional[str] = Field(default="ALL")
    type_recherche: Optional[str] = Field(default="TOUS_LES_MOTS_DANS_UN_CHAMP")
    page_size: Optional[int] = Field(default=10)

class JurisprudenceSearchParams(BaseModel):
    search: Optional[str] = None
    publication_bulletin: Optional[List[str]] = None  # <-- Correction ici
    sort: Optional[str] = Field(default="DATE_DESC")
    champ: Optional[str] = Field(default="ALL")
    type_recherche: Optional[str] = Field(default="TOUS_LES_MOTS_DANS_UN_CHAMP")
    page_size: Optional[int] = Field(default=10)
    fetch_all: Optional[bool] = Field(default=False)
    juridiction_judiciaire: Optional[List[str]] = None  # Ajoute si besoin d'autres listes

class Article(BaseModel):
    id: str
    numero: str
    titre: str
    contenu: str
    etat: Optional[str] = None
    date_debut: Optional[datetime] = None
    date_fin: Optional[datetime] = None
    date_maj: Optional[datetime] = None
    nature: Optional[str] = None
    section: Optional[str] = None
    source: str = "Légifrance"
