from logging.config import fileConfig
import os
import sys
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from dotenv import load_dotenv

# Ensure the backend directory containing 'app' is present on sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.database.database import Base, normalize_database_url
from app.database import models

load_dotenv()


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata


def get_database_url() -> str:
    # 1. Environment variable DATABASE_URL takes priority (used in production on Render/Neon)
    env_url = os.getenv("DATABASE_URL")
    if env_url:
        return normalize_database_url(env_url)

    # 2. Config option sqlalchemy.url if set in alembic.ini or programmatically
    cfg_url = config.get_main_option("sqlalchemy.url")
    if cfg_url:
        return normalize_database_url(cfg_url)

    # 3. Default fallback
    return normalize_database_url(None)


def run_migrations_offline() -> None:
    url = get_database_url()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = config.attributes.get("connection", None)

    if connectable is None:
        configuration = config.get_section(config.config_ini_section)

        if configuration is None:
            configuration = {}

        configuration["sqlalchemy.url"] = get_database_url()

        connectable = engine_from_config(
            configuration,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
            )

            with context.begin_transaction():
                context.run_migrations()
    else:
        context.configure(
            connection=connectable,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
