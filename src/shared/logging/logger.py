"""
Configuración del sistema de logging estructurado con structlog.
"""
import logging
import sys
import structlog
from typing import Any

from src.shared.config.settings import settings


def configure_logging() -> structlog.BoundLogger:
    """
    Configura el sistema de logging estructurado.

    Returns:
        Logger configurado

    Example:
        from src.shared.logging.logger import logger

        logger.info("Usuario creó objeto", user_id=123, object_name="AhrPr001")
        logger.error("Error al importar CSV", file_name="objetos.csv", error="...")
    """
    # Configurar logging estándar de Python
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper()),
    )

    # Procesadores de structlog
    processors = [
        # Agregar nivel de log (info, error, etc.)
        structlog.stdlib.add_log_level,
        # Agregar timestamp
        structlog.processors.TimeStamper(fmt="iso"),
        # Agregar información del llamador (archivo, línea)
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.LINENO,
            }
        ),
        # Formatear excepciones
        structlog.processors.format_exc_info,
        # Decodificar unicode
        structlog.processors.UnicodeDecoder(),
    ]

    # Renderizador según el entorno
    if settings.debug:
        # En desarrollo: formato legible con colores
        processors.append(structlog.dev.ConsoleRenderer())
    else:
        # En producción: formato JSON
        processors.append(structlog.processors.JSONRenderer())

    # Configurar structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger()


# Logger global
logger = configure_logging()
