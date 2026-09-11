"""Serviço de consulta de medicamentos.

Orquestra a busca na ordem definida pela arquitetura:
1. cache local (SQLite)         — Fase 2
2. cache remoto (PostgreSQL)    — Fase 2
3. ANVISA / Bulário Eletrônico  — Fase 3
4. IA generativa (simplificação)— Fase 4

Na Fase 1 a ``DemoFonteMedicamento`` apenas valida o fluxo
Controller ⮕ Service ⮕ Fonte de ponta a ponta. Nas fases 2 e 3 ela
é substituída pelas fontes reais.
"""

from app.schemas.medicamento import BulaSimplificada, MedicamentoConsultaResponse


class MedicamentoNaoEncontrado(Exception):
    """Lançada quando nenhuma fonte encontra o medicamento buscado."""


class DemoFonteMedicamento:
    """Fonte de dados de demonstração — provisória até a Fase 3 (ANVISA)."""

    def consultar(
        self,
        nome: str | None,
        gtin: str | None,
    ) -> MedicamentoConsultaResponse | None:
        if not nome and not gtin:
            return None
        return MedicamentoConsultaResponse(
            nome=nome if nome else "Medicamento de demonstração",
            gtin=gtin,
            laboratorio="Laboratório Demo Ltda.",
            principios_ativos=["Princípio ativo de demonstração"],
            bula_simplificada=BulaSimplificada(
                contraindicacoes=[
                    "Não usar em caso de alergia ao princípio ativo.",
                    "Consulte um médico antes de iniciar o tratamento.",
                ],
                forma_de_uso=[
                    "Tomar por via oral com um copo de água.",
                    "Pode ser tomado com ou sem alimentos.",
                ],
                posologia="1 comprimido a cada 8 horas, durante 5 dias.",
                efeitos_colaterais=["Sonolência", "Dor de cabeça"],
                armazenamento=(
                    "Manter em temperatura ambiente, "
                    "protegido da luz e umidade."
                ),
                interacoes_medicamentosas=[
                    "Não consumir bebidas alcoólicas durante o tratamento.",
                ],
            ),
        )


def consultar_medicamento(
    nome: str | None,
    gtin: str | None,
) -> MedicamentoConsultaResponse:
    """Consulta o medicamento usando as fontes na ordem de prioridade."""
    # Fase 1: fonte demo. Fase 2+ entra o cache (local → remoto) e, em
    # seguida, a ANVISA (Fase 3) nos casos em que o cache não cobrir.
    fonte = DemoFonteMedicamento()
    resultado = fonte.consultar(nome=nome, gtin=gtin)
    if resultado is None:
        raise MedicamentoNaoEncontrado(
            f"Medicamento não encontrado (nome={nome!r}, gtin={gtin!r})."
        )
    return resultado