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
- Vagas CRUD under: `/api/v1/vagas`

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

### Vagas payload

| Campo           | Tipo   | Descrição                                                                 |
| --------------- | ------ | ------------------------------------------------------------------------- |
| `client_id`     | string | Referência para a empresa responsável pela vaga                          |
| `titulo`        | string | Título da vaga (ex: `Analista de Dados`)                                  |
| `descricao`     | string | Descrição detalhada das atividades                                       |
| `nivel`         | string | Nível da vaga (ex: Júnior, Pleno, Sênior)                                 |
| `localizacao`   | string | Local da vaga (cidade, estado ou `Remoto`)                                |
| `publicada_em`  | date   | Data de publicação (ISO 8601, ex: `2024-03-10`)                            |
| `status`        | string | Situação atual da vaga (ex: Aberta, Fechada, Em análise)                  |
| `skills`        | array  | Lista de habilidades desejadas (ex: `["Python", "AWS", "Testes"]`)        |

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
