---
tags: [meta, prd, revised, swarm]
version: 2.3
date: 2026-05-16
app_id: code
app_name: DClaw Code
category: Development
status: P2
---

# 📘 DClaw Code — Revised PRD v2.3

> **The single document every agent must read before writing code for this app.**
> Generated from DClaw Master PRD v2.2. Read the Master PRD first: https://raw.githubusercontent.com/dclawstack/dclaw-prd/main/DClaw-Master-PRD.md

---

## 1. Product Identity

| Field | Value |
|-------|-------|
| **App ID** | `code` |
| **Name** | DClaw Code |
| **Category** | Development |
| **Tagline** | AI-native IDE |
| **Color** | #1F2937 |
| **Phase** | P2 |
| **Port (Frontend Dev)** | 3006 (Assigned) |
| **Port (Backend Dev)** | 8094 (Assigned) |
| **Maturity Tier** | 🟢 Tier 1 — Mature |

---

## 2. Current State Assessment

### 2.1 Scaffold Status
| Component | Status | Notes |
|-----------|--------|-------|
| `frontend/` | ✅ | Next.js 14+ app |
| `backend/` | ✅ | FastAPI + SQLAlchemy 2.0 |
| `docs/` | ✅ | getting-started, guides, reference, releases |
| `helm/` | ✅ | K8s deployment manifests |
| `.github/workflows/` | ✅ | CI/CD + Claude integration |
| `AGENTS.md` | ✅ | Per-repo agent instructions |
| `PLAN-v1.2.md` | ✅ | Feature roadmap |
| `docker-compose.yml` | ✅ | Local dev stack |
| `tests/` | ✅ | pytest + pytest-asyncio |
| `alembic/` | ✅ | Database migrations |
| `dclaw-manifest.json` | ✅ | DPanel registration |

### 2.2 Code Maturity
| Metric | Value |
|--------|-------|
| Python source files (backend) | ~40 |
| TypeScript/TSX files (frontend) | ~28 |
| Total source files | ~68 |
| Tests | ✅ Present |
| Alembic migrations | ✅ Present |
| DPanel manifest | ✅ Present |

### 2.3 Feature Maturity
- **P0 Foundation:** Partially implemented
- **P1 Platform:** Not yet started
- **P2 Vertical:** Not yet started

---

## 3. Gap Analysis

| # | Gap | Severity | Fix |
|---|-----|----------|-----|
| 1 | No critical gaps identified — focus on P1/P2 features | 🟢 | Continue building P1 features and add depth to existing code |

---

## 4. Sacred Architecture & Tech Stack

> **NON-NEGOTIABLE. Every DClaw product MUST use this exact stack.**

| Layer | Technology | Version |
|-------|------------|---------|
| **Frontend** | Next.js 14+ | App Router, Tailwind CSS, shadcn/ui |
| **Backend** | FastAPI | Pydantic v2, SQLAlchemy 2.0, asyncpg |
| **Database** | PostgreSQL 16 | CloudNativePG operator in K8s |
| **Vector DB** | Qdrant / pgvector | Only if RAG / semantic search |
| **Cache / Bus** | Redis | 7.x |
| **Object Storage** | MinIO | Latest |
| **Workflow** | Temporal.io | Only if automation/orchestration |
| **Auth** | Logto | JWT validation on all protected routes |
| **Billing** | Stripe | Metered or per-seat |
| **K8s Operator** | Go + controller-runtime | 0.18 |
| **LLM Local** | Ollama | Apple Silicon |
| **LLM Cloud** | OpenRouter + Kimi K2.5 | Fallback |
| **Monitoring** | Prometheus + Grafana | Latest |

### 4.1 Python Rules
- `ruff` formatting enforced
- Type hints on ALL public APIs
- `pydantic` v2 for schemas
- `sqlalchemy` 2.0 style (`Mapped`, `mapped_column`)
- `pytest` + `pytest-asyncio` for tests
- Functions < 50 lines
- No `print()` — use `structlog`

### 4.2 TypeScript / Next.js Rules
- Strict TypeScript (`strict: true`)
- Tailwind for ALL styling
- `cn()` utility for conditional classes
- No `any` without `// @ts-ignore`

### 4.3 Docker Standards
- Port mappings MUST match container listen port
- Healthchecks MUST use binaries present in base image
- `docker compose config` must pass before shipping
- Service type MUST be `ClusterIP`
- TLS required on all ingress

---

## 5. P0 Foundation Features (Must Have — Demo Ready)

> **Every P0 MUST include an AI Copilot per YC S25/W26 RFS.**

| # | Feature | Description | AI Component | Acceptance Criteria |
|---|---------|-------------|--------------|---------------------|
| P0.1 | **AI Code Copilot** | Intelligent code completion, explanation, and generation in 30+ languages. | CodeLlama/StarCoder fine-tuned + RAG over codebase | Autocomplete latency <200ms; explain selected code in <3s |
| P0.2 | **Monaco Editor Integration** | Full-featured code editor with syntax highlighting, IntelliSense, and debugging. | AI error-explanation + fix suggestion | Support 30+ languages; breakpoints; variable inspection |
| P0.3 | **Project & Repository Management** | Create projects, manage files, and integrate with Git. | AI commit-message generation + PR description | Git clone/commit/push/PR; file tree explorer; diff viewer |
| P0.4 | **Terminal & Execution** | In-browser terminal for running code, tests, and commands. | AI command suggestion + explanation | Bash terminal; language-specific REPL; output streaming |

---

## 6. P1 Platform Features (Should Have — v1.1–1.2)

| # | Feature | Description | AI Component | Acceptance Criteria |
|---|---------|-------------|--------------|---------------------|
| P1.1 | **Code Review AI** | Automated code review with style, security, and logic checks. | Static analysis + LLM explanation + fix suggestion | Review 500 LOC in <10s; 50+ rule categories |
| P1.2 | **Live Collaboration** | Real-time pair programming with cursors and voice. | AI conflict-resolution + merge-strategy suggestion | 5 concurrent editors; live cursors; voice chat integration |
| P1.3 | **Deployment Integration** | Deploy to Vercel, K8s, or VPS directly from the IDE. | AI deployment-risk assessment + rollback recommendation | One-click deploy; preview URL; rollback to previous version |
| P1.4 | **Debugging Assistant** | AI-powered debugging that suggests root causes and fixes. | LLM stack-trace analysis + variable-state inference | Explain errors in plain English; suggest 3 fixes with confidence scores |

---

## 7. P2 Vertical / Scale Features (Could Have — v1.3+)

| # | Feature | Description | AI Component | Acceptance Criteria |
|---|---------|-------------|--------------|---------------------|
| P2.1 | **Custom Extensions** | Build and install IDE extensions for custom workflows. | AI extension-template generation | Extension API; marketplace; 10+ hook points |
| P2.2 | **Performance Profiling** | Identify bottlenecks with flame graphs and memory analysis. | AI hotspot prediction + optimization suggestion | CPU + memory profiling; export flame graph; suggest 3 optimizations |
| P2.3 | **Documentation Generator** | Auto-generate README, API docs, and inline comments. | LLM doc generation + code-structure analysis | Generate README from codebase in <30s; docstring all public APIs |
| P2.4 | **Mobile Preview** | Preview web apps on simulated mobile devices. | AI responsive-issue detection | 10 device presets; touch simulation; rotate/orientation test |

---

## 8. Scaffold Checklist

Before marking this app "shipped", confirm:

- [ ] `frontend/` with Next.js 14+, Tailwind, shadcn/ui
- [ ] `backend/` with FastAPI, Pydantic v2, SQLAlchemy 2.0, asyncpg
- [ ] `docs/` with getting-started, guides, reference, releases, troubleshooting
- [ ] `helm/` with Chart.yaml, values.yaml, templates (deployment, service, ingress, cloudnativepg)
- [ ] `.github/workflows/` with build-backend.yml, build-frontend.yml, deploy.yml, claude.yml
- [ ] `frontend/public/dclaw-manifest.json` for DPanel registration
- [ ] `backend/tests/` with pytest + pytest-asyncio
- [ ] `backend/alembic/` with initial migration
- [ ] `Dockerfile` + `docker-compose.yml` with correct healthchecks
- [ ] Health endpoint at `/health` returning `{"status":"ok"}`
- [ ] `AGENTS.md` with per-repo instructions
- [ ] `PLAN-v1.2.md` with feature roadmap
- [ ] Port assigned from registry and documented
- [ ] No hardcoded secrets — use `.env.example` + K8s Secrets
- [ ] Non-root containers in Dockerfile

---

## 9. AI Copilot Mandate (YC S25/W26 Requirement)

Every DClaw app MUST have an AI Copilot as its first P0 feature. The copilot must:
1. Be contextually aware of the app's domain data
2. Use RAG over the app's knowledge base where applicable
3. Suggest next actions, not just answer questions
4. Be accessible from every page via floating chat or sidebar
5. Fall back to local Ollama when cloud is unavailable

---

## 10. Next Tasks for Vibe Coders

1. **Complete P0 features**: Finish any incomplete P0 backend services and frontend pages.
2. **Add missing scaffold**: Fill gaps identified above (docs, helm, tests, manifest, etc.).
3. **Start P1 features**: Implement the first 2 P1 features to deepen domain capability.
4. **Polish and integrate**: Ensure health endpoints, Docker builds, and DPanel manifest are production-ready.

---

## 11. Domain Research Notes

Inspired by VS Code, Cursor, GitHub Copilot, Replit. AI IDE is the most used dev tool; YC deeply interested.

---

## 12. Links & Resources

| Resource | URL |
|----------|-----|
| **Master PRD** | https://raw.githubusercontent.com/dclawstack/dclaw-prd/main/DClaw-Master-PRD.md |
| **GitHub Org** | https://github.com/dclawstack |
| **DPanel** | https://dpanel.dclawstack.io |
| **Port Registry** | See `dclaw-platform/PORT_REGISTRY.md` |
| **App PRD Template** | Obsidian Vault → `00-META/📐 App PRD Template.md` |
| **Scaffold Source** | `dclaw-scaffold/` in DClaw-Stack |

---

*Revised PRD version: 2.3*
*Generated: 2026-05-16 by DClaw Stack Generator*
*Next review: When P0 features are complete or architecture changes*
