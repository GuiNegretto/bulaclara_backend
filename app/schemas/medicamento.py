"""Schemas Pydantic do domínio de medicamentos (contrato público da API).

Este arquivo define o contrato fixo da aplicação:
`POST /medicamentos/consulta` ↔ requisição/Resposta abaixo.
"""

from pydantic import BaseModel, Field, model_validator


class BulaSimplificada(BaseModel):
    """Resumo da bula organizado por tópicos acessíveis."""

    contraindicacoes: list[str] = Field(default_factory=list)
    forma_de_uso: list[str] = Field(default_factory=list)
    efeitos_colaterais: list[str] = Field(default_factory=list)
    posologia: str = ""
    armazenamento: str = ""
    interacoes_medicamentosas: list[str] = Field(default_factory=list)


class MedicamentoConsultaRequest(BaseModel):
    """Busca por nome e/ou GTIN (código de barras). Pelo menos um é obrigatório."""

    nome: str | None = Field(default=None, max_length=200)
    gtin: str | None = Field(default=None, pattern=r"^[0-9]{8,14}$")

    @model_validator(mode="after")
    def ao_menos_um_campo(self) -> "MedicamentoConsultaRequest":
        if not self.nome and not self.gtin:
            raise ValueError("Informe ao menos 'nome' ou 'gtin'.")
        return self


class MedicamentoConsultaResponse(BaseModel):
    """Bula simplificada do medicamento encontrado."""

    nome: str
    gtin: str | None = None
    laboratorio: str
    principios_ativos: list[str] = Field(default_factory=list)
    bula_simplificada: BulaSimplificada