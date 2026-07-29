"""
Interfaz del repositorio de GeneXusObject.

Define el contrato que debe implementar cualquier repositorio de GeneXusObject.
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from uuid import UUID

from src.genexus_objects.domain.genexus_object import GeneXusObject, SourceType


class GeneXusObjectRepository(ABC):
    """
    Repositorio de objetos GeneXus.

    Esta es una interfaz (abstract class) que define qué operaciones
    debe soportar cualquier implementación del repositorio.
    """

    @abstractmethod
    async def create(self, genexus_object: GeneXusObject) -> GeneXusObject:
        """
        Crea un nuevo objeto GeneXus.

        Args:
            genexus_object: Objeto a crear

        Returns:
            Objeto creado con ID asignado

        Raises:
            ObjectAlreadyExistsError: Si ya existe un objeto con ese nombre y tipo
            ObjectTypeNotFoundError: Si el tipo no existe
            DatabaseError: Si hay error de base de datos
        """
        pass

    @abstractmethod
    async def bulk_create(self, objects: List[GeneXusObject]) -> List[GeneXusObject]:
        """
        Crea múltiples objetos en lote (para importación CSV).

        Args:
            objects: Lista de objetos a crear

        Returns:
            Lista de objetos creados

        Raises:
            DatabaseError: Si hay error de base de datos
        """
        pass

    @abstractmethod
    async def find_by_id(self, object_id: UUID) -> Optional[GeneXusObject]:
        """
        Busca un objeto por su ID.

        Args:
            object_id: ID del objeto a buscar

        Returns:
            GeneXusObject si existe, None si no existe
        """
        pass

    @abstractmethod
    async def find_by_name_and_type(
        self,
        name: str,
        object_type_id: UUID,
    ) -> Optional[GeneXusObject]:
        """
        Busca un objeto por nombre y tipo.

        Args:
            name: Nombre del objeto
            object_type_id: ID del tipo

        Returns:
            GeneXusObject si existe, None si no existe
        """
        pass

    @abstractmethod
    async def exists_by_name_and_type(
        self,
        name: str,
        object_type_id: UUID,
    ) -> bool:
        """
        Verifica si existe un objeto con ese nombre y tipo.

        Args:
            name: Nombre a verificar
            object_type_id: ID del tipo

        Returns:
            True si existe, False si no existe
        """
        pass

    @abstractmethod
    async def search(
        self,
        search: Optional[str] = None,
        name: Optional[str] = None,
        object_type_id: Optional[UUID] = None,
        source_type: Optional[SourceType] = None,
        page: int = 1,
        page_size: int = 50,
        sort_by: str = "name",
        sort_order: str = "asc",
    ) -> Tuple[List[GeneXusObject], int]:
        """
        Búsqueda avanzada de objetos con filtros y paginación.

        Args:
            search: Búsqueda general en name y description (opcional)
            name: Filtro exacto por nombre (opcional)
            object_type_id: Filtro por tipo (opcional)
            source_type: Filtro por origen (opcional)
            page: Número de página (empezando en 1)
            page_size: Cantidad de elementos por página
            sort_by: Campo por el que ordenar (name, created_at, updated_at)
            sort_order: Orden (asc, desc)

        Returns:
            Tupla (lista de objetos, total de registros)
        """
        pass

    @abstractmethod
    async def update(self, genexus_object: GeneXusObject) -> GeneXusObject:
        """
        Actualiza un objeto existente.

        Args:
            genexus_object: Objeto con datos actualizados

        Returns:
            Objeto actualizado

        Raises:
            ObjectNotFoundError: Si el objeto no existe
            ObjectAlreadyExistsError: Si el nuevo nombre/tipo ya existe
            ObjectTypeNotFoundError: Si el nuevo tipo no existe
            DatabaseError: Si hay error de base de datos
        """
        pass

    @abstractmethod
    async def bulk_update(self, objects: List[GeneXusObject]) -> List[GeneXusObject]:
        """
        Actualiza múltiples objetos en lote (para importación CSV).

        Args:
            objects: Lista de objetos a actualizar

        Returns:
            Lista de objetos actualizados

        Raises:
            DatabaseError: Si hay error de base de datos
        """
        pass

    @abstractmethod
    async def delete(self, object_id: UUID) -> None:
        """
        Elimina un objeto.

        Args:
            object_id: ID del objeto a eliminar

        Raises:
            ObjectNotFoundError: Si el objeto no existe
            DatabaseError: Si hay error de base de datos
        """
        pass
