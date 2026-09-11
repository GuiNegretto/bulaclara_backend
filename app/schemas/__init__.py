"""Contratos Pydantic de entrada/saída da API BulaClara."""

from app.schemas.medicamento import (
    BulaSimplificada,
    MedicamentoConsultaRequest,
    MedicamentoConsultaResponse,
)

__all__ = [
    "BulaSimplificada",
    "MedicamentoConsultaRequest",
    "MedicamentoConsultaResponse",
]