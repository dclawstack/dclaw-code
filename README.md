# DClaw Code

**AI-native IDE inside your desktop**

An AI-powered integrated development environment with code completion, refactoring, explanation, and test generation.

[![Build Backend](https://github.com/dclawstack/dclaw-code/actions/workflows/build-backend.yml/badge.svg)](https://github.com/dclawstack/dclaw-code/actions/workflows/build-backend.yml)
[![Build Frontend](https://github.com/dclawstack/dclaw-code/actions/workflows/build-frontend.yml/badge.svg)](https://github.com/dclawstack/dclaw-code/actions/workflows/build-frontend.yml)

## Quick Start

```bash
git clone https://github.com/dclawstack/dclaw-code.git
cd dclaw-code
docker compose up -d

# Backend API: http://localhost:8094
# Frontend UI: http://localhost:3005
```

## Backend API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/api/v1/code/completion` | AI code completion |
| POST | `/api/v1/code/refactor` | Code refactoring |
| POST | `/api/v1/code/explain` | Explain code |
| POST | `/api/v1/code/generate-tests` | Generate unit tests |
| GET | `/api/v1/code/projects` | List projects |
| POST | `/api/v1/code/projects` | Create project |
| GET | `/api/v1/code/files` | List files |
| POST | `/api/v1/code/files` | Create file |
| GET | `/api/v1/code/snippets` | List snippets |
| POST | `/api/v1/code/snippets` | Create snippet |
| POST | `/api/v1/code/chat/messages` | Send chat message |

## Frontend Pages

| Route | Feature |
|-------|---------|
| `/` | Dashboard with projects and stats |
| `/editor` | Monaco Editor + AI chat sidebar |
| `/chat` | Code-focused chat |
| `/projects` | Project management |
| `/settings` | Model selection and config |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, SQLAlchemy 2.0, Pydantic v2, asyncpg |
| Frontend | Next.js 16, TypeScript, Tailwind CSS, shadcn/ui |
| Database | PostgreSQL 16 (CloudNativePG in K8s) |
| LLM | Ollama (local) / OpenRouter (cloud) |

## Ports

| Service | Port |
|---------|------|
| Backend API | 8094 |
| Frontend Dev | 3005 |
| PostgreSQL | 5432 |

## Deployment

### Docker Compose
```bash
docker compose up -d
```

### Kubernetes (Helm)
```bash
helm upgrade --install dclaw-code ./helm/dclaw-code \
  --namespace dclaw --create-namespace
```

## DClaw Stack

Part of the [DClaw Stack](https://github.com/dclawstack) — an AI-native application platform.
