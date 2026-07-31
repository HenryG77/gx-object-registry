"""
Caso de uso: Eliminar tipo de objeto.
"""
from src.object_types.domain.object_type_repository import ObjectTypeRepository
from src.shared.errors.exceptions import (
    ObjectTypeNotFoundError,
    ObjectTypeInUseError,
)
from src.shared.logging.logger import logger


class DeleteObjectType:
    """
    Caso de uso para eliminar un tipo de objeto.

    Flujo:
    1. Verificar que el tipo existe
    2. Verificar que no tenga objetos relacionados
    3. Eliminar del repositorio
    """

    def __init__(self, repository: ObjectTypeRepository):
        """
        Inicializa el caso de uso.

        Args:
            repository: Repositorio de tipos de objetos
        """
        self.repository = repository

    async def execute(self, object_type_id: int) -> None:
        """
        Ejecuta el caso de uso.

        Args:
            object_type_id: ID del tipo a eliminar

        Raises:
            ObjectTypeNotFoundError: Si el tipo no existe
            ObjectTypeInUseError: Si el tipo tiene objetos relacionados
        """
        # Verificar que existe
        object_type = await self.repository.find_by_id(object_type_id)
        if object_type is None:
            raise ObjectTypeNotFoundError(str(object_type_id))

        # Verificar que no tenga objetos relacionados
        has_objects = await self.repository.has_related_objects(object_type_id)
        if has_objects:
            count = await self.repository.count_related_objects(object_type_id)
            logger.warning(
                "Attempt to delete ObjectType with related objects",
                object_type_id=str(object_type_id),
                related_objects_count=count,
            )
            raise ObjectTypeInUseError(str(object_type_id), count)

        # Eliminar
        await self.repository.delete(object_type_id)

        logger.info(
            "ObjectType deleted successfully",
            object_type_id=str(object_type_id),
        )
