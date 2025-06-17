from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import codes  # nous allons créer ce module ensuite

app = FastAPI(
    title="API Légifrance",
    description="API pour accéder aux données juridiques françaises",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route de test
@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API Légifrance"}

# Inclusion des routes
app.include_router(codes.router)
