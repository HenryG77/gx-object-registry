"""
Interfaz del repositorio de User.

Define el contrato que debe implementar cualquier repositorio de User.
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple

from src.auth.domain.user import User


class UserRepository(ABC):
    """
    Repositorio de usuarios.

    Esta es una interfaz (abstract class) que define qué operaciones
    debe soportar cualquier implementación del repositorio.
    """

    @abstractmethod
    async def create(self, user: User) -> User:
        """
        Crea un nuevo usuario.

        Args:
            user: Usuario a crear

        Returns:
            Usuario creado con ID asignado

        Raises:
            UserAlreadyExistsError: Si ya existe un usuario con ese username o email
            DatabaseError: Si hay error de base de datos
        """
        pass

    @abstractmethod
    async def find_by_id(self, user_id: int) -> Optional[User]:
        """
        Busca un usuario por su ID.

        Args:
            user_id: ID del usuario a buscar

        Returns:
            User si existe, None si no existe
        """
        pass

    @abstractmethod
    async def find_by_username(self, username: str) -> Optional[User]:
        """
        Busca un usuario por su nombre de usuario (case-sensitive).

        Args:
            username: Username del usuario a buscar

        Returns:
            User si existe, None si no existe
        """
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        """
        Busca un usuario por su email (case-insensitive).

        Args:
            email: Email del usuario a buscar

        Returns:
            User si existe, None si no existe
        """
        pass

    @abstractmethod
    async def exists_by_username(self, username: str) -> bool:
        """
        Verifica si existe un usuario con el username dado.

        Args:
            username: Username a verificar

        Returns:
            True si existe, False si no existe
        """
        pass

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        """
        Verifica si existe un usuario con el email dado.

        Args:
            email: Email a verificar

        Returns:
            True si existe, False si no existe
        """
        pass

    @abstractmethod
    async def list_all(
        self, page: int = 1, page_size: int = 50, include_inactive: bool = False
    ) -> Tuple[List[User], int]:
        """
        Lista todos los usuarios con paginación.

        Args:
            page: Número de página (empezando en 1)
            page_size: Cantidad de elementos por página
            include_inactive: Si incluir usuarios inactivos (default: False)

        Returns:
            Tupla (lista de usuarios, total de registros)
        """
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """
        Actualiza un usuario existente.

        Args:
            user: Usuario con datos actualizados

        Returns:
            Usuario actualizado

        Raises:
            UserNotFoundError: Si el usuario no existe
            UserAlreadyExistsError: Si el nuevo username o email ya existe
            DatabaseError: Si hay error de base de datos
        """
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        """
        Elimina un usuario.

        Args:
            user_id: ID del usuario a eliminar

        Raises:
            UserNotFoundError: Si el usuario no existe
            DatabaseError: Si hay error de base de datos
        """
        pass

    @abstractmethod
    async def count_active_users(self) -> int:
        """
        Cuenta cuántos usuarios activos hay en el sistema.

        Returns:
            Cantidad de usuarios activos
        """
        pass

    @abstractmethod
    async def count_all_users(self) -> int:
        """
        Cuenta cuántos usuarios hay en el sistema (activos e inactivos).

        Returns:
            Cantidad total de usuarios
        """
        pass

    @abstractmethod
    async def list_users(
        self, offset: int = 0, limit: int = 50, include_inactive: bool = False
    ) -> List[User]:
        """
        Lista usuarios con paginación basada en offset/limit.

        Args:
            offset: Offset para paginación
            limit: Límite de resultados
            include_inactive: Si incluir usuarios inactivos

        Returns:
            Lista de usuarios
        """
        pass
