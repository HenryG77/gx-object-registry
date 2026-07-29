"""
Mapper para convertir códigos de tipo de objeto a IDs.
"""
from typing import Dict, Optional
from uuid import UUID

from src.object_types.domain.object_type import ObjectType
from src.shared.logging.logger import logger


class ObjectTypeMapper:
    """
    Mapea códigos de tipo de objeto (del CSV) a IDs de la base de datos.

    El CSV contiene códigos numéricos (1, 2, 3...) que representan tipos.
    Este mapper construye un diccionario code -> UUID basándose en
    el orden de los tipos en la base de datos.

    Estrategia:
    1. Ordenar tipos por nombre alfabéticamente
    2. Asignar código 1 al primero, 2 al segundo, etc.
    """

    def __init__(self, object_types: list[ObjectType]):
        """
        Inicializa el mapper con los tipos disponibles.

        Args:
            object_types: Lista de tipos de objeto de la BD
        """
        self.types_by_code: Dict[str, UUID] = {}
        self.types_by_id: Dict[UUID, str] = {}
        self._build_mappings(object_types)

    def _build_mappings(self, object_types: list[ObjectType]) -> None:
        """
        Construye el mapping code <-> ID.

        Args:
            object_types: Lista de tipos de objeto
        """
        # Ordenar por nombre alfabéticamente para consistencia
        sorted_types = sorted(object_types, key=lambda t: t.name.lower())

        for index, obj_type in enumerate(sorted_types, start=1):
            code = str(index)
            self.types_by_code[code] = obj_type.id
            self.types_by_id[obj_type.id] = obj_type.name

        logger.info(
            "Object type mappings built",
            total_types=len(object_types),
            mappings={code: self.types_by_id[id_] for code, id_ in self.types_by_code.items()},
        )

    def get_type_id(self, code: str) -> Optional[UUID]:
        """
        Obtiene el UUID del tipo a partir del código.

        Args:
            code: Código del tipo (ej: "1", "2", "3")

        Returns:
            UUID del tipo o None si no existe
        """
        return self.types_by_code.get(code)

    def get_type_name(self, type_id: UUID) -> Optional[str]:
        """
        Obtiene el nombre del tipo a partir del ID.

        Args:
            type_id: ID del tipo

        Returns:
            Nombre del tipo o None si no existe
        """
        return self.types_by_id.get(type_id)

    def is_valid_code(self, code: str) -> bool:
        """
        Verifica si un código es válido.

        Args:
            code: Código a verificar

        Returns:
            True si el código existe
        """
        return code in self.types_by_code

    def get_available_mappings(self) -> Dict[str, str]:
        """
        Obtiene un diccionario legible de los mappings disponibles.

        Returns:
            Dict con code -> nombre del tipo
        """
        return {code: self.types_by_id[id_] for code, id_ in self.types_by_code.items()}
