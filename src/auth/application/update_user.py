"""
Caso de uso: Actualizar información de usuario.
"""
from typing import Optional

from src.auth.domain.user import User
from src.auth.domain.user_repository import UserRepository
from src.shared.errors.exceptions import UserNotFoundError
from src.shared.logging.logger import logger


class UpdateUser:
    """
    Caso de uso para actualizar la información de un usuario.

    Flujo:
    1. Buscar usuario por ID
    2. Actualizar campos permitidos
    3. Persistir cambios
    """

    def __init__(self, repository: UserRepository):
        """
        Inicializa el caso de uso.

        Args:
            repository: Repositorio de usuarios
        """
        self.repository = repository

    async def execute(
        self,
        user_id: int,
        full_name: Optional[str] = None,
        email: Optional[str] = None,
    ) -> User:
        """
        Ejecuta el caso de uso.

        Args:
            user_id: ID del usuario a actualizar
            full_name: Nuevo nombre completo (opcional)
            email: Nuevo email (opcional)

        Returns:
            Usuario actualizado

        Raises:
            UserNotFoundError: Si el usuario no existe
            UserAlreadyExistsError: Si el nuevo email ya existe
            ValueError: Si los datos son inválidos
        """
        # Buscar usuario
        user = await self.repository.find_by_id(user_id)

        if user is None:
            raise UserNotFoundError(f"Usuario con ID {user_id} no encontrado")

        # Actualizar perfil
        user.update_profile(full_name=full_name, email=email)

        # Persistir cambios
        updated_user = await self.repository.update(user)

        logger.info(
            "User profile updated",
            user_id=user_id,
            full_name=full_name,
            email=email,
        )

        return updated_user
