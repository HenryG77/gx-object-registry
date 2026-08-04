"""
Caso de uso: Autenticar usuario (Login).
"""
from src.auth.domain.user import User
from src.auth.domain.user_repository import UserRepository
from src.auth.infrastructure.password_hasher import verify_password
from src.auth.infrastructure.jwt_handler import create_access_token
from src.shared.errors.exceptions import InvalidCredentialsError
from src.shared.logging.logger import logger


class AuthenticateUser:
    """
    Caso de uso para autenticar un usuario.

    Flujo:
    1. Buscar usuario por username
    2. Verificar que el usuario existe
    3. Verificar que el usuario está activo
    4. Verificar la contraseña
    5. Generar token JWT
    """

    def __init__(self, repository: UserRepository):
        """
        Inicializa el caso de uso.

        Args:
            repository: Repositorio de usuarios
        """
        self.repository = repository

    async def execute(self, username: str, password: str) -> tuple[User, str]:
        """
        Ejecuta el caso de uso.

        Args:
            username: Nombre de usuario
            password: Contraseña en texto plano

        Returns:
            Tupla (usuario autenticado, token JWT)

        Raises:
            InvalidCredentialsError: Si las credenciales son incorrectas
        """
        # Buscar usuario por username
        user = await self.repository.find_by_username(username)

        # Verificar que existe
        if user is None:
            logger.warning(
                "Login attempt with non-existent username",
                username=username,
            )
            raise InvalidCredentialsError()

        # Verificar que está activo
        if not user.is_active:
            logger.warning(
                "Login attempt with inactive user",
                username=username,
                user_id=user.id,
            )
            raise InvalidCredentialsError()

        # Verificar contraseña
        if not verify_password(password, user.hashed_password):
            logger.warning(
                "Login attempt with incorrect password",
                username=username,
                user_id=user.id,
            )
            raise InvalidCredentialsError()

        # Actualizar last_login
        user.record_login()
        await self.repository.update(user)

        # Generar token JWT
        # El token contiene el ID del usuario en el claim "sub"
        access_token = create_access_token(data={"sub": str(user.id)})

        logger.info(
            "User authenticated successfully",
            user_id=user.id,
            username=user.username,
        )

        return user, access_token
