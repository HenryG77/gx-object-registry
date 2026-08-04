"""
Caso de uso: Obtener estadísticas de un usuario.
"""
from dataclasses import dataclass

from src.auth.domain.user_repository import UserRepository
from src.object_types.domain.object_type_repository import ObjectTypeRepository
from src.genexus_objects.domain.genexus_object_repository import GeneXusObjectRepository
from src.shared.errors.exceptions import UserNotFoundError
from src.shared.logging.logger import logger


@dataclass
class UserStats:
    """Estadísticas de un usuario."""

    user_id: int
    username: str
    full_name: str | None
    total_object_types_created: int
    total_genexus_objects_created: int


class GetUserStats:
    """
    Caso de uso para obtener estadísticas de un usuario.

    Flujo:
    1. Verificar que el usuario existe
    2. Contar object_types creados
    3. Contar genexus_objects creados
    4. Retornar estadísticas
    """

    def __init__(
        self,
        user_repository: UserRepository,
        object_type_repository: ObjectTypeRepository,
        genexus_object_repository: GeneXusObjectRepository,
    ):
        """
        Inicializa el caso de uso.

        Args:
            user_repository: Repositorio de usuarios
            object_type_repository: Repositorio de tipos de objetos
            genexus_object_repository: Repositorio de objetos GeneXus
        """
        self.user_repository = user_repository
        self.object_type_repository = object_type_repository
        self.genexus_object_repository = genexus_object_repository

    async def execute(self, user_id: int) -> UserStats:
        """
        Ejecuta el caso de uso.

        Args:
            user_id: ID del usuario

        Returns:
            Estadísticas del usuario

        Raises:
            UserNotFoundError: Si el usuario no existe
        """
        # Verificar que el usuario existe
        user = await self.user_repository.find_by_id(user_id)

        if user is None:
            raise UserNotFoundError(f"Usuario con ID {user_id} no encontrado")

        # Contar object_types creados (necesitaría implementar este método en el repositorio)
        # Por ahora retornar 0 como placeholder
        total_object_types = 0

        # Contar genexus_objects creados (necesitaría implementar este método en el repositorio)
        # Por ahora retornar 0 como placeholder
        total_genexus_objects = 0

        logger.info(
            "User stats retrieved",
            user_id=user_id,
            username=user.username,
        )

        return UserStats(
            user_id=user.id,
            username=user.username,
            full_name=user.full_name,
            total_object_types_created=total_object_types,
            total_genexus_objects_created=total_genexus_objects,
        )
