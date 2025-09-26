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
- Candidaturas CRUD under: `/api/v1/candidaturas`

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

### Candidaturas payload

| Campo                 | Tipo         | Descrição                                                             |
| --------------------- | ------------ | --------------------------------------------------------------------- |
| `company_id`          | string       | Identificador único da empresa associada                              |
| `name`                | string       | Nome da empresa                                                       |
| `email`               | string       | E-mail corporativo usado para login e contato                         |
| `password_hash`       | string       | Hash da senha para autenticação                                       |
| `phone`               | string       | Telefone de contato                                                   |
| `website`             | string (URL) | Website oficial                                                       |
| `location.city`       | string       | Cidade onde a empresa está localizada                                 |
| `location.state`      | string       | Estado onde a empresa está localizada                                 |
| `location.country`    | string       | País onde a empresa está localizada                                   |
| `about`               | string       | Descrição da empresa                                                  |
| `industry`            | string       | Setor de atuação (ex: Tecnologia, Saúde)                              |
| `size`                | string       | Tamanho da empresa (ex: `1-10`, `11-50`, `201-500`)                   |
| `founded_year`        | number       | Ano de fundação                                                       |
| `social_links.linkedin` | string (URL) | Link para o LinkedIn corporativo                                      |
| `social_links.instagram` | string (URL) | Link para o Instagram corporativo                                     |
| `logo_url`            | string (URL) | URL com o logo da empresa                                             |
| `created_at`          | string (ISO 8601) | Data de criação do cadastro                                        |
| `updated_at`          | string (ISO 8601) | Data da última atualização do cadastro                              |

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
