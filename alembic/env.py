from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine
from alembic import context
import asyncio
import sys
from pathlib import Path

# ------------------------------------------------------
# Add app folder to sys.path for imports
# ------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR / "app"))

# ------------------------------------------------------
# Import app settings and models
# ------------------------------------------------------
from app.core.config import settings
from app.database import Base, DATABASE_URL
from app import models  


# ------------------------------------------------------
# Alembic configuration setup
# ------------------------------------------------------
config = context.config
fileConfig(config.config_file_name)

# Use your app's DB URL dynamically
config.set_main_option("sqlalchemy.url", DATABASE_URL)
target_metadata = Base.metadata


# ------------------------------------------------------
# Run migrations in OFFLINE mode
# ------------------------------------------------------
def run_migrations_offline():
    """Run migrations without a live DB connection."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ------------------------------------------------------
# Run migrations in ONLINE (async) mode
# ------------------------------------------------------
async def run_migrations_online():
    """Run migrations with a live async DB connection."""
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def do_run_migrations(connection):
    """Helper to configure and run sync migration logic."""
    context.configure(connection=connection, target_metadata=target_metadata)

    # ⚠️ Must use 'with', not 'async with' here
    with context.begin_transaction():
        context.run_migrations()


# ------------------------------------------------------
# Entrypoint for Alembic CLI
# ------------------------------------------------------
def run_migrations():
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())


run_migrations()
