# DClaw Code — v1.2 Feature Roadmap

> Based on: Y Combinator vertical SaaS principles, trending GitHub repos (gitpod, coder), AI product research (Cursor, Replit, GitHub Copilot, CodeSandbox)

## Pre-Flight Checklist

- [ ] `frontend/package-lock.json` committed after any `npm install` / dependency change
- [ ] `frontend/next-env.d.ts` exists and is committed
- [ ] `docker-compose.yml` healthchecks correct
- [ ] `frontend/Dockerfile` declares `ARG NEXT_PUBLIC_API_URL` before `RUN npm run build`

## v1.0 Feature Inventory (Current)

- [ ] Code repository browser
- [ ] File editor with syntax highlighting
- [ ] Terminal/shell access
- [ ] Project/workspace management
- [ ] Real backend CRUD (no mocks)
- [ ] Docker + Helm deployment
- [ ] Alembic migrations
- [ ] Backend tests

---

## v1.2 Roadmap

### P0 — Must Have (Ship in v1.0, demo-ready)

#### 1. AI Code Copilot (Pair Programmer)
**Description:** AI assistant embedded in the IDE that suggests code, explains functions, finds bugs, and writes tests. "Write a Python function to parse this JSON schema."
- **AI Angle:** Code completion (LLM). RAG over codebase. Inline chat.
- **Backend:** `/api/v1/ai/code-chat` endpoint. Code context extraction.
- **Frontend:** Monaco/ACE editor with AI sidebar. Inline suggestion widget.
- **Files:** `backend/app/services/code_ai.py`, `frontend/src/components/code-copilot.tsx`

#### 2. Cloud Development Environment (CDE)
**Description:** Spin up containerized dev environments from repo with one click. Pre-configured toolchains.
- **Backend:** Docker-in-Docker orchestration. Environment template engine.
- **Frontend:** Environment launcher. Resource monitor.
- **Files:** `backend/app/services/cde.py`

#### 3. Code Review & PR Assistant
**Description:** AI-generated PR summaries, code review comments, and security scanning.
- **AI Angle:** Diff analysis + LLM review suggestions. Security pattern detection.
- **Backend:** Git webhook handler. Review generation pipeline.
- **Frontend:** PR dashboard with AI review cards.
- **Files:** `backend/app/services/pr_ai.py`

#### 4. Real-Time Collaboration
**Description:** Multi-cursor editing, live cursors, voice chat, and pair programming sessions.
- **Backend:** WebSocket sync engine. Presence management.
- **Frontend:** Collaborative editor with user cursors and avatars.
- **Files:** `backend/app/services/collaboration.py`

### P1 — Should Have (v1.1–1.2)

#### 5. AI Test Generator
**Description:** Auto-generate unit tests, integration tests, and edge cases from code.
- **Backend:** `/api/v1/ai/generate-tests` endpoint.
- **Frontend:** Test explorer with AI-generated test suggestions.

#### 6. Dependency & Vulnerability Scanning
**Description:** Scan dependencies for CVEs. Suggest upgrades. License compliance check.
- **Backend:** Snyx/OSV integration. License scanner.
- **Frontend:** Security dashboard with vulnerability list.

#### 7. CI/CD Pipeline Builder
**Description:** Visual pipeline builder with pre-built templates. GitHub Actions/GitLab CI export.
- **Backend:** Pipeline definition generator.
- **Frontend:** Drag-and-drop pipeline canvas.

#### 8. Documentation Generator
**Description:** Auto-generate README, API docs, and inline comments from code.
- **AI Angle:** LLM docstring generation. API spec extraction.
- **Backend:** `/api/v1/ai/generate-docs` endpoint.
- **Frontend:** Doc preview with export to Markdown/OpenAPI.

### P2 — Could Have (v1.3+)

#### 9. AI Refactoring Agent
**Description:** AI agent that performs large-scale refactoring across the codebase with human approval.

#### 10. Performance Profiler & Optimizer
**Description:** Identify bottlenecks and AI-suggest optimizations with predicted impact.

#### 11. Multi-Repo Search & Navigation
**Description:** Code search across all connected repos with semantic understanding.

#### 12. AI Debugging Assistant
**Description:** Paste an error trace. AI identifies root cause and suggests fixes.

---

## Implementation Priority

1. **Week 1–2:** AI Code Copilot (P0.1) + Cloud Dev Environment (P0.2)
2. **Week 3–4:** Code Review AI (P0.3) + Real-Time Collaboration (P0.4)
3. **Week 5–6:** Test Generator (P1.5) + Vulnerability Scanning (P1.6)
4. **Week 7–8:** CI/CD Builder (P1.7) + Documentation AI (P1.8)
