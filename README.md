# API Légifrance

## Description
API FastAPI pour accéder aux données juridiques françaises via l'API Légifrance officielle.

## Installation
```bash
# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows

# Installer les dépendances
pip install -r requirements.txt
```

## Configuration
Créer un fichier `.env` à la racine du projet :
```env
LEGIFRANCE_CLIENT_ID=votre_client_id
LEGIFRANCE_CLIENT_SECRET=votre_client_secret
LEGIFRANCE_API_URL=https://oauth.piste.gouv.fr
LEGIFRANCE_API_ENDPOINT=https://api.piste.gouv.fr/dila/legifrance/lf-engine-app
```

## Démarrage
```bash
uvicorn src.server.main:app --reload --host 0.0.0.0 --port 8000
```

## Documentation API
Accéder à la documentation Swagger :
http://localhost:8000/docs

## Endpoints
1. `/tools/rechercher_code` - Recherche dans les codes
2. `/tools/rechercher_texte_legal` - Recherche de textes légaux
3. `/tools/rechercher_jurisprudence_judiciaire` - Recherche de jurisprudence

## Tests
```bash
pytest tests/
```
```

5. **Pour démarrer avec la nouvelle structure** :
```bash
# Arrête le serveur actuel si nécessaire (Ctrl+C)
cd ~/legifrance_api
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.server.main:app --reload --host 0.0.0.0 --port 8000
```

**Veux-tu que je te montre comment :**
1. Tester les nouveaux endpoints
2. Ajouter des fonctionnalités spécifiques
3. Configurer le logging
4. Mettre en place le monitoring

Dis-moi ce qui t'intéresse en premier !
