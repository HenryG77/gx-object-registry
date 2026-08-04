"""
Caso de uso: Resetear contraseña de usuario (por admin).
"""
from src.auth.domain.user import User
from src.auth.domain.user_repository import UserRepository
from src.auth.infrastructure.password_hasher import hash_password
from src.shared.errors.exceptions import UserNotFoundError
from src.shared.logging.logger import logger


class ResetUserPassword:
    """
    Caso de uso para resetear la contraseña de un usuario.

    Este caso de uso es para que un administrador pueda resetear
    la contraseña de cualquier usuario.

    Flujo:
    1. Buscar usuario por ID
    2. Hashear nueva contraseña
    3. Actualizar usuario
    4. Persistir cambios
    """

    def __init__(self, repository: UserRepository):
        """
        Inicializa el caso de uso.

        Args:
            repository: Repositorio de usuarios
        """
        self.repository = repository

    async def execute(self, user_id: int) -> User:
        """
        Ejecuta el caso de uso.

        La contraseña temporal será igual al username del usuario.
        El usuario deberá cambiarla en su próximo login.

        Args:
            user_id: ID del usuario

        Returns:
            Usuario actualizado

        Raises:
            UserNotFoundError: Si el usuario no existe
        """
        # Buscar usuario
        user = await self.repository.find_by_id(user_id)

        if user is None:
            raise UserNotFoundError(f"Usuario con ID {user_id} no encontrado")

        # Usar username como contraseña temporal
        temp_password = user.username
        hashed_password = hash_password(temp_password)

        # Actualizar contraseña
        user.change_password(hashed_password)

        # Marcar que debe cambiar contraseña en próximo login
        user.must_change_password = True
        user.updated_at = user.updated_at  # Asegurar que se actualiza

        # Persistir cambios
        updated_user = await self.repository.update(user)

        logger.info(
            "User password reset by admin",
            user_id=user_id,
            username=user.username,
            temp_password_set=True,
        )

        return updated_user
