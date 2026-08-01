"""
DTOs (Data Transfer Objects) para genexus_objects.

Define los modelos de Request y Response para la API REST.
"""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import List, Optional
from enum import Enum


class SourceTypeDTO(str, Enum):
    """Enumeración para el origen del registro."""
    MANUAL = "MANUAL"
    CSV = "CSV"


class CreateGeneXusObjectRequest(BaseModel):
    """Request para crear un objeto GeneXus."""

    id: Optional[int] = Field(
        None,
        ge=0,
        description="ID opcional del objeto (si no se especifica, se autoincrementa)",
        examples=[0, 1, 2],
    )

    name: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="Nombre técnico del objeto GeneXus",
        examples=["AhrPr001", "AhrTn001", "CálculoIVA"],
    )

    description: Optional[str] = Field(
        None,
        description="Descripción funcional del objeto",
        examples=["Recupera Tasa de Interés", "Tipos de Cuentas"],
    )

    object_type_id: int = Field(
        ...,
        description="ID del tipo de objeto",
    )

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        """Valida que el nombre no esté vacío después de trim."""
        stripped = v.strip()
        if not stripped:
            raise ValueError("El nombre no puede estar vacío")
        return stripped

    @field_validator("description")
    @classmethod
    def normalize_description(cls, v: Optional[str]) -> Optional[str]:
        """Normaliza la descripción."""
        if v is None or not v.strip():
            return None
        return v.strip()


class UpdateGeneXusObjectRequest(BaseModel):
    """Request para actualizar un objeto GeneXus."""

    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=128,
        description="Nuevo nombre del objeto",
    )

    description: Optional[str] = Field(
        None,
        description="Nueva descripción del objeto",
    )

    object_type_id: Optional[int] = Field(
        None,
        description="Nuevo ID del tipo de objeto",
    )

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        """Valida que el nombre no esté vacío después de trim."""
        if v is not None:
            stripped = v.strip()
            if not stripped:
                raise ValueError("El nombre no puede estar vacío")
            return stripped
        return None

    @field_validator("description")
    @classmethod
    def normalize_description(cls, v: Optional[str]) -> Optional[str]:
        """Normaliza la descripción."""
        if v is None or not v.strip():
            return None
        return v.strip()


class GeneXusObjectResponse(BaseModel):
    """Response de un objeto GeneXus."""

    id: int = Field(..., description="ID único del objeto (autoincremental)")
    name: str = Field(..., description="Nombre técnico del objeto")
    description: Optional[str] = Field(None, description="Descripción funcional")
    object_type_id: int = Field(..., description="ID del tipo de objeto")
    source_type: SourceTypeDTO = Field(..., description="Origen del registro")
    created_by: Optional[int] = Field(None, description="ID del usuario que creó el objeto")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")

    # Campos adicionales denormalizados (se llenarán en el router)
    object_type_name: Optional[str] = Field(None, description="Nombre del tipo de objeto")

    model_config = {"from_attributes": True}


class SearchGeneXusObjectsRequest(BaseModel):
    """Request para búsqueda de objetos."""

    search: Optional[str] = Field(
        None,
        description="Búsqueda general en nombre y descripción",
    )

    name: Optional[str] = Field(
        None,
        description="Filtro exacto por nombre",
    )

    object_type_id: Optional[int] = Field(
        None,
        description="Filtro por tipo de objeto",
    )

    source_type: Optional[SourceTypeDTO] = Field(
        None,
        description="Filtro por origen (MANUAL/CSV)",
    )

    page: int = Field(
        default=1,
        ge=1,
        description="Número de página",
    )

    page_size: int = Field(
        default=50,
        ge=1,
        le=1000,
        description="Tamaño de página (máximo 1000)",
    )

    sort_by: str = Field(
        default="id",
        description="Campo por el que ordenar",
        pattern="^(id|name|created_at|updated_at|object_type_name|source_type)$",
    )

    sort_order: str = Field(
        default="asc",
        description="Orden (asc/desc)",
        pattern="^(asc|desc)$",
    )


class GeneXusObjectListResponse(BaseModel):
    """Response de lista de objetos con paginación."""

    items: List[GeneXusObjectResponse] = Field(..., description="Lista de objetos")
    total: int = Field(..., description="Total de registros")
    page: int = Field(..., description="Página actual")
    page_size: int = Field(..., description="Tamaño de página")
    total_pages: int = Field(..., description="Total de páginas")

    @staticmethod
    def create(
        items: List[GeneXusObjectResponse],
        total: int,
        page: int,
        page_size: int,
    ) -> "GeneXusObjectListResponse":
        """
        Factory method para crear la respuesta paginada.

        Args:
            items: Lista de objetos
            total: Total de registros
            page: Página actual
            page_size: Tamaño de página

        Returns:
            Respuesta paginada
        """
        total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0

        return GeneXusObjectListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )
