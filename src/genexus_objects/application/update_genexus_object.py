"""
Caso de uso: Actualizar objeto GeneXus.
"""
from typing import Optional
from uuid import UUID

from src.genexus_objects.domain.genexus_object import GeneXusObject
from src.genexus_objects.domain.genexus_object_repository import GeneXusObjectRepository
from src.shared.errors.exceptions import (
    ObjectNotFoundError,
    ObjectAlreadyExistsError,
)
from src.shared.logging.logger import logger


class UpdateGeneXusObject:
    """
    Caso de uso para actualizar un objeto GeneXus.

    Flujo:
    1. Buscar objeto por ID
    2. Si cambia nombre o tipo, verificar que no exista duplicado
    3. Actualizar campos
    4. Persistir cambios
    """

    def __init__(self, repository: GeneXusObjectRepository):
        """
        Inicializa el caso de uso.

        Args:
            repository: Repositorio de objetos GeneXus
        """
        self.repository = repository

    async def execute(
        self,
        object_id: UUID,
        name: Optional[str] = None,
        description: Optional[str] = None,
        object_type_id: Optional[UUID] = None,
    ) -> GeneXusObject:
        """
        Ejecuta el caso de uso.

        Args:
            object_id: ID del objeto a actualizar
            name: Nuevo nombre (opcional)
            description: Nueva descripción (opcional)
            object_type_id: Nuevo tipo (opcional)

        Returns:
            Objeto GeneXus actualizado

        Raises:
            ObjectNotFoundError: Si el objeto no existe
            ObjectTypeNotFoundError: Si el nuevo tipo no existe
            ObjectAlreadyExistsError: Si el nuevo nombre/tipo ya existe
        """
        # Buscar objeto
        genexus_object = await self.repository.find_by_id(object_id)
        if genexus_object is None:
            raise ObjectNotFoundError(str(object_id))

        # Determinar nuevos valores
        new_name = name.strip() if name is not None else genexus_object.name
        new_type_id = object_type_id if object_type_id is not None else genexus_object.object_type_id

        # Si cambió nombre o tipo, verificar duplicados
        if new_name != genexus_object.name or new_type_id != genexus_object.object_type_id:
            existing = await self.repository.find_by_name_and_type(new_name, new_type_id)
            if existing is not None and existing.id != object_id:
                logger.warning(
                    "Attempt to update GeneXusObject with duplicate name/type",
                    object_id=str(object_id),
                    new_name=new_name,
                    new_type_id=str(new_type_id),
                )
                raise ObjectAlreadyExistsError(new_name, str(new_type_id))

        # Actualizar entidad (se valida automáticamente)
        genexus_object.update(
            name=name,
            description=description,
            object_type_id=object_type_id,
        )

        # Persistir
        updated = await self.repository.update(genexus_object)

        logger.info(
            "GeneXusObject updated successfully",
            object_id=str(updated.id),
            name=updated.name,
        )

        return updated
