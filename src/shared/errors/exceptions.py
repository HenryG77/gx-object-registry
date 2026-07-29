"""
Excepciones personalizadas de la aplicación.
"""
from typing import Any, Dict, Optional
from src.shared.errors.error_codes import ErrorCode


class ApplicationError(Exception):
    """
    Excepción base para todos los errores de la aplicación.

    Attributes:
        code: Código de error estandarizado
        message: Mensaje legible para humanos
        details: Información adicional sobre el error
        status_code: Código HTTP a devolver
    """

    def __init__(
        self,
        code: ErrorCode,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = 500,
    ):
        self.code = code
        self.message = message
        self.details = details or {}
        self.status_code = status_code
        super().__init__(message)


# ============================================================================
# Object Types Exceptions
# ============================================================================


class ObjectTypeNotFoundError(ApplicationError):
    """El tipo de objeto no existe."""

    def __init__(self, object_type_id: str):
        super().__init__(
            code=ErrorCode.OBJECT_TYPE_NOT_FOUND,
            message=f"Tipo de objeto con ID '{object_type_id}' no encontrado.",
            details={"object_type_id": object_type_id},
            status_code=404,
        )


class ObjectTypeAlreadyExistsError(ApplicationError):
    """El tipo de objeto ya existe."""

    def __init__(self, name: str):
        super().__init__(
            code=ErrorCode.OBJECT_TYPE_ALREADY_EXISTS,
            message=f"Ya existe un tipo de objeto con el nombre '{name}'.",
            details={"name": name},
            status_code=409,
        )


class ObjectTypeInUseError(ApplicationError):
    """El tipo de objeto no puede eliminarse porque tiene objetos relacionados."""

    def __init__(self, object_type_id: str, objects_count: int):
        super().__init__(
            code=ErrorCode.OBJECT_TYPE_IN_USE,
            message=f"No se puede eliminar el tipo de objeto porque tiene {objects_count} objeto(s) relacionado(s).",
            details={
                "object_type_id": object_type_id,
                "objects_count": objects_count,
            },
            status_code=409,
        )


# ============================================================================
# GeneXus Objects Exceptions
# ============================================================================


class ObjectNotFoundError(ApplicationError):
    """El objeto GeneXus no existe."""

    def __init__(self, object_id: str):
        super().__init__(
            code=ErrorCode.OBJECT_NOT_FOUND,
            message=f"Objeto con ID '{object_id}' no encontrado.",
            details={"object_id": object_id},
            status_code=404,
        )


class ObjectAlreadyExistsError(ApplicationError):
    """El objeto GeneXus ya existe."""

    def __init__(self, name: str, object_type_id: str):
        super().__init__(
            code=ErrorCode.OBJECT_ALREADY_EXISTS,
            message=f"Ya existe un objeto con el nombre '{name}' y ese tipo.",
            details={"name": name, "object_type_id": object_type_id},
            status_code=409,
        )


# ============================================================================
# Import Exceptions
# ============================================================================


class InvalidFileError(ApplicationError):
    """El archivo es inválido."""

    def __init__(self, reason: str):
        super().__init__(
            code=ErrorCode.INVALID_FILE,
            message=f"Archivo inválido: {reason}",
            details={"reason": reason},
            status_code=400,
        )


class InvalidFileExtensionError(ApplicationError):
    """La extensión del archivo no es válida."""

    def __init__(self, extension: str):
        super().__init__(
            code=ErrorCode.INVALID_FILE_EXTENSION,
            message=f"Extensión de archivo inválida. Se esperaba '.csv', se recibió '{extension}'.",
            details={"extension": extension},
            status_code=400,
        )


class FileTooLargeError(ApplicationError):
    """El archivo excede el tamaño máximo permitido."""

    def __init__(self, file_size_mb: float, max_size_mb: int):
        super().__init__(
            code=ErrorCode.FILE_TOO_LARGE,
            message=f"El archivo ({file_size_mb:.2f}MB) excede el tamaño máximo permitido ({max_size_mb}MB).",
            details={"file_size_mb": file_size_mb, "max_size_mb": max_size_mb},
            status_code=413,
        )


class InvalidHeaderError(ApplicationError):
    """El encabezado del CSV es inválido."""

    def __init__(self, expected: list, received: list):
        super().__init__(
            code=ErrorCode.INVALID_HEADER,
            message=f"Encabezado del CSV inválido. Se esperaba {expected}, se recibió {received}.",
            details={"expected": expected, "received": received},
            status_code=400,
        )


# ============================================================================
# Validation Exceptions
# ============================================================================


class ValidationError(ApplicationError):
    """Error de validación de datos."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=ErrorCode.VALIDATION_ERROR,
            message=message,
            details=details,
            status_code=400,
        )


# ============================================================================
# Database Exceptions
# ============================================================================


class DatabaseError(ApplicationError):
    """Error de base de datos."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=ErrorCode.DATABASE_ERROR,
            message=f"Error de base de datos: {message}",
            details=details,
            status_code=500,
        )
