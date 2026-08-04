"""
Manejadores de excepciones para FastAPI.

Convierte las excepciones de la aplicación en respuestas HTTP JSON.
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError as PydanticValidationError
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import Union

from src.shared.errors.exceptions import ApplicationError
from src.shared.errors.error_codes import ErrorCode
from src.shared.logging.logger import logger


async def application_error_handler(
    request: Request, exc: ApplicationError
) -> JSONResponse:
    """
    Maneja errores personalizados de la aplicación.

    Args:
        request: Request de FastAPI
        exc: Excepción de tipo ApplicationError

    Returns:
        JSONResponse con formato estandarizado
    """
    logger.error(
        "Application error",
        error_code=exc.code,
        message=exc.message,
        details=exc.details,
        path=request.url.path,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.code,
            "message": exc.message,
            "details": exc.details,
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path,
        },
    )


async def validation_error_handler(
    request: Request, exc: Union[RequestValidationError, PydanticValidationError]
) -> JSONResponse:
    """
    Maneja errores de validación de Pydantic.

    Args:
        request: Request de FastAPI
        exc: Excepción de validación

    Returns:
        JSONResponse con errores de validación formateados
    """
    errors = exc.errors()

    logger.warning(
        "Validation error",
        path=request.url.path,
        errors=errors,
    )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": ErrorCode.VALIDATION_ERROR,
            "message": "Error de validación de datos.",
            "details": {"errors": errors},
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path,
        },
    )


async def sqlalchemy_error_handler(
    request: Request, exc: SQLAlchemyError
) -> JSONResponse:
    """
    Maneja errores de SQLAlchemy.

    Args:
        request: Request de FastAPI
        exc: Excepción de SQLAlchemy

    Returns:
        JSONResponse con error de base de datos
    """
    logger.error(
        "Database error",
        error=str(exc),
        path=request.url.path,
    )

    # No exponer detalles internos de la BD en producción
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": ErrorCode.DATABASE_ERROR,
            "message": "Error interno de base de datos.",
            "details": {},
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path,
        },
    )


async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Maneja cualquier otra excepción no capturada.

    Args:
        request: Request de FastAPI
        exc: Cualquier excepción

    Returns:
        JSONResponse con error genérico
    """
    logger.exception(
        "Unhandled exception",
        error=str(exc),
        error_type=type(exc).__name__,
        path=request.url.path,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": ErrorCode.INTERNAL_ERROR,
            "message": "Error interno del servidor.",
            "details": {},
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path,
        },
    )


def register_exception_handlers(app):
    """
    Registra todos los manejadores de excepciones en la aplicación FastAPI.

    Args:
        app: Instancia de FastAPI

    Example:
        app = FastAPI()
        register_exception_handlers(app)
    """
    app.add_exception_handler(ApplicationError, application_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(PydanticValidationError, validation_error_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
    app.add_exception_handler(Exception, generic_error_handler)
