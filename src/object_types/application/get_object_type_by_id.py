"""
Caso de uso: Obtener tipo de objeto por ID.
"""
from uuid import UUID

from src.object_types.domain.object_type import ObjectType
from src.object_types.domain.object_type_repository import ObjectTypeRepository
from src.shared.errors.exceptions import ObjectTypeNotFoundError


class GetObjectTypeById:
    """
    Caso de uso para obtener un tipo de objeto por su ID.

    Flujo:
    1. Buscar tipo por ID
    2. Si no existe, lanzar excepción
    3. Retornar tipo encontrado
    """

    def __init__(self, repository: ObjectTypeRepository):
        """
        Inicializa el caso de uso.

        Args:
            repository: Repositorio de tipos de objetos
        """
        self.repository = repository

    async def execute(self, object_type_id: UUID) -> ObjectType:
        """
        Ejecuta el caso de uso.

        Args:
            object_type_id: ID del tipo a buscar

        Returns:
            Tipo de objeto encontrado

        Raises:
            ObjectTypeNotFoundError: Si el tipo no existe
        """
        object_type = await self.repository.find_by_id(object_type_id)

        if object_type is None:
            raise ObjectTypeNotFoundError(str(object_type_id))

        return object_type
