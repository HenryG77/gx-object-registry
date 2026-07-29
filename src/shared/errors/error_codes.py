"""
Códigos de error estandarizados para toda la aplicación.
"""
from enum import Enum


class ErrorCode(str, Enum):
    """
    Códigos de error del sistema.

    Estos códigos son estables y se devuelven en las respuestas de error.
    El cliente puede usarlos para manejar errores específicos.
    """

    # ============================================================================
    # Object Types
    # ============================================================================
    OBJECT_TYPE_NOT_FOUND = "OBJECT_TYPE_NOT_FOUND"
    OBJECT_TYPE_ALREADY_EXISTS = "OBJECT_TYPE_ALREADY_EXISTS"
    OBJECT_TYPE_IN_USE = "OBJECT_TYPE_IN_USE"
    INVALID_OBJECT_TYPE_NAME = "INVALID_OBJECT_TYPE_NAME"

    # ============================================================================
    # GeneXus Objects
    # ============================================================================
    OBJECT_NOT_FOUND = "OBJECT_NOT_FOUND"
    OBJECT_ALREADY_EXISTS = "OBJECT_ALREADY_EXISTS"
    INVALID_OBJECT_NAME = "INVALID_OBJECT_NAME"
    INVALID_NAME_LENGTH = "INVALID_NAME_LENGTH"

    # ============================================================================
    # Import
    # ============================================================================
    INVALID_FILE = "INVALID_FILE"
    INVALID_FILE_EXTENSION = "INVALID_FILE_EXTENSION"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    INVALID_HEADER = "INVALID_HEADER"
    INVALID_ENCODING = "INVALID_ENCODING"
    INVALID_CSV = "INVALID_CSV"
    MISSING_NAME = "MISSING_NAME"
    MISSING_OBJECT_TYPE = "MISSING_OBJECT_TYPE"
    DUPLICATE_IN_FILE = "DUPLICATE_IN_FILE"
    INVALID_ROW = "INVALID_ROW"

    # ============================================================================
    # System
    # ============================================================================
    DATABASE_ERROR = "DATABASE_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    NOT_FOUND = "NOT_FOUND"
    BAD_REQUEST = "BAD_REQUEST"
