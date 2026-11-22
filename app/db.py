"""Database helpers: everything that talks to PostgreSQL lives here."""

import psycopg

from app.config import settings


def get_connection() -> psycopg.Connection:
    """Open a new connection to PostgreSQL (gives up after 3 seconds)."""
    return psycopg.connect(settings.database_url, connect_timeout=3)


def check_database() -> dict:
    """Return the PostgreSQL and pgvector versions.

    Raises psycopg.Error if the database can't be reached.
    pgvector is None if the extension is not installed.
    """
    with get_connection() as conn:
        postgres_version, pgvector_version = conn.execute(
            """
            SELECT current_setting('server_version'),
                   (SELECT extversion FROM pg_extension WHERE extname = 'vector')
            """
        ).fetchone()
    # "17.12 (Debian 17.12-1.pgdg12+1)" -> "17.12"
    return {"postgres": postgres_version.split()[0], "pgvector": pgvector_version}
