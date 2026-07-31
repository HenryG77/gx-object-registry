"""
Entidad de dominio ObjectType.

Representa un tipo de objeto GeneXus (PROCEDURE, TRANSACTION, etc.)
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ObjectType:
    """
    Tipo de objeto GeneXus.

    Invariantes de dominio:
    - name no puede estar vacío después de trim
    - name no puede superar 100 caracteres
    - name debe ser único (case-insensitive)

    Attributes:
        id: Identificador único (autoincremental)
        name: Nombre del tipo (ej: PROCEDURE, TRANSACTION)
        created_at: Fecha de creación
        updated_at: Fecha de última actualización
    """

    id: Optional[int]
    name: str
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
            raise ValueError("El nombre del tipo no puede estar vacío")

        # Validar longitud máxima
        if len(self.name) > 100:
            raise ValueError("El nombre del tipo no puede superar 100 caracteres")

    @staticmethod
    def create(name: str, id: Optional[int] = None) -> "ObjectType":
        """
        Factory method para crear un nuevo tipo de objeto.

        Args:
            name: Nombre del tipo
            id: ID opcional (si no se especifica, se autoincrementa)

        Returns:
            Nueva instancia de ObjectType

        Example:
            >>> object_type = ObjectType.create("PROCEDURE")
            >>> object_type_with_id = ObjectType.create("TRANSACTION", id=0)
        """
        now = datetime.utcnow()
        normalized_name = name.strip()

        return ObjectType(
            id=id,  # Puede ser None o un valor específico
            name=normalized_name,
            created_at=now,
            updated_at=now,
        )

    def update_name(self, new_name: str) -> None:
        """
        Actualiza el nombre del tipo.

        Args:
            new_name: Nuevo nombre para el tipo

        Raises:
            ValueError: Si el nombre es inválido
        """
        self.name = new_name.strip()
        self.updated_at = datetime.utcnow()
        self._validate()

    def __str__(self) -> str:
        return f"ObjectType(id={self.id}, name={self.name})"

    def __repr__(self) -> str:
        return self.__str__()
