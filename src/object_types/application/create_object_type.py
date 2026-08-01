"""
Caso de uso: Crear tipo de objeto.
"""
from typing import Optional

from src.object_types.domain.object_type import ObjectType
from src.object_types.domain.object_type_repository import ObjectTypeRepository
from src.shared.errors.exceptions import ObjectTypeAlreadyExistsError
from src.shared.logging.logger import logger


class CreateObjectType:
    """
    Caso de uso para crear un nuevo tipo de objeto.

    Flujo:
    1. Validar que el nombre no esté vacío
    2. Verificar que no exista un tipo con ese nombre
    3. Crear la entidad de dominio
    4. Persistir en el repositorio
    """

    def __init__(self, repository: ObjectTypeRepository):
        """
        Inicializa el caso de uso.

        Args:
            repository: Repositorio de tipos de objetos
        """
        self.repository = repository

    async def execute(self, name: str, created_by: Optional[int] = None, id: int = None) -> ObjectType:
        """
        Ejecuta el caso de uso.

        Args:
            name: Nombre del tipo de objeto a crear
            created_by: ID del usuario que crea el tipo (opcional)
            id: ID opcional (si no se especifica, se autoincrementa)

        Returns:
            Tipo de objeto creado

        Raises:
            ObjectTypeAlreadyExistsError: Si ya existe un tipo con ese nombre
            ValidationError: Si el nombre es inválido
        """
        # Normalizar nombre
        normalized_name = name.strip()

        # Verificar que no exista
        existing = await self.repository.find_by_name(normalized_name)
        if existing is not None:
            logger.warning(
                "Attempt to create duplicate ObjectType",
                name=normalized_name,
            )
            raise ObjectTypeAlreadyExistsError(normalized_name)

        # Crear entidad de dominio (se valida automáticamente)
        object_type = ObjectType.create(normalized_name, created_by=created_by, id=id)

        # Persistir
        created = await self.repository.create(object_type)

        logger.info(
            "ObjectType created successfully",
            object_type_id=str(created.id),
            name=created.name,
        )

        return created
