"""
Script de inicio que fuerza la carga del archivo .env
"""
import sys
from pathlib import Path
from dotenv import load_dotenv

# Cargar .env antes de importar cualquier cosa
root_dir = Path(__file__).parent
env_path = root_dir / ".env"

# Forzar la carga del .env
load_dotenv(env_path, override=True)

# Agregar el directorio raíz al path
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Ahora importar y ejecutar la aplicación
if __name__ == "__main__":
    import uvicorn
    from src.shared.config.settings import settings

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=9000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
