"""
Caso de uso: Activar/Desactivar usuario.
"""
from src.auth.domain.user import User
from src.auth.domain.user_repository import UserRepository
from src.shared.errors.exceptions import UserNotFoundError
from src.shared.logging.logger import logger


class ToggleUserStatus:
    """
    Caso de uso para activar o desactivar un usuario.

    Flujo:
    1. Buscar usuario por ID
    2. Cambiar estado is_active
    3. Persistir cambios
    """

    def __init__(self, repository: UserRepository):
        """
        Inicializa el caso de uso.

        Args:
            repository: Repositorio de usuarios
        """
        self.repository = repository

    async def execute(self, user_id: int, is_active: bool) -> User:
        """
        Ejecuta el caso de uso.

        Args:
            user_id: ID del usuario
            is_active: True para activar, False para desactivar

        Returns:
            Usuario actualizado

        Raises:
            UserNotFoundError: Si el usuario no existe
        """
        # Buscar usuario
        user = await self.repository.find_by_id(user_id)

        if user is None:
            raise UserNotFoundError(f"Usuario con ID {user_id} no encontrado")

        # Cambiar estado
        if is_active:
            user.activate()
        else:
            user.deactivate()

        # Persistir cambios
        updated_user = await self.repository.update(user)

        action = "activated" if is_active else "deactivated"
        logger.info(
            f"User {action}",
            user_id=user_id,
            username=user.username,
            is_active=is_active,
        )

        return updated_user
