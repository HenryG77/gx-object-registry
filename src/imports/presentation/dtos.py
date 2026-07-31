"""
DTOs para el módulo de importación CSV.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class ImportErrorDTO(BaseModel):
    """Representa un error durante la importación."""

    row_number: int = Field(..., description="Número de fila donde ocurrió el error")
    field: Optional[str] = Field(None, description="Campo que causó el error")
    message: str = Field(..., description="Mensaje de error")
    raw_data: Dict = Field(default_factory=dict, description="Datos crudos de la fila")


class ImportResultResponse(BaseModel):
    """Response del resultado de la importación."""

    total_rows: int = Field(..., description="Total de filas procesadas")
    success_count: int = Field(..., description="Total de filas procesadas exitosamente")
    created_count: int = Field(..., description="Objetos creados")
    updated_count: int = Field(..., description="Objetos actualizados")
    skipped_count: int = Field(..., description="Filas omitidas")
    error_count: int = Field(..., description="Filas con errores")
    has_errors: bool = Field(..., description="Indica si hubo errores")
    errors: List[ImportErrorDTO] = Field(default_factory=list, description="Lista de errores")
    created_ids: List[int] = Field(default_factory=list, description="IDs de objetos creados")
    updated_ids: List[int] = Field(default_factory=list, description="IDs de objetos actualizados")


class ObjectTypeMappingDTO(BaseModel):
    """Representa el mapping de código a tipo de objeto."""

    code: str = Field(..., description="Código numérico (1, 2, 3...)")
    name: str = Field(..., description="Nombre del tipo de objeto")
    id: int = Field(..., description="ID del tipo en la base de datos")


class ObjectTypeMappingsResponse(BaseModel):
    """Response con los mappings disponibles de tipos de objeto."""

    mappings: List[ObjectTypeMappingDTO] = Field(
        ...,
        description="Lista de mappings código -> tipo",
    )
    total: int = Field(..., description="Total de tipos disponibles")
