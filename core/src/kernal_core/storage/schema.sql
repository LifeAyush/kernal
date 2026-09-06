-- Paste into the Supabase SQL editor if you create tables before the API has DATABASE_URL.
-- Matches kernal_core.storage.models (create_all).

CREATE TABLE IF NOT EXISTS user_context (
    id INTEGER PRIMARY KEY,
    interests TEXT[] NOT NULL DEFAULT '{}',
    topics TEXT[] NOT NULL DEFAULT '{}',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS people (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    linkedin_url TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    headline TEXT NOT NULL DEFAULT '',
    score DOUBLE PRECISION,
    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS workflow_runs (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    workflow_name TEXT NOT NULL,
    status TEXT NOT NULL,
    started_at TIMESTAMPTZ NOT NULL,
    finished_at TIMESTAMPTZ,
    error TEXT
);