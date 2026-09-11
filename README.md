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

## Configuração

Toda a configuração é feita por variáveis de ambiente (`.env`), lidas por
`pydantic-settings` em `app/core/config.py`. Veja o `.env.example` para o
inventário completo.

> **Importante:** a connection string do PostgreSQL remoto e as chaves de API
> (ANVISA/IA generativa) são segredos e **nunca** devem ser commitados — use
> apenas o `.env` local.