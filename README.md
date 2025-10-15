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
- Users endpoints under: `/api/v1/users`
- Companies CRUD under: `/api/v1/companies`
- Applications CRUD under: `/api/v1/applications`
- Jobs CRUD under: `/api/v1/vagas`
- Use the interactive docs at `http://localhost:8000/docs` to inspect every endpoint's
  request and response schema (click **Try it out** → **Execute** for live examples).

## Inspecting request/response payloads

FastAPI ships with interactive documentation that lets you validate the payloads for
each operation without writing any code.

1. Start the server (`uvicorn app.src.main:app --reload`).
2. Open `http://localhost:8000/docs` for Swagger UI (or `http://localhost:8000/redoc`).
3. Select an endpoint, press **Try it out**, fill the body/query parameters and
   execute the call.
4. Swagger UI shows the exact request sent and the formatted response payload,
   making it easy to verify the contract for every route.

If you prefer the terminal, you can capture the request/response pairs with `curl`
or `httpie`. Example for the companies listing:

```bash
curl -X GET http://localhost:8000/api/v1/companies | jq
```


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

### Applications payload

| Campo                 | Tipo         | Descrição                                                             |
| --------------------- | ------------ | --------------------------------------------------------------------- |
| `company_id`          | string       | Unique identifier for the company associated with the application     |
| `name`                | string       | Company name                                                          |
| `email`               | string       | Corporate e-mail used for login and contact                           |
| `password_hash`       | string       | Password hash used for authentication                                 |
| `phone`               | string       | Contact phone number                                                  |
| `website`             | string (URL) | Official website                                                      |
| `location.city`       | string       | City where the company is located                                     |
| `location.state`      | string       | State where the company is located                                    |
| `location.country`    | string       | Country where the company is located                                  |
| `about`               | string       | Company description                                                   |
| `industry`            | string       | Industry sector (e.g. Technology, Healthcare)                         |
| `size`                | string       | Company size (e.g. `1-10`, `11-50`, `201-500`)                        |
| `founded_year`        | number       | Year the company was founded                                          |
| `social_links.linkedin` | string (URL) | Link to the corporate LinkedIn profile                                |
| `social_links.instagram` | string (URL) | Link to the corporate Instagram profile                               |
| `logo_url`            | string (URL) | URL with the company logo                                             |
| `created_at`          | string (ISO 8601) | Date the application profile was created                            |
| `updated_at`          | string (ISO 8601) | Date the application profile was last updated                       |

### Job openings payload

| Campo           | Tipo   | Descrição                                                                 |
| --------------- | ------ | ------------------------------------------------------------------------- |
| `client_id`     | string | Referência para a empresa responsável pela vaga                          |
| `titulo`        | string | Job title (e.g. `Analista de Dados`)                                     |
| `descricao`     | string | Detailed description of the activities                                   |
| `nivel`         | string | Job level (e.g. Junior, Mid, Senior)                                     |
| `localizacao`   | string | Job location (city/state or `Remote`)                                    |
| `publicada_em`  | date   | Publication date (ISO 8601, e.g. `2024-03-10`)                            |
| `status`        | string | Current status (e.g. Open, Closed, Under review)                          |
| `skills`        | array  | Desired skills (e.g. `["Python", "AWS", "Testing"]`)                      |


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
