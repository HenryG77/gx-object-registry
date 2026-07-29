"""
Interfaz del repositorio de ObjectType.

Define el contrato que debe implementar cualquier repositorio de ObjectType.
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from uuid import UUID

from src.object_types.domain.object_type import ObjectType


class ObjectTypeRepository(ABC):
    """
    Repositorio de tipos de objetos.

    Esta es una interfaz (abstract class) que define qué operaciones
    debe soportar cualquier implementación del repositorio.
    """

    @abstractmethod
    async def create(self, object_type: ObjectType) -> ObjectType:
        """
        Crea un nuevo tipo de objeto.

        Args:
            object_type: Tipo de objeto a crear

        Returns:
            Tipo de objeto creado con ID asignado

        Raises:
            ObjectTypeAlreadyExistsError: Si ya existe un tipo con ese nombre
            DatabaseError: Si hay error de base de datos
        """
        pass

    @abstractmethod
    async def find_by_id(self, object_type_id: UUID) -> Optional[ObjectType]:
        """
        Busca un tipo de objeto por su ID.

        Args:
            object_type_id: ID del tipo a buscar

        Returns:
            ObjectType si existe, None si no existe
        """
        pass

    @abstractmethod
    async def find_by_name(self, name: str) -> Optional[ObjectType]:
        """
        Busca un tipo de objeto por su nombre (case-insensitive).

        Args:
            name: Nombre del tipo a buscar

        Returns:
            ObjectType si existe, None si no existe
        """
        pass

    @abstractmethod
    async def exists_by_name(self, name: str) -> bool:
        """
        Verifica si existe un tipo con el nombre dado.

        Args:
            name: Nombre a verificar

        Returns:
            True si existe, False si no existe
        """
        pass

    @abstractmethod
    async def list_all(self, page: int = 1, page_size: int = 50) -> Tuple[List[ObjectType], int]:
        """
        Lista todos los tipos de objetos con paginación.

        Args:
            page: Número de página (empezando en 1)
            page_size: Cantidad de elementos por página

        Returns:
            Tupla (lista de tipos, total de registros)
        """
        pass

    @abstractmethod
    async def update(self, object_type: ObjectType) -> ObjectType:
        """
        Actualiza un tipo de objeto existente.

        Args:
            object_type: Tipo con datos actualizados

        Returns:
            Tipo de objeto actualizado

        Raises:
            ObjectTypeNotFoundError: Si el tipo no existe
            ObjectTypeAlreadyExistsError: Si el nuevo nombre ya existe
            DatabaseError: Si hay error de base de datos
        """
        pass

    @abstractmethod
    async def delete(self, object_type_id: UUID) -> None:
        """
        Elimina un tipo de objeto.

        Args:
            object_type_id: ID del tipo a eliminar

        Raises:
            ObjectTypeNotFoundError: Si el tipo no existe
            ObjectTypeInUseError: Si el tipo tiene objetos relacionados
            DatabaseError: Si hay error de base de datos
        """
        pass

    @abstractmethod
    async def has_related_objects(self, object_type_id: UUID) -> bool:
        """
        Verifica si el tipo tiene objetos relacionados.

        Args:
            object_type_id: ID del tipo a verificar

        Returns:
            True si tiene objetos relacionados, False si no
        """
        pass

    @abstractmethod
    async def count_related_objects(self, object_type_id: UUID) -> int:
        """
        Cuenta cuántos objetos están relacionados con este tipo.

        Args:
            object_type_id: ID del tipo

        Returns:
            Cantidad de objetos relacionados
        """
        pass
