"""
Caso de uso: Actualizar tipo de objeto.
"""
from src.object_types.domain.object_type import ObjectType
from src.object_types.domain.object_type_repository import ObjectTypeRepository
from src.shared.errors.exceptions import (
    ObjectTypeNotFoundError,
    ObjectTypeAlreadyExistsError,
)
from src.shared.logging.logger import logger


class UpdateObjectType:
    """
    Caso de uso para actualizar un tipo de objeto.

    Flujo:
    1. Buscar tipo por ID
    2. Verificar que el nuevo nombre no exista (si cambió)
    3. Actualizar nombre
    4. Persistir cambios
    """

    def __init__(self, repository: ObjectTypeRepository):
        """
        Inicializa el caso de uso.

        Args:
            repository: Repositorio de tipos de objetos
        """
        self.repository = repository

    async def execute(self, object_type_id: int, new_name: str) -> ObjectType:
        """
        Ejecuta el caso de uso.

        Args:
            object_type_id: ID del tipo a actualizar
            new_name: Nuevo nombre para el tipo

        Returns:
            Tipo de objeto actualizado

        Raises:
            ObjectTypeNotFoundError: Si el tipo no existe
            ObjectTypeAlreadyExistsError: Si el nuevo nombre ya existe
        """
        # Buscar tipo
        object_type = await self.repository.find_by_id(object_type_id)
        if object_type is None:
            raise ObjectTypeNotFoundError(str(object_type_id))

        # Normalizar nuevo nombre
        normalized_name = new_name.strip()

        # Si el nombre no cambió, retornar sin modificar
        if object_type.name.lower() == normalized_name.lower():
            return object_type

        # Verificar que el nuevo nombre no exista
        existing = await self.repository.find_by_name(normalized_name)
        if existing is not None and existing.id != object_type_id:
            logger.warning(
                "Attempt to update ObjectType with duplicate name",
                object_type_id=str(object_type_id),
                new_name=normalized_name,
            )
            raise ObjectTypeAlreadyExistsError(normalized_name)

        # Actualizar nombre (la entidad se valida automáticamente)
        object_type.update_name(normalized_name)

        # Persistir
        updated = await self.repository.update(object_type)

        logger.info(
            "ObjectType updated successfully",
            object_type_id=str(updated.id),
            new_name=updated.name,
        )

        return updated
