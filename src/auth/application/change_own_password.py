"""
Caso de uso: Cambiar la propia contraseña.
"""
from src.auth.domain.user import User
from src.auth.domain.user_repository import UserRepository
from src.auth.infrastructure.password_hasher import hash_password, verify_password
from src.shared.errors.exceptions import UserNotFoundError, InvalidCredentialsError
from src.shared.logging.logger import logger


class ChangeOwnPassword:
    """
    Caso de uso para que un usuario cambie su propia contraseña.

    Flujo:
    1. Buscar usuario por ID
    2. Verificar contraseña actual (si se proporciona)
    3. Hashear nueva contraseña
    4. Actualizar usuario
    5. Desmarcar must_change_password
    6. Persistir cambios
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
        new_password: str,
        current_password: str | None = None,
    ) -> User:
        """
        Ejecuta el caso de uso.

        Args:
            user_id: ID del usuario
            new_password: Nueva contraseña en texto plano
            current_password: Contraseña actual (opcional, requerida si no es cambio obligatorio)

        Returns:
            Usuario actualizado

        Raises:
            UserNotFoundError: Si el usuario no existe
            InvalidCredentialsError: Si la contraseña actual no coincide
            ValueError: Si la nueva contraseña no es válida
        """
        # Validar nueva contraseña
        if not new_password or len(new_password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")

        # Buscar usuario
        user = await self.repository.find_by_id(user_id)

        if user is None:
            raise UserNotFoundError(f"Usuario con ID {user_id} no encontrado")

        # Si no es cambio obligatorio, verificar contraseña actual
        if not user.must_change_password:
            if not current_password:
                raise ValueError("Debes proporcionar tu contraseña actual")

            if not verify_password(current_password, user.hashed_password):
                logger.warning(
                    "Password change attempt with incorrect current password",
                    user_id=user_id,
                    username=user.username,
                )
                raise InvalidCredentialsError("La contraseña actual es incorrecta")

        # Validar que no sea igual a la contraseña temporal (username)
        if user.must_change_password and new_password == user.username:
            raise ValueError("La nueva contraseña no puede ser igual a tu nombre de usuario")

        # Hashear nueva contraseña
        hashed_password = hash_password(new_password)

        # Actualizar contraseña
        user.change_password(hashed_password)

        # Desmarcar cambio obligatorio
        user.must_change_password = False

        # Persistir cambios
        updated_user = await self.repository.update(user)

        logger.info(
            "User changed own password",
            user_id=user_id,
            username=user.username,
            was_forced=user.must_change_password,
        )

        return updated_user
