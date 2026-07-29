"""
Configuración de la conexión a la base de datos con SQLAlchemy.
"""
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool
from typing import AsyncGenerator

from src.shared.config.settings import settings


# Motor de base de datos (Engine)
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # Muestra SQL en consola si debug=True
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    pool_pre_ping=True,  # Verifica conexiones antes de usarlas
)


# Fábrica de sesiones
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # No expira objetos después de commit
    autocommit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Generador de sesiones de base de datos.

    Se usa como dependencia en FastAPI:
        @router.get("/objects")
        async def list_objects(session: AsyncSession = Depends(get_session)):
            ...

    Yields:
        AsyncSession: Sesión activa de base de datos

    Example:
        async with get_session() as session:
            result = await session.execute(query)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """
    Inicializa la base de datos.

    NOTA: En producción, usa Alembic para migraciones.
    Esta función es solo para desarrollo/testing.
    """
    from src.shared.database.base import Base

    async with engine.begin() as conn:
        # Crea todas las tablas definidas en Base
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """
    Cierra todas las conexiones a la base de datos.

    Debe llamarse al apagar la aplicación.
    """
    await engine.dispose()
