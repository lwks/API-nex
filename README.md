# FastAPI Scaffold (NoSQL-ready)

Layered FastAPI project with async MongoDB repository and REST best practices.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r app/requirements.txt
cp .env.example .env
uvicorn app.src.main:app --reload
```

- Health check: `GET /health` → `{"status":"ok"}`
- Swagger UI: `http://localhost:8000/docs` (or just open `http://localhost:8000` for a redirect)
- Items CRUD under: `/api/v1/items`
- Users endpoints under: `/api/v1/users`
- Companies CRUD under: `/api/v1/companies`

### Empresas (Companies) payload

| Campo         | Tipo   | Descrição                                                 |
| ------------- | ------ | --------------------------------------------------------- |
| `id`          | string | ID única da empresa (ex: `cli_001`)                       |
| `nome`        | string | Nome da empresa                                           |
| `cnpj`        | string | CNPJ da empresa                                           |
| `setor`       | string | Setor de atuação (ex: Tecnologia, Saúde)                  |
| `localizacao` | string | Cidade e estado                                           |
| `criado_em`   | date   | Data de cadastro da empresa (ISO 8601, ex: `2024-01-31`) |
| `vagas`       | array  | Lista de vagas abertas ou já encerradas                  |

## Structure

```
app/
  controllers/
  domain/
  helpers/
  models/
  services/
tests/
```

## Notes
- Simple DI wiring sets singleton services (items, users, companies) at startup.
- Swap storage by implementing a new repository matching `RepositoryProtocol`.
