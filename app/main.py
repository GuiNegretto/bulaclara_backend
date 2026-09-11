"""Ponto de entrada da API BulaClara (FastAPI).

Fase 0 — esqueleto: CORS + `/health`.
Fase 1 — MVC: controllers, services e schemas registrados
(`POST /medicamentos/consulta`).
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import medicamentos
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------- Routers --------------- #
app.include_router(medicamentos.router)


@app.get("/health", tags=["sistema"])
def health() -> dict[str, str]:
    """Health check usado pelo Electron para saber quando o backend subiu."""
    return {"status": "ok", "app": settings.app_name}