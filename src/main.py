"""
Punto de entrada principal de la aplicación FastAPI.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.shared.config.settings import settings
from src.shared.errors.handlers import register_exception_handlers
from src.shared.database.connection import close_db
from src.shared.logging.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Maneja el ciclo de vida de la aplicación.

    Se ejecuta al iniciar y al cerrar la aplicación.
    """
    # Startup
    logger.info(
        "Starting application",
        app_env=settings.app_env,
        debug=settings.debug,
    )

    yield

    # Shutdown
    logger.info("Shutting down application")
    await close_db()


# Crear aplicación FastAPI
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    debug=settings.debug,
    lifespan=lifespan,
)


# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Registrar manejadores de excepciones
register_exception_handlers(app)


# ============================================================================
# Endpoints básicos
# ============================================================================


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Endpoint de health check.

    Verifica que la aplicación esté funcionando.

    Returns:
        dict: Estado de la aplicación
    """
    return {
        "status": "ok",
        "app": settings.api_title,
        "version": settings.api_version,
        "environment": settings.app_env,
    }


@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raíz.

    Redirige a la documentación de la API.
    """
    return {
        "message": "GeneXus Object Registry API",
        "docs": "/docs",
        "health": "/health",
    }


# ============================================================================
# Incluir routers de módulos
# ============================================================================

from src.object_types.presentation.router import router as object_types_router
from src.genexus_objects.presentation.router import router as genexus_objects_router
from src.imports.presentation.router import router as imports_router

app.include_router(object_types_router, prefix=settings.api_prefix)
app.include_router(genexus_objects_router, prefix=settings.api_prefix)
app.include_router(imports_router, prefix=settings.api_prefix)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
