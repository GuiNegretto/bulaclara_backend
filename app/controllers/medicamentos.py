"""Endpoints de medicamentos (consulta de bula simplificada)."""

from fastapi import APIRouter, HTTPException

from app.schemas.medicamento import (
    MedicamentoConsultaRequest,
    MedicamentoConsultaResponse,
)
from app.services import consulta_service

router = APIRouter(prefix="/medicamentos", tags=["medicamentos"])


@router.post(
    "/consulta",
    response_model=MedicamentoConsultaResponse,
    summary="Consulta bula simplificada por nome ou GTIN",
)
def consultar(payload: MedicamentoConsultaRequest) -> MedicamentoConsultaResponse:
    """Retorna a bula simplificada do medicamento buscado."""
    try:
        return consulta_service.consultar_medicamento(
            nome=payload.nome,
            gtin=payload.gtin,
        )
    except consulta_service.MedicamentoNaoEncontrado as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc