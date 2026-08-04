"""
Script de prueba para verificar configuración
"""
import sys
from pathlib import Path

# Agregar root al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Cargar .env explícitamente
from dotenv import load_dotenv
load_dotenv(root_dir / ".env", override=True)

# Ahora importar y verificar
from src.shared.config.settings import settings

print("="*60)
print("VERIFICACIÓN DE CONFIGURACIÓN")
print("="*60)
print(f"DATABASE_URL: {settings.database_url}")
print(f"APP_ENV: {settings.app_env}")
print(f"DEBUG: {settings.debug}")
print(f"DATABASE_POOL_SIZE: {settings.database_pool_size}")
print("="*60)

# Verificar la conexión
import asyncio
from src.shared.database.connection import engine

async def test_connection():
    """Probar la conexión a la base de datos"""
    print("\nProbando conexión a la base de datos...")
    try:
        async with engine.begin() as conn:
            result = await conn.execute(__import__("sqlalchemy").text("SELECT 1"))
            print("[OK] Conexión exitosa!")
            return True
    except Exception as e:
        print(f"[ERROR] Error de conexión: {e}")
        return False
    finally:
        await engine.dispose()

if __name__ == "__main__":
    success = asyncio.run(test_connection())
    sys.exit(0 if success else 1)
