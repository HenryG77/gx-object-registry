"""
Script para resetear la base de datos.
Elimina todas las tablas y tipos para poder ejecutar las migraciones desde cero.
"""
import asyncio
import asyncpg
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

async def reset_database():
    """Resetea la base de datos eliminando tipos y tablas."""
    # Obtener DATABASE_URL del .env
    database_url = os.getenv("DATABASE_URL", "")

    # Convertir asyncpg URL a formato asyncpg
    database_url = database_url.replace("postgresql+asyncpg://", "postgresql://")

    print("Conectando a la base de datos...")
    conn = await asyncpg.connect(database_url)

    try:
        print("\n[1/4] Eliminando tabla genexus_objects (si existe)...")
        await conn.execute("DROP TABLE IF EXISTS genexus_objects CASCADE;")
        print("[OK] Tabla genexus_objects eliminada")

        print("\n[2/4] Eliminando tabla object_types (si existe)...")
        await conn.execute("DROP TABLE IF EXISTS object_types CASCADE;")
        print("[OK] Tabla object_types eliminada")

        print("\n[3/4] Eliminando tabla alembic_version (si existe)...")
        await conn.execute("DROP TABLE IF EXISTS alembic_version CASCADE;")
        print("[OK] Tabla alembic_version eliminada")

        print("\n[4/4] Eliminando tipo source_type_enum (si existe)...")
        await conn.execute("DROP TYPE IF EXISTS source_type_enum CASCADE;")
        print("[OK] Tipo source_type_enum eliminado")

        print("\n" + "="*50)
        print("[OK] Base de datos reseteada correctamente")
        print("="*50)
        print("\nAhora puedes ejecutar:")
        print("  alembic upgrade head")

    finally:
        await conn.close()
        print("\nConexión cerrada.")

if __name__ == "__main__":
    asyncio.run(reset_database())
