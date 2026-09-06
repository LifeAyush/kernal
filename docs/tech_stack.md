# Kernal tech stack

Agent-facing brief. **Read this before implementing.** Product intent, workflows, and architecture principles live in [`initial_context.md`](initial_context.md). This file only locks languages, hosting, persistence, and the rules that keep those choices from leaking into workflow code.

If a decision here conflicts with a convenience in a vendor SDK, this file wins.

## Locked stack

| Piece | Choice |
|---|---|
| Backend | Python + FastAPI (ASGI / uvicorn) |
| Frontend | Vite + React + TypeScript (SPA; no SSR in v1) |
| Frontend host | Cloudflare Pages (`apps/web` → `dist/`) |
| Backend host | Google Cloud Run (Dockerfile, scale to zero) |
| Context / memory | Supabase **Postgres only**, via `DATABASE_URL` |
| Scheduler | GitHub Actions cron → authenticated FastAPI routes (or Cloud Run Jobs) |
| LLM | `core/llm` interface; default **Sarvam 105B** (`complete(prompt) -> str`) |
| Secrets | Platform env vars. Never commit keys |
| Auth (v1) | CORS locked to the Pages origin; cron/workflow routes gated by `CRON_SECRET`. No user-auth system |
| Local Python | Repo-root **`.venv` only** (via `uv sync` / `uv run`) |

## Local Python environment

Install and run Python only through the project venv:

- `uv sync` — creates/updates **repo-root `.venv`**
- `source .venv/bin/activate` then run `uvicorn` / `kernal` — do not use `uv run` for app commands
- Host tools allowed: `uv`, Python 3.12, Node/npm
- Do **not** `pip install`, `pip install --user`, or `brew install` FastAPI, ruff, or any project library onto the machine
- Do **not** use a second venv (`venv/`, per-package envs, or a global interpreter)

Frontend deps stay in `apps/web/node_modules`.

## Supabase is a dumb memory layer

Supabase exists so workflows can persist and reuse context (people seen, posts surfaced, drafts, interests, history). It is **not** the application backend.

**Do**

- Connect FastAPI with `DATABASE_URL` (SQLAlchemy or asyncpg) to the Supabase Postgres instance.
- Put all reads/writes behind `core/storage` (and `core/context`). Tables and SQL live there.
- Treat generated files (carousels, decks) the same way: an object/blob interface on `core/storage`. If the implementation uses a Supabase Storage bucket, workflows still must not import Supabase.
- Rely on daily/weekly GitHub Actions jobs to keep the free project from the **7-day inactivity pause**. If cron might not run for a week, add a tiny heartbeat query. A paused project does not auto-wake.

**Do not**

- Use PostgREST, `supabase-py`, or the JS client as the primary data API.
- Use Supabase Auth, Realtime, Edge Functions, or RLS as the app’s security/session model.
- Import `supabase` (or any vendor SDK) from `apps/linkedin/` or any workflow.
- Point the Vite app at Supabase. The browser talks only to FastAPI.
- Use local `data/`, SQLite, or the Cloud Run filesystem as source of truth.

Daily cron (`linkedin.find_people`, `linkedin.engage_posts`) counts as activity and should prevent pause under normal use. Do not assume that if someone disables the schedule.

### Setting `DATABASE_URL`

1. In Supabase: Project Settings → Database → connection string (URI). Prefer the **session** pooler or direct URI. Add `sslmode=require` if it is not already in the query string.
2. Put it in `apps/api/.env` as `DATABASE_URL=postgresql://...` (never commit `.env`).
3. Optional: run [`core/src/kernal_core/storage/schema.sql`](../core/src/kernal_core/storage/schema.sql) in the Supabase SQL editor before the API has a URL. When `DATABASE_URL` is set, the API also runs `create_all` on startup.
4. SQLAlchemy is configured as `postgresql+psycopg://` automatically. Do not add `supabase-py` or the JS client.

## LLM

- Workflows call `core/llm` only. No vendor SDK in app modules.
- Default: Sarvam 105B via `kernal_core.llm.complete`. Key: `SARVAM_API_KEY`. Optional `LLM_MODEL` (default `sarvam-105b`).
- `sarvamai` is imported only in `kernal_core.llm`.
- Hosting can stay $0; LLM tokens use the Sarvam credit balance.

## Deploy and runtime

```text
GitHub Actions (cron) --POST /workflows/... + CRON_SECRET--> Cloud Run (FastAPI)
Cloudflare Pages (SPA) --HTTPS + CORS--> Cloud Run (FastAPI)
Cloud Run --DATABASE_URL--> Supabase Postgres
Cloud Run --core/llm--> Sarvam 105B
```

- FastAPI is the only public API. CORS allowlist = Pages origin.
- Cron hits FastAPI (or a Cloud Run Job) with a shared secret header. Do not put APScheduler inside the API process: Cloud Run sleeps.
- Long LinkedIn/LLM work must not depend on FastAPI `BackgroundTasks` after the HTTP response. Return `202` and run in-request on Cloud Run, or use a Cloud Run Job.
- Cloud Run request window is long enough for ranking + generation; still design jobs so a kill/retry is safe (idempotent writes to storage).

## What not to do

- Install Python packages on the host (`pip`, `--user`, Homebrew formulae). Use `.venv` only.
- Host FastAPI on Vercel or Netlify (timeouts, no real scheduler, ASGI adapter gaps).
- Use Render Free as the production API (15 min sleep, 750 h/month, no free cron, no persistent disk).
- Use Render’s free Postgres (expires in 30 days).
- Run in-process cron on a scale-to-zero service.
- Scrape LinkedIn from Cloud Run as if it were reliable. Datacenter IPs get blocked. Prefer a local CLI that writes into `core/storage` (Supabase Postgres) if cloud discovery fails.
- Couple workflow logic to “how we automate LinkedIn today.” Automate through **RECOMMEND**; the user executes sensitive actions in v1 ([`initial_context.md`](initial_context.md) action model).

## Repo layout to implement against

Directories match [`initial_context.md`](initial_context.md). Python import names are `kernal_*` (not `core`).

```text
kernal/
  docs/
    initial_context.md
    tech_stack.md
  core/src/kernal_core/
    workflows/
    scheduler/      # trigger/lifecycle helpers — not an in-process cron daemon
    storage/        # Postgres + optional blobs; the only place that knows Supabase
    context/
    llm/
    notifications/
    actions/
  apps/
    api/src/kernal_api/   # FastAPI → Cloud Run
    web/                  # Vite + React + TS → Cloudflare Pages
    linkedin/src/kernal_linkedin/
      discovery/
      ranking/
      generation/
      workflows/
        find_people.py
        engage_posts.py
        create_content.py
  config/
  cli/src/kernal_cli/     # local LinkedIn/session work that writes to core/storage
  .github/workflows/
```

| Directory | Import |
|---|---|
| `core/` | `kernal_core` |
| `apps/api/` | `kernal_api` |
| `apps/linkedin/` | `kernal_linkedin` |
| `cli/` | `kernal_cli` |

Do not grow a `data/` directory as durable memory.

## Env vars

| Variable | Where | Purpose |
|---|---|---|
| `DATABASE_URL` | Cloud Run | Supabase Postgres connection string |
| `SARVAM_API_KEY` | Cloud Run | Default LLM (Sarvam) |
| `LLM_MODEL` | Cloud Run | Optional; default `sarvam-105b` |
| `CRON_SECRET` | Cloud Run + GitHub Actions | Gate workflow trigger routes |
| `CORS_ORIGINS` | Cloud Run | Pages origin(s) |
| `VITE_API_URL` | Cloudflare Pages build | FastAPI base URL |

Do not add `SUPABASE_ANON_KEY` / client keys to the frontend. If Storage is used later, keep service credentials on Cloud Run only, behind `core/storage`.

## Not free (do not pretend otherwise)

- LLM usage beyond the provider free tier.
- LinkedIn has no official API for these workflows.
- SMTP is often blocked on free hosts. Dashboard first; email (Resend/Brevo) later.

## v1 objective

Build the minimum reusable core to run the three LinkedIn workflows well, with storage and LLM behind Core interfaces, so GitHub / Gmail / Calendar / Jira can land later without swapping the database product or the frontend host.
