"""
Entidad de dominio GeneXusObject.

Representa un objeto de GeneXus (AhrPr001, AhrTn001, etc.)
"""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class SourceType(str, Enum):
    """Origen del registro del objeto."""
    MANUAL = "MANUAL"
    CSV = "CSV"


@dataclass
class GeneXusObject:
    """
    Objeto de GeneXus.

    Invariantes de dominio:
    - name no puede estar vacío después de trim
    - name no puede superar 128 caracteres
    - object_type_id debe existir en object_types
    - La combinación (name, object_type_id) debe ser única

    Attributes:
        id: Identificador único (autoincremental)
        name: Nombre técnico del objeto (ej: AhrPr001)
        description: Descripción funcional del objeto (opcional)
        object_type_id: ID del tipo de objeto (FK a object_types)
        source_type: Origen del registro (MANUAL o CSV)
        created_at: Fecha de creación
        updated_at: Fecha de última actualización
    """

    id: Optional[int]
    name: str
    description: Optional[str]
    object_type_id: int
    source_type: SourceType
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        """Valida la entidad después de inicializarla."""
        self._validate()

    def _validate(self):
        """
        Valida las reglas de negocio de la entidad.

        Raises:
            ValueError: Si alguna regla de negocio es violada
        """
        # Validar que name no esté vacío
        if not self.name or not self.name.strip():
            raise ValueError("El nombre del objeto no puede estar vacío")

        # Validar longitud máxima
        if len(self.name) > 128:
            raise ValueError("El nombre del objeto no puede superar 128 caracteres")

    @staticmethod
    def create_manual(
        name: str,
        object_type_id: int,
        description: Optional[str] = None,
        id: Optional[int] = None,
    ) -> "GeneXusObject":
        """
        Factory method para crear un objeto manualmente.

        Args:
            name: Nombre del objeto
            object_type_id: ID del tipo de objeto
            description: Descripción opcional
            id: ID opcional (si no se especifica, se autoincrementa)

        Returns:
            Nueva instancia de GeneXusObject con source_type=MANUAL

        Example:
            >>> obj = GeneXusObject.create_manual(
            ...     "AhrPr001",
            ...     1,
            ...     "Recupera Tasa de Interés"
            ... )
            >>> obj_with_id = GeneXusObject.create_manual(
            ...     "AhrPr002",
            ...     1,
            ...     "Otro objeto",
            ...     id=0
            ... )
        """
        now = datetime.utcnow()
        normalized_name = name.strip()
        normalized_description = description.strip() if description and description.strip() else None

        return GeneXusObject(
            id=id,  # Puede ser None o un valor específico
            name=normalized_name,
            description=normalized_description,
            object_type_id=object_type_id,
            source_type=SourceType.MANUAL,
            created_at=now,
            updated_at=now,
        )

    @staticmethod
    def create_from_csv(
        name: str,
        object_type_id: int,
        description: Optional[str] = None,
    ) -> "GeneXusObject":
        """
        Factory method para crear un objeto desde CSV.

        Args:
            name: Nombre del objeto
            object_type_id: ID del tipo de objeto
            description: Descripción opcional

        Returns:
            Nueva instancia de GeneXusObject con source_type=CSV
        """
        now = datetime.utcnow()
        normalized_name = name.strip()
        normalized_description = description.strip() if description and description.strip() else None

        return GeneXusObject(
            id=None,  # El ID será asignado por la BD
            name=normalized_name,
            description=normalized_description,
            object_type_id=object_type_id,
            source_type=SourceType.CSV,
            created_at=now,
            updated_at=now,
        )

    def update_description(self, new_description: Optional[str]) -> None:
        """
        Actualiza solo la descripción del objeto.

        Args:
            new_description: Nueva descripción (puede ser None)
        """
        normalized = new_description.strip() if new_description and new_description.strip() else None
        self.description = normalized
        self.updated_at = datetime.utcnow()

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        object_type_id: Optional[int] = None,
    ) -> None:
        """
        Actualiza múltiples campos del objeto.

        Args:
            name: Nuevo nombre (opcional)
            description: Nueva descripción (opcional)
            object_type_id: Nuevo tipo (opcional)

        Raises:
            ValueError: Si las validaciones fallan
        """
        if name is not None:
            self.name = name.strip()

        if description is not None:
            normalized = description.strip() if description.strip() else None
            self.description = normalized

        if object_type_id is not None:
            self.object_type_id = object_type_id

        self.updated_at = datetime.utcnow()
        self._validate()

    def __str__(self) -> str:
        return f"GeneXusObject(id={self.id}, name={self.name}, type_id={self.object_type_id})"

    def __repr__(self) -> str:
        return self.__str__()
