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
- Simple DI wiring sets a singleton `ItemsService` at startup.
- Swap storage by implementing a new repository matching `RepositoryProtocol`.
- Configure MongoDB TLS trust by setting `MONGO_TLS_CA_FILE` (defaults to the `certifi` bundle when available).
