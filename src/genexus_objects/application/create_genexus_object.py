"""
Caso de uso: Crear objeto GeneXus manualmente.
"""
from typing import Optional

from src.genexus_objects.domain.genexus_object import GeneXusObject
from src.genexus_objects.domain.genexus_object_repository import GeneXusObjectRepository
from src.shared.errors.exceptions import ObjectAlreadyExistsError
from src.shared.logging.logger import logger


class CreateGeneXusObject:
    """
    Caso de uso para crear un nuevo objeto GeneXus manualmente.

    Flujo:
    1. Validar que el tipo de objeto existe
    2. Verificar que no exista un objeto con ese nombre y tipo
    3. Crear la entidad de dominio
    4. Persistir en el repositorio
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
        name: str,
        object_type_id: int,
        created_by: Optional[int] = None,
        description: str = None,
        id: int = None,
    ) -> GeneXusObject:
        """
        Ejecuta el caso de uso.

        Args:
            name: Nombre del objeto
            object_type_id: ID del tipo de objeto
            created_by: ID del usuario que crea el objeto (opcional)
            description: Descripción opcional
            id: ID opcional (si no se especifica, se autoincrementa)

        Returns:
            Objeto GeneXus creado

        Raises:
            ObjectTypeNotFoundError: Si el tipo no existe
            ObjectAlreadyExistsError: Si ya existe un objeto con ese nombre y tipo
            ValidationError: Si los datos son inválidos
        """
        # Normalizar datos
        normalized_name = name.strip()

        # Verificar que no exista
        existing = await self.repository.find_by_name_and_type(
            normalized_name, object_type_id
        )
        if existing is not None:
            logger.warning(
                "Attempt to create duplicate GeneXusObject",
                name=normalized_name,
                object_type_id=str(object_type_id),
            )
            raise ObjectAlreadyExistsError(normalized_name, str(object_type_id))

        # Crear entidad de dominio (se valida automáticamente)
        genexus_object = GeneXusObject.create_manual(
            name=normalized_name,
            object_type_id=object_type_id,
            created_by=created_by,
            description=description,
            id=id,
        )

        # Persistir
        created = await self.repository.create(genexus_object)

        logger.info(
            "GeneXusObject created successfully",
            object_id=str(created.id),
            name=created.name,
            object_type_id=str(created.object_type_id),
        )

        return created
