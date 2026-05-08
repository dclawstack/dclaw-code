# DClaw Code — Agent Development Guide

> **Read this file first before making any code changes.**
> This document is the source of truth for architecture, anti-patterns, and development workflow.

## App Identity

**DClaw Code** is an AI-native IDE. It provides project management, file editing with Monaco Editor, code snippets, AI chat, and LLM-powered code completion, refactoring, explanation, and test generation.

- **Backend Port:** `8094` (FastAPI)
- **Frontend Port:** `3005` (Next.js)
- **Database:** `dclaw_code` (PostgreSQL)
- **Base API Path:** `/api/v1/code`

## Architecture Lock — DO NOT CHANGE

These are non-negotiable. If an agent suggests changing them, reject it.

### Backend
- **FastAPI** with `lifespan` handler
- **SQLAlchemy 2.0** — `DeclarativeBase` from `app.models.base`, NOT `declarative_base()`
- **Pydantic v2** schemas with `ConfigDict(from_attributes=True)`
- **Async SQLAlchemy** — `create_async_engine` + `AsyncSession`
- **Repository pattern** — all DB access through `app/repositories/`
- **Dependency injection** — `Depends(get_db)`, never manual `AsyncSession`
- **NO MOCK DATA** — never use in-memory `dict`s

### Frontend
- **Next.js 14+ App Router**
- **Tailwind CSS** + **shadcn/ui**
- **Monaco Editor** via `@monaco-editor/react` for code editing
- **API client** in `src/lib/api.ts` — typed fetch wrapper
- **Environment variables** — `NEXT_PUBLIC_API_URL` baked at build time. Dockerfile MUST declare `ARG NEXT_PUBLIC_API_URL`.

### Docker
- **Backend:** `python:3.11-slim`, non-root `appuser`, healthcheck with `python urllib.request.urlopen()`
- **Frontend:** `node:20-alpine`, port `3005`
- **Compose:** container port MUST match `EXPOSE`/`ENV PORT`

## Directory Structure

```
dclaw-code/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── main.py
│   │   │   ├── routes/
│   │   │   │   └── health.py
│   │   │   └── v1/
│   │   │       └── code/
│   │   │           ├── __init__.py      # Router aggregator
│   │   │           ├── projects.py      # Project CRUD
│   │   │           ├── files.py         # File CRUD
│   │   │           ├── snippets.py      # Snippet CRUD
│   │   │           └── chat.py          # Chat + AI tools
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── database.py            # Base(DeclarativeBase), engine, get_db
│   │   ├── models/
│   │   │   ├── base.py
│   │   │   ├── project.py
│   │   │   ├── file.py
│   │   │   ├── snippet.py
│   │   │   └── chat_message.py
│   │   ├── repositories/              # CRUD layer
│   │   ├── schemas/                   # Pydantic v2
│   │   └── services/
│   │       └── code_service.py        # LLM proxy (Ollama → OpenRouter → mock)
│   ├── alembic/
│   ├── tests/
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/                       # Next.js App Router
│   │   │   ├── editor/
│   │   │   ├── chat/
│   │   │   ├── projects/
│   │   │   └── settings/
│   │   ├── components/
│   │   │   └── ui/                    # shadcn/ui
│   │   └── lib/
│   │       └── api.ts
│   └── Dockerfile
├── docker-compose.yml
├── helm/
└── .env.example
```

## Anti-Patterns — NEVER DO

| Anti-Pattern | Why It Breaks Things | Correct Alternative |
|--------------|---------------------|---------------------|
| `declarative_base()` in `database.py` | Separate metadata → zero tables | `from app.models.base import Base` |
| `curl` in healthcheck on `python:*-slim` | No `curl` → silent failure | `python -c "import urllib.request; urllib.request.urlopen(...)"` |
| In-memory `MOCK_*` dicts | Data lost on restart | Create repository + real DB |
| Missing `ARG NEXT_PUBLIC_API_URL` | Wrong API URL baked in | Add `ARG NEXT_PUBLIC_API_URL` before build |
| Manual `get_db()` with `__anext__()` | Session leaks | `Depends(get_db)` |
| Hardcoded `localhost:PORT` | Breaks Docker/K8s | Use `process.env.NEXT_PUBLIC_API_URL` |
| Plain `<Textarea>` for code editing | No syntax highlighting, no IntelliSense | Use `@monaco-editor/react` |
| No alembic migration for new models | Schema drift | `alembic revision --autogenerate` |

## Database Rules

1. All models MUST inherit from `Base` in `app.models.base`
2. All models MUST use `Mapped[...]` and `mapped_column()`
3. Relationships MUST specify `lazy="selectin"`
4. All new tables MUST get an alembic migration
5. `ondelete="CASCADE"` for child tables (files, snippets)
6. `ondelete="SET NULL"` for optional refs (chat messages → project)

## How to Add a Feature

1. **Read this file** and `PLAN-v1.2.md`
2. **Backend:**
   - Add/update model in `app/models/`
   - Add/update schema in `app/schemas/`
   - Add repository in `app/repositories/`
   - Add/update router in `app/api/v1/code/`
   - Wire router in `app/api/v1/code/__init__.py`
   - Add tests in `tests/`
   - Generate alembic migration
3. **Frontend:**
   - Add API types/functions to `src/lib/api.ts`
   - Add page in `src/app/` or component
   - Use Monaco Editor for any code editing surface
4. **Docker:** Verify `docker compose config` and `docker compose up -d`
5. **Commit** with conventional commit message

## Testing Requirements

- Every new repository MUST have tests
- Every new router endpoint MUST be covered
- Use `pytest-asyncio` with `async` test functions
- Use `httpx.AsyncClient` with `ASGITransport`
- Override `get_db` dependency with test session

## Port Registry

| Service | Host Port | Container Port |
|---------|-----------|----------------|
| code-frontend | 3005 | 3005 |
| code-backend | 8094 | 8094 |
| code-postgres | 5432 | 5432 |
