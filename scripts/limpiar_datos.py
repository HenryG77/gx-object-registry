"""
Script para limpiar todos los datos de las tablas sin borrar la estructura.
Esto te permite empezar desde cero, con el primer ID en 0.
"""
import asyncio
import asyncpg
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

async def limpiar_datos():
    """Limpia todos los datos de las tablas manteniendo la estructura."""
    database_url = os.getenv("DATABASE_URL", "")
    database_url = database_url.replace("postgresql+asyncpg://", "postgresql://")

    print("="*60)
    print("  LIMPIAR DATOS DE LAS TABLAS")
    print("="*60)
    print()

    print("Conectando a la base de datos...")
    conn = await asyncpg.connect(database_url)

    try:
        print("\n[1/3] Eliminando todos los objetos GeneXus...")
        result = await conn.execute("DELETE FROM genexus_objects;")
        print(f"  [OK] Objetos eliminados")

        print("\n[2/3] Eliminando todos los tipos de objeto...")
        result = await conn.execute("DELETE FROM object_types;")
        print(f"  [OK] Tipos eliminados")

        print("\n[3/3] Reiniciando secuencia a 0...")
        await conn.execute("ALTER SEQUENCE object_types_id_seq RESTART WITH 0;")
        print(f"  [OK] Secuencia reiniciada")

        print("\n" + "="*60)
        print("  LIMPIEZA COMPLETADA")
        print("="*60)
        print("\n  Tablas vacias.")
        print("  El primer registro que insertes tendra ID = 0")

    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        raise

    finally:
        await conn.close()
        print("\nConexion cerrada.")

if __name__ == "__main__":
    asyncio.run(limpiar_datos())
