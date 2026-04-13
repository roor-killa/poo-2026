"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-04-13
"""

from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    op.execute("""
        CREATE TABLE routes (
            id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name        VARCHAR(120) NOT NULL UNIQUE,
            description TEXT,
            is_active   BOOLEAN NOT NULL DEFAULT TRUE,
            created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)

    op.execute("""
        CREATE TABLE stops (
            id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name       VARCHAR(120) NOT NULL,
            location   GEOGRAPHY(POINT, 4326) NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    op.execute("CREATE INDEX idx_stops_location ON stops USING GIST(location)")

    op.execute("""
        CREATE TABLE route_stops (
            id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            route_id             UUID NOT NULL REFERENCES routes(id) ON DELETE CASCADE,
            stop_id              UUID NOT NULL REFERENCES stops(id) ON DELETE CASCADE,
            stop_order           SMALLINT NOT NULL,
            distance_from_prev_m DOUBLE PRECISION,
            UNIQUE (route_id, stop_order)
        )
    """)

    op.execute("""
        CREATE TABLE buses (
            id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            code       VARCHAR(20) NOT NULL UNIQUE,
            label      VARCHAR(80),
            route_id   UUID REFERENCES routes(id) ON DELETE SET NULL,
            api_token  VARCHAR(128) NOT NULL UNIQUE,
            is_active  BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)

    op.execute("""
        CREATE TABLE positions (
            id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            bus_id      UUID NOT NULL REFERENCES buses(id) ON DELETE CASCADE,
            location    GEOGRAPHY(POINT, 4326) NOT NULL,
            speed_kmh   DOUBLE PRECISION,
            heading     DOUBLE PRECISION,
            recorded_at TIMESTAMPTZ NOT NULL,
            received_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    op.execute("CREATE INDEX idx_positions_bus_time ON positions (bus_id, recorded_at DESC)")
    op.execute("CREATE INDEX idx_positions_location ON positions USING GIST(location)")

    op.execute("""
        CREATE TABLE segment_speeds (
            id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            route_id        UUID NOT NULL REFERENCES routes(id) ON DELETE CASCADE,
            from_stop_order SMALLINT NOT NULL,
            to_stop_order   SMALLINT NOT NULL,
            hour_bucket     SMALLINT NOT NULL CHECK (hour_bucket BETWEEN 0 AND 23),
            day_type        VARCHAR(10) NOT NULL DEFAULT 'weekday',
            avg_speed_kmh   DOUBLE PRECISION NOT NULL,
            sample_count    INTEGER NOT NULL DEFAULT 0,
            updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
            UNIQUE (route_id, from_stop_order, to_stop_order, hour_bucket, day_type)
        )
    """)

    op.execute("""
        CREATE TABLE bus_status (
            bus_id          UUID PRIMARY KEY REFERENCES buses(id) ON DELETE CASCADE,
            last_location   GEOGRAPHY(POINT, 4326),
            last_speed_kmh  DOUBLE PRECISION,
            last_seen_at    TIMESTAMPTZ,
            is_online       BOOLEAN NOT NULL DEFAULT FALSE,
            current_stop_id UUID REFERENCES stops(id),
            next_stop_id    UUID REFERENCES stops(id),
            eta_next_stop_s INTEGER,
            eta_terminus_s  INTEGER,
            progress_pct    DOUBLE PRECISION,
            updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS bus_status")
    op.execute("DROP TABLE IF EXISTS segment_speeds")
    op.execute("DROP TABLE IF EXISTS positions")
    op.execute("DROP TABLE IF EXISTS buses")
    op.execute("DROP TABLE IF EXISTS route_stops")
    op.execute("DROP TABLE IF EXISTS stops")
    op.execute("DROP TABLE IF EXISTS routes")
