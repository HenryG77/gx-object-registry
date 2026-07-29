"""
Caso de uso: Obtener objeto GeneXus por ID.
"""
from uuid import UUID

from src.genexus_objects.domain.genexus_object import GeneXusObject
from src.genexus_objects.domain.genexus_object_repository import GeneXusObjectRepository
from src.shared.errors.exceptions import ObjectNotFoundError


class GetGeneXusObjectById:
    """
    Caso de uso para obtener un objeto GeneXus por su ID.

    Flujo:
    1. Buscar objeto por ID
    2. Si no existe, lanzar excepción
    3. Retornar objeto encontrado
    """

    def __init__(self, repository: GeneXusObjectRepository):
        """
        Inicializa el caso de uso.

        Args:
            repository: Repositorio de objetos GeneXus
        """
        self.repository = repository

    async def execute(self, object_id: UUID) -> GeneXusObject:
        """
        Ejecuta el caso de uso.

        Args:
            object_id: ID del objeto a buscar

        Returns:
            Objeto GeneXus encontrado

        Raises:
            ObjectNotFoundError: Si el objeto no existe
        """
        genexus_object = await self.repository.find_by_id(object_id)

        if genexus_object is None:
            raise ObjectNotFoundError(str(object_id))

        return genexus_object
