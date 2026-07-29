"""
DTOs (Data Transfer Objects) para object_types.

Define los modelos de Request y Response para la API REST.
"""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from uuid import UUID
from typing import List


class CreateObjectTypeRequest(BaseModel):
    """Request para crear un tipo de objeto."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre del tipo de objeto (ej: PROCEDURE, TRANSACTION)",
        examples=["PROCEDURE", "TRANSACTION", "WORK_PANEL"],
    )

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        """Valida que el nombre no esté vacío después de trim."""
        stripped = v.strip()
        if not stripped:
            raise ValueError("El nombre no puede estar vacío")
        return stripped


class UpdateObjectTypeRequest(BaseModel):
    """Request para actualizar un tipo de objeto."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nuevo nombre del tipo de objeto",
        examples=["STORED_PROCEDURE"],
    )

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        """Valida que el nombre no esté vacío después de trim."""
        stripped = v.strip()
        if not stripped:
            raise ValueError("El nombre no puede estar vacío")
        return stripped


class ObjectTypeResponse(BaseModel):
    """Response de un tipo de objeto."""

    id: UUID = Field(..., description="ID único del tipo de objeto")
    name: str = Field(..., description="Nombre del tipo")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")

    model_config = {"from_attributes": True}


class ObjectTypeListResponse(BaseModel):
    """Response de lista de tipos con paginación."""

    items: List[ObjectTypeResponse] = Field(..., description="Lista de tipos de objetos")
    total: int = Field(..., description="Total de registros")
    page: int = Field(..., description="Página actual")
    page_size: int = Field(..., description="Tamaño de página")
    total_pages: int = Field(..., description="Total de páginas")

    @staticmethod
    def create(
        items: List[ObjectTypeResponse],
        total: int,
        page: int,
        page_size: int,
    ) -> "ObjectTypeListResponse":
        """
        Factory method para crear la respuesta paginada.

        Args:
            items: Lista de tipos
            total: Total de registros
            page: Página actual
            page_size: Tamaño de página

        Returns:
            Respuesta paginada
        """
        total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0

        return ObjectTypeListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )
