"""
Caso de uso: Obtener usuario actual desde token JWT.
"""
from typing import Optional

from src.auth.domain.user import User
from src.auth.domain.user_repository import UserRepository
from src.auth.infrastructure.jwt_handler import get_user_id_from_token
from src.shared.errors.exceptions import UnauthorizedError
from src.shared.logging.logger import logger


class GetCurrentUser:
    """
    Caso de uso para obtener el usuario actual desde un token JWT.

    Flujo:
    1. Extraer user_id del token JWT
    2. Buscar usuario en el repositorio
    3. Verificar que el usuario existe y está activo
    4. Retornar usuario
    """

    def __init__(self, repository: UserRepository):
        """
        Inicializa el caso de uso.

        Args:
            repository: Repositorio de usuarios
        """
        self.repository = repository

    async def execute(self, token: str) -> User:
        """
        Ejecuta el caso de uso.

        Args:
            token: Token JWT

        Returns:
            Usuario autenticado

        Raises:
            UnauthorizedError: Si el token es inválido o el usuario no existe/está inactivo
        """
        # Extraer user_id del token
        user_id = get_user_id_from_token(token)

        if user_id is None:
            logger.warning("Invalid or expired token")
            raise UnauthorizedError("Token inválido o expirado")

        # Buscar usuario
        user = await self.repository.find_by_id(user_id)

        if user is None:
            logger.warning(
                "Token contains non-existent user_id",
                user_id=user_id,
            )
            raise UnauthorizedError("Usuario no encontrado")

        # Verificar que está activo
        if not user.is_active:
            logger.warning(
                "Token belongs to inactive user",
                user_id=user_id,
                username=user.username,
            )
            raise UnauthorizedError("Usuario inactivo")

        return user
