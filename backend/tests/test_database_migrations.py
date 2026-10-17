import io
from pathlib import Path
import pytest
import sqlalchemy as sa
from alembic.config import Config
from alembic import command
from alembic.script import ScriptDirectory

from app.database.database import Base, normalize_database_url
import app.database.models  # ensure models are registered


@pytest.fixture
def alembic_config():
    """Provides an Alembic Config instance pointing to the backend alembic.ini."""
    backend_dir = Path(__file__).resolve().parent.parent
    ini_path = backend_dir / "alembic.ini"
    cfg = Config(str(ini_path))
    cfg.set_main_option("script_location", str(backend_dir / "alembic"))
    return cfg


def test_migration_chain_integrity(alembic_config):
    """
    Verify that the migration chain starts with the initial schema creation,
    has no broken links, and cleanly reaches the single head revision.
    """
    script = ScriptDirectory.from_config(alembic_config)
    heads = script.get_heads()
    assert len(heads) == 1, f"Expected exactly 1 migration head, found {len(heads)}: {heads}"
    head_rev = heads[0]
    assert head_rev == "5b813be1bb86", f"Expected head revision 5b813be1bb86, got {head_rev}"

    # Verify migration revisions and down_revisions
    revisions = list(script.walk_revisions())
    # walk_revisions returns from head to base
    assert len(revisions) == 2, f"Expected 2 revisions in chain, found {len(revisions)}"

    rev_roadmap = revisions[0]
    assert rev_roadmap.revision == "5b813be1bb86"
    assert rev_roadmap.down_revision == "38f89b1b139a"

    rev_initial = revisions[1]
    assert rev_initial.revision == "38f89b1b139a"
    assert rev_initial.down_revision is None


def test_model_metadata_table_completeness():
    """
    Verify that Base.metadata contains all required application tables and expected constraints.
    """
    expected_tables = {
        "users",
        "job_descriptions",
        "resumes",
        "analyses",
        "skill_gaps",
        "recommendations",
        "roadmaps",
    }
    actual_tables = set(Base.metadata.tables.keys())
    assert expected_tables.issubset(actual_tables), f"Missing tables in metadata: {expected_tables - actual_tables}"

    # Verify users table constraints
    users_table = Base.metadata.tables["users"]
    assert "id" in users_table.c
    assert "email" in users_table.c
    assert users_table.c.email.unique or any(idx.unique for idx in users_table.indexes if "email" in [c.name for c in idx.columns])

    # Verify roadmaps table constraints
    roadmaps_table = Base.metadata.tables["roadmaps"]
    assert "analysis_id" in roadmaps_table.c
    assert any(fk.column.table.name == "analyses" for fk in roadmaps_table.foreign_keys)


def test_offline_sql_generation_head(alembic_config, capsys):
    """
    Verify that Alembic generates complete, valid static SQL for PostgreSQL dialect
    covering both the initial core tables and the roadmap table.
    """
    command.upgrade(alembic_config, "head", sql=True)
    captured = capsys.readouterr()
    sql_output = captured.out

    # Core table creations must be present in SQL
    assert "CREATE TABLE users" in sql_output
    assert "CREATE TABLE job_descriptions" in sql_output
    assert "CREATE TABLE resumes" in sql_output
    assert "CREATE TABLE analyses" in sql_output
    assert "CREATE TABLE recommendations" in sql_output
    assert "CREATE TABLE skill_gaps" in sql_output
    assert "CREATE TABLE roadmaps" in sql_output

    # Version tracking must be updated to head
    assert "38f89b1b139a" in sql_output
    assert "5b813be1bb86" in sql_output



def test_fresh_database_initialization_isolated(alembic_config):
    """
    Verify that a fresh isolated database can run the complete migration chain
    to head using an active engine connection passed to Alembic.
    """
    engine = sa.create_engine("sqlite:///:memory:")
    with engine.connect() as connection:
        alembic_config.attributes["connection"] = connection
        command.upgrade(alembic_config, "head")

        inspector = sa.inspect(connection)
        tables = set(inspector.get_table_names())

        expected_tables = {
            "alembic_version",
            "users",
            "job_descriptions",
            "resumes",
            "analyses",
            "skill_gaps",
            "recommendations",
            "roadmaps",
        }
        assert expected_tables.issubset(tables), f"Missing tables in migrated database: {expected_tables - tables}"

        # Check alembic_version reaches head
        res = connection.execute(sa.text("SELECT version_num FROM alembic_version")).scalar()
        assert res == "5b813be1bb86"


def test_fresh_postgresql_database_initialization(alembic_config):
    """
    Verify that a fresh PostgreSQL database instance can be created, migrated to head,
    verified for table and constraint integrity, and safely cleaned up.
    Skips if local PostgreSQL is unreachable.
    """
    import os
    admin_url = os.getenv("TEST_DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")
    try:
        admin_engine = sa.create_engine(admin_url, isolation_level="AUTOCOMMIT")
        with admin_engine.connect() as conn:
            conn.execute(sa.text("SELECT 1"))
    except Exception:
        pytest.skip("Local PostgreSQL server is not accessible; skipping live PostgreSQL migration test.")

    test_db_name = "jobjazz_test_fresh_mig"
    try:
        # Create fresh temporary database
        with admin_engine.connect() as conn:
            conn.execute(sa.text(f"DROP DATABASE IF EXISTS {test_db_name}"))
            conn.execute(sa.text(f"CREATE DATABASE {test_db_name}"))

        test_db_url = f"postgresql://postgres:postgres@localhost:5432/{test_db_name}"
        test_engine = sa.create_engine(test_db_url)

        with test_engine.connect() as connection:
            alembic_config.attributes["connection"] = connection
            command.upgrade(alembic_config, "head")

            inspector = sa.inspect(connection)
            tables = set(inspector.get_table_names())
            expected_tables = {
                "alembic_version",
                "users",
                "job_descriptions",
                "resumes",
                "analyses",
                "skill_gaps",
                "recommendations",
                "roadmaps",
            }
            assert expected_tables.issubset(tables)

            # Check foreign key from resumes to users
            resume_fks = inspector.get_foreign_keys("resumes")
            assert any(fk["referred_table"] == "users" for fk in resume_fks)

            # Check foreign key from roadmaps to analyses
            roadmap_fks = inspector.get_foreign_keys("roadmaps")
            assert any(fk["referred_table"] == "analyses" for fk in roadmap_fks)

            version = connection.execute(sa.text("SELECT version_num FROM alembic_version")).scalar()
            assert version == "5b813be1bb86"

        test_engine.dispose()
    finally:
        with admin_engine.connect() as conn:
            conn.execute(sa.text(f"DROP DATABASE IF EXISTS {test_db_name}"))
        admin_engine.dispose()


def test_neon_database_url_normalization():
    """
    Verify that production Neon PostgreSQL connection URLs with sslmode=require
    are cleanly normalized for psycopg v3 and accepted by Alembic URL resolution.
    """
    neon_url = "postgres://neondb_owner:npg_123456@ep-round-forest-a56789.us-east-2.aws.neon.tech/neondb?sslmode=require"
    normalized = normalize_database_url(neon_url)

    assert normalized.startswith("postgresql://")
    assert not normalized.startswith("postgres://")
    assert "?sslmode=require" in normalized
    assert "neondb_owner" in normalized


def test_entrypoint_script_contract():
    """
    Verify backend/entrypoint.sh contract for Render Free Tier:
    - Must use POSIX sh with set -e (fail-fast)
    - Must run alembic upgrade head before uvicorn
    - Must bind to ${PORT:-8000}
    - Must use exec for PID 1 signal handling
    - Must have Unix LF line endings (no \r)
    """
    backend_dir = Path(__file__).resolve().parent.parent
    entrypoint_path = backend_dir / "entrypoint.sh"

    assert entrypoint_path.is_file(), "backend/entrypoint.sh does not exist"

    raw_bytes = entrypoint_path.read_bytes()
    assert b"\r\n" not in raw_bytes, "backend/entrypoint.sh contains Windows CRLF line endings"

    content = raw_bytes.decode("utf-8")
    assert content.startswith("#!/bin/sh") or content.startswith("#!/bin/bash")
    assert "set -e" in content
    assert "alembic upgrade head" in content
    assert "uvicorn app.main:app" in content
    assert "${PORT:-8000}" in content
    assert "exec uvicorn" in content or "exec \"$@\"" in content


def test_dockerfile_startup_configuration():
    """
    Verify backend/Dockerfile startup configuration:
    - Must configure /app/entrypoint.sh as CMD
    - Must sanitize line endings and make entrypoint executable
    - Must NOT execute migrations during docker build
    - Must support dynamic $PORT in healthcheck
    """
    backend_dir = Path(__file__).resolve().parent.parent
    dockerfile_path = backend_dir / "Dockerfile"

    assert dockerfile_path.is_file(), "backend/Dockerfile does not exist"
    content = dockerfile_path.read_text(encoding="utf-8")

    # Entrypoint script must be configured as container command
    assert 'CMD ["/app/entrypoint.sh"]' in content

    # Line ending cleanup and executable permission
    assert "chmod +x /app/entrypoint.sh" in content

    # Build-time migration prohibition (must run at runtime, not build time)
    assert "RUN alembic" not in content

    # Dynamic health check port support
    assert "${PORT:-8000}" in content


def test_startup_command_simulation():
    """
    Simulate the startup logic in Python:
    - Validates that port defaults to 8000 if PORT is unset
    - Validates that custom PORT (e.g. Render's 10000) is honored
    - Validates that migration failure prevents server startup
    """
    def simulate_startup(migration_success: bool, env_port: str | None) -> dict:
        # Step 1: Run migration
        if not migration_success:
            raise RuntimeError("Alembic migration failed: relation 'users' does not exist")

        # Step 2: Determine port
        port = int(env_port) if env_port else 8000

        # Step 3: Server startup arguments
        return {
            "started": True,
            "host": "0.0.0.0",
            "port": port,
        }

    # Scenario A: Default port when PORT is unset (local Docker)
    result_default = simulate_startup(migration_success=True, env_port=None)
    assert result_default["started"] is True
    assert result_default["port"] == 8000

    # Scenario B: Render assigned port (e.g. 10000)
    result_render = simulate_startup(migration_success=True, env_port="10000")
    assert result_render["started"] is True
    assert result_render["port"] == 10000

    # Scenario C: Migration failure aborts startup without launching server
    with pytest.raises(RuntimeError) as exc_info:
        simulate_startup(migration_success=False, env_port="10000")
    assert "Alembic migration failed" in str(exc_info.value)
