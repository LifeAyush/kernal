# Kernal

Personal workbench for managing work across apps.

- Product intent: [`docs/initial_context.md`](docs/initial_context.md)
- Stack: [`docs/tech_stack.md`](docs/tech_stack.md)
- Agent rules: [`.cursor/rules/`](.cursor/rules/) (`backend-typing.mdc`, `frontend-component-files.mdc`)
- Skills: [`.cursor/skills/`](.cursor/skills/) (`update-agent-rules`)

This repo is a uv workspace (Python) plus a Vite React app. Local setup only — no deploy yet.

Python packages live only in the **repo-root `.venv`** (gitignored). `uv sync` creates it. Do not `pip install --user`, do not use the system interpreter, and do not create a second env named `venv`.

## Requirements

Host tools only — not project libraries:

- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- Node.js 20+ and npm

## Setup

```bash
# Creates / uses .venv and installs core, api, linkedin, cli
uv sync

# Frontend (project-local node_modules)
cd apps/web
cp .env.example .env
npm install
```

Optional API env (CORS defaults to `http://localhost:5173` if omitted):

```bash
cp apps/api/.env.example apps/api/.env
```

## Run locally

Activate `.venv` before any Python command. Do not start the API or CLI with `uv run` or the system interpreter.

```bash
uv sync
source .venv/bin/activate
uvicorn kernal_api.main:app --reload --port 8000
```

In another terminal:

```bash
cd apps/web
npm run dev
```

- API: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)
- UI: [http://localhost:5173](http://localhost:5173) (proxies `/api` to the backend)

CLI (after `source .venv/bin/activate`):

```bash
kernal
```

## Layout

| Path | Import / role |
| --- | --- |
| `core/` | `kernal_core` — storage, context, llm, workflow lifecycle |
| `apps/api/` | `kernal_api` — FastAPI |
| `apps/linkedin/` | `kernal_linkedin` — LinkedIn module (stubs) |
| `apps/web/` | Vite + React + TypeScript |
| `apps/web/src/App/` | First component directory (`index.tsx`, `types.ts`, `helpers.ts`, `styles.css`) |
| `cli/` | `kernal_cli` — local session-bound work |
| `docs/` | Product and stack briefs |
| `.cursor/rules/` | Agent coding rules (always apply) |
| `.cursor/skills/` | Agent skills (e.g. `update-agent-rules`) |

## Contributing

For people and agents:

- Install and run Python only via the repo-root `.venv`: `uv sync` then `source .venv/bin/activate`. No host `pip`. No `uv run` for app commands.
- Backend: follow [`.cursor/rules/backend-typing.mdc`](.cursor/rules/backend-typing.mdc).
- Frontend components: follow [`.cursor/rules/frontend-component-files.mdc`](.cursor/rules/frontend-component-files.mdc).
- New convention from a snippet: use the `update-agent-rules` skill — add a new `.mdc` or extend the same concern.
- Do not commit `.env` or `.venv`.
