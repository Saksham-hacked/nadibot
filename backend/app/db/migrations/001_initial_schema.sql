-- NadiBot database migration
-- Run this SQL in the Supabase SQL editor or via psql to initialise the schema.
-- Tables use UUID primary keys and timestamptz for all timestamps.

-- Enable PostGIS extension for spatial queries (available on Supabase by default)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";

-- ── reporters ─────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS reporters (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    reporter_id   TEXT NOT NULL UNIQUE,      -- device-generated or server-assigned ID
    complaint_count INTEGER NOT NULL DEFAULT 0,
    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_reporters_reporter_id ON reporters(reporter_id);

-- ── incidents ─────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS incidents (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title           TEXT NOT NULL,
    category        TEXT NOT NULL,
    severity        TEXT NOT NULL,
    authority       TEXT NOT NULL,
    latitude        DOUBLE PRECISION NOT NULL,
    longitude       DOUBLE PRECISION NOT NULL,
    district        TEXT,
    state           TEXT,
    status          TEXT NOT NULL DEFAULT 'OPEN',
    complaint_count INTEGER NOT NULL DEFAULT 0,
    resolution_notes TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_incidents_status    ON incidents(status);
CREATE INDEX IF NOT EXISTS idx_incidents_category  ON incidents(category);
CREATE INDEX IF NOT EXISTS idx_incidents_authority ON incidents(authority);
CREATE INDEX IF NOT EXISTS idx_incidents_district  ON incidents(district);

-- ── complaints ────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS complaints (
    id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    reporter_id       TEXT NOT NULL,
    text              TEXT,
    transcript        TEXT,
    image_url         TEXT,
    audio_url         TEXT,
    image_summary     TEXT,
    -- Location raw
    latitude          DOUBLE PRECISION NOT NULL,
    longitude         DOUBLE PRECISION NOT NULL,
    location_accuracy DOUBLE PRECISION NOT NULL,
    location_source   TEXT,
    -- Location resolved
    locality          TEXT,
    district          TEXT,
    state             TEXT,
    full_address      TEXT,
    -- Classification
    category          TEXT NOT NULL DEFAULT 'Other',
    subcategory       TEXT NOT NULL DEFAULT 'Other',
    severity          TEXT NOT NULL DEFAULT 'Medium',
    authority         TEXT NOT NULL,
    summary           TEXT,
    confidence        DOUBLE PRECISION,
    -- Workflow
    status            TEXT NOT NULL DEFAULT 'OPEN',
    incident_id       UUID REFERENCES incidents(id) ON DELETE SET NULL,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_complaints_reporter_id ON complaints(reporter_id);
CREATE INDEX IF NOT EXISTS idx_complaints_status      ON complaints(status);
CREATE INDEX IF NOT EXISTS idx_complaints_category    ON complaints(category);
CREATE INDEX IF NOT EXISTS idx_complaints_authority   ON complaints(authority);
CREATE INDEX IF NOT EXISTS idx_complaints_district    ON complaints(district);
CREATE INDEX IF NOT EXISTS idx_complaints_incident_id ON complaints(incident_id);
CREATE INDEX IF NOT EXISTS idx_complaints_severity    ON complaints(severity);
CREATE INDEX IF NOT EXISTS idx_complaints_created_at  ON complaints(created_at);

-- ── Auto-update updated_at ─────────────────────────────────────────────────────

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE OR REPLACE TRIGGER complaints_updated_at
    BEFORE UPDATE ON complaints
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE OR REPLACE TRIGGER incidents_updated_at
    BEFORE UPDATE ON incidents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
