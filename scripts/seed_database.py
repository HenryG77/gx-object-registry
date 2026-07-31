"""
Script para crear datos iniciales (seed) en la base de datos.

Crea los tipos de objeto básicos para empezar a usar la aplicación.
"""
import asyncio
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.shared.config.settings import settings
from src.object_types.infrastructure.sqlalchemy_object_type_repository import (
    SQLAlchemyObjectTypeRepository,
)
from src.object_types.application.create_object_type import CreateObjectType
from src.shared.errors.exceptions import ObjectAlreadyExistsError


async def seed_object_types():
    """Crea los tipos de objeto iniciales."""
    print("🌱 Iniciando seed de tipos de objeto...")
    print(f"📊 Base de datos: {settings.database_url.split('@')[-1]}\n")

    # Tipos de objeto básicos de GeneXus
    object_types = [
        "PROCEDURE",
        "TRANSACTION",
        "DATA_PROVIDER",
        "WEB_PANEL",
        "WORK_WITH",
        "DASHBOARD",
        "SD_PANEL",
        "MASTER_PAGE",
        "THEME",
        "DOMAIN",
        "IMAGE",
        "STYLE",
    ]

    engine = create_async_engine(settings.database_url, echo=False)
    async_session_factory = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    created_count = 0
    skipped_count = 0

    async with async_session_factory() as session:
        repo = SQLAlchemyObjectTypeRepository(session)
        use_case = CreateObjectType(repo)

        for type_name in object_types:
            try:
                object_type = await use_case.execute(type_name)
                print(f"✅ Creado: {type_name} (ID: {object_type.id})")
                created_count += 1

            except ObjectAlreadyExistsError:
                print(f"⏭️  Ya existe: {type_name}")
                skipped_count += 1

            except Exception as e:
                print(f"❌ Error creando {type_name}: {e}")

        # Commit de la transacción
        await session.commit()

    await engine.dispose()

    print(f"\n✨ Seed completado:")
    print(f"   • Creados: {created_count}")
    print(f"   • Ya existían: {skipped_count}")
    print(f"   • Total: {len(object_types)}")


if __name__ == "__main__":
    asyncio.run(seed_object_types())
