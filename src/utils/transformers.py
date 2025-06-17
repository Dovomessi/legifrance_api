from typing import Dict, Any, List

def transform_code_response(api_response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Transforme la réponse brute de l'API Légifrance pour la recherche de codes
    en une liste d'articles structurés (titre, texte, lien, etc.).
    """
    articles = []
    for item in api_response.get("results", []):
        article = {
            "id": item.get("id"),
            "numero": item.get("numero"),
            "titre": item.get("titre"),
            "contenu": item.get("contenu"),
            "etat": item.get("etat"),
            "date_debut": item.get("date_debut"),
            "date_fin": item.get("date_fin"),
            "date_maj": item.get("date_maj"),
            "nature": item.get("nature"),
            "section": item.get("section"),
            "source": "Légifrance",
            "lien_officiel": item.get("lien_officiel")
        }
        articles.append(article)
    return articles

def transform_texte_legal_response(api_response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Transforme la réponse brute de l'API Légifrance pour la recherche de textes légaux.
    """
    textes = []
    for item in api_response.get("results", []):
        texte = {
            "id": item.get("id"),
            "titre": item.get("titre"),
            "contenu": item.get("contenu"),
            "date_maj": item.get("date_maj"),
            "nature": item.get("nature"),
            "source": "Légifrance",
            "lien_officiel": item.get("lien_officiel")
        }
        textes.append(texte)
    return textes

def transform_jurisprudence_response(api_response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Transforme la réponse brute de l'API Légifrance pour la recherche de jurisprudence.
    """
    decisions = []
    for item in api_response.get("results", []):
        decision = {
            "id": item.get("id"),
            "date": item.get("date"),
            "juridiction": item.get("juridiction"),
            "numero": item.get("numero"),
            "theme_principal": item.get("theme_principal"),
            "resume": item.get("resume"),
            "texte_integral": item.get("texte_integral"),
            "lien_officiel": item.get("lien_officiel"),
            "source": "Légifrance"
        }
        decisions.append(decision)
    return decisions
