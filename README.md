# BulaClara — Backend

Camada de **Controller** e **Model/Serviços** do BulaClara: aplicativo desktop
que ajuda pessoas com deficiência visual e cuidadores de idosos a consultarem
bulas de medicamentos simplificadas (contraindicações, forma de uso, efeitos
colaterais) e a gerarem etiquetas em PDF com horários de uso.

## Stack

- Python 3.12 · FastAPI · SQLAlchemy · Alembic · Pydantic · pytest

## Estrutura (MVC)

```
app/
├── main.py            # FastAPI + CORS + routers
├── controllers/       # routers HTTP sem lógica de negócio
├── schemas/           # contratos Pydantic de entrada/saída
├── models/            # entidades SQLAlchemy (compartilhadas local/remoto)
├── services/          # regras de negócio: cache, ANVISA, IA, OCR, etiquetas
├── repositories/      # local_repository (SQLite) e remote_repository (PostgreSQL)
└── core/              # configuração via variáveis de ambiente (pydantic-settings)
```

## Como rodar (desenvolvimento)

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env   # preencha conforme seu ambiente
.\.venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

## Testes

```powershell
.\.venv\Scripts\python -m pytest -q
```

## Estado atual (Fase 1)

- `app/schemas/medicamento.py` — contrato `POST /medicamentos/consulta`
  (busca por nome e/ou GTIN; validações no Pydantic).
- `app/controllers/medicamentos.py` — router registrado em `main.py`.
- `app/services/consulta_service.py` — orquestra fontes de dados. Na Fase 1
  usa a `DemoFonteMedicamento` (dados fictícios claramente marcados) apenas
  para validar o fluxo Controller ⮕ Service ⮕ Fonte de ponta a ponta.
  Nas Fases 2 e 3 essa fonte é substituída pelo cache (SQLite → PostgreSQL)
  e pela ANVISA.
- `app/models/` e `app/repositories/` — camadas vazias criadas (SQLAlchemy e
  cache entram na Fase 2).

## Configuração

Toda a configuração é feita por variáveis de ambiente (`.env`), lidas por
`pydantic-settings` em `app/core/config.py`. Veja o `.env.example` para o
inventário completo.

> **Importante:** a connection string do PostgreSQL remoto e as chaves de API
> (ANVISA/IA generativa) são segredos e **nunca** devem ser commitados — use
> apenas o `.env` local.