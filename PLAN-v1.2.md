# DClaw Code — v1.2 Feature Roadmap

> **For coding agents:** Pick features from this list, implement them fully, and update this doc with a checkmark.
> **Do NOT change the basic stack.** See `AGENTS.md` for architecture lock.

## Pre-Flight Checklist — Do This First

Before implementing any v1.2 feature, verify:

- [ ] `frontend/package-lock.json` is committed after any `npm install` / dependency change
- [ ] `frontend/next-env.d.ts` exists and is committed (required for Next.js TypeScript builds)
- [ ] `frontend/.gitignore` excludes `node_modules/` and `.next/`
- [ ] `docker-compose.yml` healthchecks use `python urllib.request.urlopen()` (backend) and `wget -q --spider` (frontend)
- [ ] `frontend/Dockerfile` declares `ARG NEXT_PUBLIC_API_URL` before `RUN npm run build`

## v1.0 Feature Inventory (Current)

- [x] Project CRUD with metadata
- [x] File CRUD with content storage
- [x] Snippet CRUD with tags
- [x] AI chat with project context
- [x] Monaco Editor for code editing
- [x] AI code completion (Ollama → OpenRouter → mock)
- [x] AI code refactor, explain, test generation
- [x] Docker + Helm deployment
- [x] Alembic migrations
- [x] Backend tests

---

## v1.2 Roadmap

### P0 — Must Have

#### 1. Git Integration
**Description:** Clone, commit, push, and view diff history for projects.
- **Backend:** Add `GitService` using `GitPython` or shelling out to `git`. Endpoints: `POST /projects/{id}/git/clone`, `GET /projects/{id}/git/status`, `POST /projects/{id}/git/commit`, `GET /projects/{id}/git/log`, `GET /projects/{id}/git/diff`.
- **Frontend:** Git panel in the editor sidebar showing changed files, diff viewer, commit message input, branch selector.
- **Files to touch:** `backend/app/services/git_service.py`, `backend/app/api/v1/code/git.py`, `frontend/src/app/editor/GitPanel.tsx`

#### 2. File Tree Explorer
**Description:** A proper file tree with folders, drag-and-drop, context menus.
- **Backend:** Add `GET /projects/{id}/files/tree` to return nested directory structure.
- **Frontend:** Replace flat file list with a collapsible file tree component. Right-click context menu (new file, new folder, rename, delete). Drag-and-drop to move files.
- **Files to touch:** `backend/app/api/v1/code/files.py`, `frontend/src/components/FileTree.tsx`, `frontend/src/app/editor/page.tsx`

#### 3. Multi-File AI Context
**Description:** When asking the AI to complete/refactor code, include related files from the project as context.
- **Backend:** Add context gathering logic in `code_service.py` — find imports, same-directory files, and recently edited files. Send them in the LLM prompt as "additional context".
- **Frontend:** Show a "Context files" panel in the AI chat sidebar. Let users pin/unpin files for context.
- **Files to touch:** `backend/app/services/code_service.py`, `backend/app/api/v1/code/chat.py`, `frontend/src/app/chat/page.tsx`

#### 4. Terminal / Shell Execution
**Description:** An integrated terminal that runs commands in the backend container.
- **Backend:** Use `asyncio.create_subprocess_shell` with strict allowlists. `POST /api/v1/code/terminal/exec` takes command, returns stdout/stderr. Security: whitelist allowed commands, timeout 30s, block dangerous ops (`rm -rf /`, `curl | bash`).
- **Frontend:** Terminal emulator component (xterm.js or simple output stream). Command input at bottom.
- **Files to touch:** `backend/app/services/terminal_service.py`, `backend/app/api/v1/code/terminal.py`, `frontend/src/components/Terminal.tsx`

### P1 — Should Have

#### 5. Code Review Workflow
**Description:** Create and manage code review threads on specific lines of code.
- **Backend:** Add `CodeReview` and `ReviewComment` models. Endpoints for creating reviews, adding line-level comments, resolving threads.
- **Frontend:** Inline comment bubbles in Monaco Editor gutter. Review sidebar with open/resolved threads.
- **Files to touch:** `backend/app/models/code_review.py`, `backend/app/repositories/code_review_repo.py`, `backend/app/api/v1/code/reviews.py`, `frontend/src/components/editor/InlineComments.tsx`

#### 6. Dark / Light Theme Toggle
**Description:** Support both themes across the entire app.
- **Backend:** No changes needed.
- **Frontend:** Add `next-themes` provider. Configure shadcn/ui themes. Ensure Monaco Editor switches themes (`vs` vs `vs-dark`).
- **Files to touch:** `frontend/src/app/layout.tsx`, `frontend/src/components/ThemeToggle.tsx`

#### 7. LSP Integration
**Description:** Connect to Language Servers for IntelliSense, go-to-definition, hover info.
- **Backend:** Run LSP servers in containers (typescript-language-server, pylsp, rust-analyzer). Proxy LSP JSON-RPC over WebSocket or HTTP.
- **Frontend:** Use Monaco Editor's LSP client (`monaco-languageclient`).
- **Files to touch:** `backend/app/services/lsp_service.py`, `frontend/src/lib/monaco-lsp.ts`

#### 8. Settings Persistence
**Description:** User preferences (theme, font size, editor config, default LLM model) persisted per user.
- **Backend:** Add `UserSettings` model. CRUD endpoints.
- **Frontend:** Settings page with form controls. Load settings on app mount.
- **Files to touch:** `backend/app/models/user_settings.py`, `backend/app/api/v1/code/settings.py`, `frontend/src/app/settings/page.tsx`

### P2 — Could Have

#### 9. Collaborative Editing
**Description:** Multiple users editing the same file simultaneously.
- **Backend:** WebSocket server with Yjs CRDT protocol or Operational Transformation.
- **Frontend:** Monaco Editor with `y-monaco` binding.

#### 10. CI/CD Pipeline Viewer
**Description:** Show GitHub Actions or GitLab CI status for the project.
- **Backend:** Integrate with GitHub/GitLab API. Cache pipeline status.
- **Frontend:** Status badges in project list. Pipeline details page.

---

## Implementation Priority

1. Git Integration (core developer workflow)
2. File Tree Explorer (navigation)
3. Multi-File AI Context (AI quality)
4. Terminal / Shell Execution (power user)
5. Code Review Workflow (team collaboration)
6. Settings Persistence (UX polish)
7. Dark / Light Theme Toggle (accessibility)
8. LSP Integration (developer experience)
9. Collaborative Editing (advanced)
10. CI/CD Pipeline Viewer (integration)
