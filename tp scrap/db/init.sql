-- db/init.sql
-- Executed automatically when the PostgreSQL volume is created.

CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    source_id VARCHAR(64) UNIQUE,
    source_url TEXT UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    event_type VARCHAR(120),
    region VARCHAR(120),
    venue VARCHAR(255),
    address TEXT,
    city VARCHAR(120),
    country VARCHAR(80),
    start_date TIMESTAMPTZ,
    end_date TIMESTAMPTZ,
    description TEXT,
    image_url TEXT,
    organizer VARCHAR(255),
    min_price NUMERIC(10, 2),
    currency VARCHAR(10),
    offers JSONB DEFAULT '[]'::jsonb,
    contact_phone VARCHAR(80),
    contact_email VARCHAR(255),
    website TEXT,
    scraped_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS events_source_id_uidx ON events (source_id);
CREATE INDEX IF NOT EXISTS events_start_date_idx ON events (start_date);
CREATE INDEX IF NOT EXISTS events_region_idx ON events (region);
CREATE INDEX IF NOT EXISTS events_type_idx ON events (event_type);
