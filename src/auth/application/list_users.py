"""
Caso de uso: Listar usuarios con paginación.
"""
from typing import Tuple, List

from src.auth.domain.user import User
from src.auth.domain.user_repository import UserRepository
from src.shared.logging.logger import logger


class ListUsers:
    """
    Caso de uso para listar usuarios con paginación.

    Flujo:
    1. Obtener total de usuarios activos
    2. Obtener página de usuarios
    3. Retornar resultados con información de paginación
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
        page: int = 1,
        page_size: int = 50,
        include_inactive: bool = False,
    ) -> Tuple[List[User], int]:
        """
        Ejecuta el caso de uso.

        Args:
            page: Número de página (inicia en 1)
            page_size: Tamaño de página
            include_inactive: Si incluir usuarios inactivos

        Returns:
            Tupla (lista de usuarios, total de usuarios)
        """
        # Validar parámetros
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 10
        if page_size > 100:
            page_size = 100

        # Calcular offset
        offset = (page - 1) * page_size

        # Obtener total de usuarios
        if include_inactive:
            total = await self.repository.count_all_users()
        else:
            total = await self.repository.count_active_users()

        # Obtener página de usuarios
        users = await self.repository.list_users(
            offset=offset,
            limit=page_size,
            include_inactive=include_inactive,
        )

        logger.info(
            "Users listed",
            page=page,
            page_size=page_size,
            total=total,
            include_inactive=include_inactive,
        )

        return users, total
