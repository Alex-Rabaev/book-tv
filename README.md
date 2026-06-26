# book-tv

Turn a book title into AI-generated images of its characters. Type a title → an agent
finds the book and confirms it by cover → pick a key character → generate an image → save it.

Full-stack: **React + TypeScript** (Vite) frontend, **FastAPI** backend, **PostgreSQL**,
**Supabase Storage** for images, **OpenAI** for character extraction and image generation.

See planning artifacts in `_bmad-output/planning-artifacts/` (PRD, architecture spine, epics).

## Repository layout

```
backend/     FastAPI service (layered: api / services / repositories / models / schemas / adapters / core)
frontend/    Vite + React + TypeScript SPA
docker-compose.yml   Local Postgres (+ optional API) for end-to-end runs
.env.example         Required environment variables (copy to .env)
```

## Prerequisites

- Python 3.12+
- Node.js 24 LTS (works on 22+) and npm
- Docker (for local Postgres via docker-compose), or your own PostgreSQL 16+

## Setup

```bash
cp .env.example .env   # fill in JWT_SECRET, OPENAI_API_KEY, SUPABASE_* (leave blank for scaffold-only run)
```

### Database (local Postgres via Docker)

```bash
docker compose up -d db
```

### Backend

```bash
cd backend
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt
alembic upgrade head        # apply migrations (requires a running Postgres)
uvicorn app.main:app --reload   # serves http://localhost:8000  (GET /health)
pytest                      # run backend tests
```

### Frontend

```bash
cd frontend
npm install
npm run dev                 # serves http://localhost:5173
npm test                    # run vitest
npm run build               # tsc -b && vite build
```

## Conventions (from the architecture spine)

- Secrets live only in the backend env (`pydantic-settings`); the frontend talks only to the API.
- Schema changes go through Alembic migrations only — never runtime `create_all`.
- UUIDv4 primary keys, UTC ISO-8601 timestamps, one JSON error envelope.
