from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings  # ✅ use absolute import (important for startup)

# -------------------------------------------------------------------
# DATABASE CONNECTION URL
# -------------------------------------------------------------------
DATABASE_URL = (
    f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}"
    f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
)

# -------------------------------------------------------------------
# CREATE ASYNC ENGINE
# -------------------------------------------------------------------
engine = create_async_engine(
    DATABASE_URL,
    echo=False,           # ✅ Set to True only for SQL debugging
    future=True
)

# -------------------------------------------------------------------
# CREATE ASYNC SESSION MAKER
# -------------------------------------------------------------------
async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # ✅ prevents data loss on commit
    autoflush=False,
    autocommit=False
)

# -------------------------------------------------------------------
# BASE CLASS FOR ORM MODELS
# -------------------------------------------------------------------
Base = declarative_base()

# -------------------------------------------------------------------
# DEPENDENCY FOR FASTAPI ROUTES
# -------------------------------------------------------------------
async def get_db():
    """Provide a transactional scope for each request."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
