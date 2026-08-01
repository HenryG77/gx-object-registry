"""
Implementación del repositorio de User usando SQLAlchemy.
"""
from typing import Optional, List, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.auth.domain.user import User
from src.auth.domain.user_repository import UserRepository
from src.auth.infrastructure.models import UserModel
from src.shared.errors.exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    DatabaseError,
)
from src.shared.logging.logger import logger


class SQLAlchemyUserRepository(UserRepository):
    """
    Implementación de UserRepository usando SQLAlchemy.

    Traduce entre la entidad de dominio User y el modelo
    de base de datos UserModel.
    """

    def __init__(self, session: AsyncSession):
        """
        Inicializa el repositorio.

        Args:
            session: Sesión activa de SQLAlchemy
        """
        self.session = session

    def _to_domain(self, model: UserModel) -> User:
        """
        Convierte un modelo de BD a entidad de dominio.

        Args:
            model: Modelo de SQLAlchemy

        Returns:
            Entidad de dominio User
        """
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            hashed_password=model.hashed_password,
            full_name=model.full_name,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
            last_login=model.last_login,
            must_change_password=model.must_change_password,
        )

    def _to_model(self, entity: User) -> UserModel:
        """
        Convierte una entidad de dominio a modelo de BD.

        Args:
            entity: Entidad de dominio

        Returns:
            Modelo de SQLAlchemy
        """
        return UserModel(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            hashed_password=entity.hashed_password,
            full_name=entity.full_name,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            last_login=entity.last_login,
            must_change_password=entity.must_change_password,
        )

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
        model = self._to_model(user)

        try:
            self.session.add(model)
            await self.session.flush()
            await self.session.refresh(model)

            logger.info("User created", user_id=model.id, username=model.username)

            return self._to_domain(model)

        except IntegrityError as e:
            await self.session.rollback()
            error_msg = str(e.orig).lower()

            if "username" in error_msg:
                raise UserAlreadyExistsError(f"Ya existe un usuario con el username '{user.username}'")
            elif "email" in error_msg:
                raise UserAlreadyExistsError(f"Ya existe un usuario con el email '{user.email}'")
            else:
                raise UserAlreadyExistsError("El usuario ya existe")

        except Exception as e:
            await self.session.rollback()
            logger.error("Error creating user", error=str(e))
            raise DatabaseError(f"Error al crear usuario: {str(e)}")

    async def find_by_id(self, user_id: int) -> Optional[User]:
        """
        Busca un usuario por su ID.

        Args:
            user_id: ID del usuario a buscar

        Returns:
            User si existe, None si no existe
        """
        try:
            stmt = select(UserModel).where(UserModel.id == user_id)
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()

            if model is None:
                return None

            return self._to_domain(model)

        except Exception as e:
            logger.error("Error finding user by id", user_id=user_id, error=str(e))
            raise DatabaseError(f"Error al buscar usuario: {str(e)}")

    async def find_by_username(self, username: str) -> Optional[User]:
        """
        Busca un usuario por su nombre de usuario (case-sensitive).

        Args:
            username: Username del usuario a buscar

        Returns:
            User si existe, None si no existe
        """
        try:
            stmt = select(UserModel).where(UserModel.username == username)
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()

            if model is None:
                return None

            return self._to_domain(model)

        except Exception as e:
            logger.error("Error finding user by username", username=username, error=str(e))
            raise DatabaseError(f"Error al buscar usuario: {str(e)}")

    async def find_by_email(self, email: str) -> Optional[User]:
        """
        Busca un usuario por su email (case-insensitive).

        Args:
            email: Email del usuario a buscar

        Returns:
            User si existe, None si no existe
        """
        try:
            # Buscar con case-insensitive
            stmt = select(UserModel).where(func.lower(UserModel.email) == email.lower())
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()

            if model is None:
                return None

            return self._to_domain(model)

        except Exception as e:
            logger.error("Error finding user by email", email=email, error=str(e))
            raise DatabaseError(f"Error al buscar usuario: {str(e)}")

    async def exists_by_username(self, username: str) -> bool:
        """
        Verifica si existe un usuario con el username dado.

        Args:
            username: Username a verificar

        Returns:
            True si existe, False si no existe
        """
        try:
            stmt = select(func.count()).select_from(UserModel).where(UserModel.username == username)
            result = await self.session.execute(stmt)
            count = result.scalar()

            return count > 0

        except Exception as e:
            logger.error("Error checking user existence by username", username=username, error=str(e))
            raise DatabaseError(f"Error al verificar usuario: {str(e)}")

    async def exists_by_email(self, email: str) -> bool:
        """
        Verifica si existe un usuario con el email dado.

        Args:
            email: Email a verificar

        Returns:
            True si existe, False si no existe
        """
        try:
            stmt = select(func.count()).select_from(UserModel).where(
                func.lower(UserModel.email) == email.lower()
            )
            result = await self.session.execute(stmt)
            count = result.scalar()

            return count > 0

        except Exception as e:
            logger.error("Error checking user existence by email", email=email, error=str(e))
            raise DatabaseError(f"Error al verificar usuario: {str(e)}")

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
        try:
            offset = (page - 1) * page_size

            # Query base
            stmt = select(UserModel)

            # Filtrar por activos si no se incluyen inactivos
            if not include_inactive:
                stmt = stmt.where(UserModel.is_active == True)

            # Ordenar por ID
            stmt = stmt.order_by(UserModel.id.asc())

            # Contar total
            count_stmt = select(func.count()).select_from(UserModel)
            if not include_inactive:
                count_stmt = count_stmt.where(UserModel.is_active == True)

            total_result = await self.session.execute(count_stmt)
            total = total_result.scalar()

            # Obtener página
            stmt = stmt.limit(page_size).offset(offset)
            result = await self.session.execute(stmt)
            models = result.scalars().all()

            users = [self._to_domain(model) for model in models]

            return users, total

        except Exception as e:
            logger.error("Error listing users", error=str(e))
            raise DatabaseError(f"Error al listar usuarios: {str(e)}")

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
        try:
            # Buscar usuario existente
            stmt = select(UserModel).where(UserModel.id == user.id)
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()

            if model is None:
                raise UserNotFoundError(f"Usuario con ID {user.id} no encontrado")

            # Actualizar campos
            model.username = user.username
            model.email = user.email
            model.hashed_password = user.hashed_password
            model.full_name = user.full_name
            model.is_active = user.is_active
            model.updated_at = user.updated_at
            model.last_login = user.last_login
            model.must_change_password = user.must_change_password

            await self.session.flush()
            await self.session.refresh(model)

            logger.info("User updated", user_id=model.id, username=model.username)

            return self._to_domain(model)

        except UserNotFoundError:
            raise
        except IntegrityError as e:
            await self.session.rollback()
            error_msg = str(e.orig).lower()

            if "username" in error_msg:
                raise UserAlreadyExistsError(f"Ya existe un usuario con el username '{user.username}'")
            elif "email" in error_msg:
                raise UserAlreadyExistsError(f"Ya existe un usuario con el email '{user.email}'")
            else:
                raise UserAlreadyExistsError("El usuario ya existe")

        except Exception as e:
            await self.session.rollback()
            logger.error("Error updating user", user_id=user.id, error=str(e))
            raise DatabaseError(f"Error al actualizar usuario: {str(e)}")

    async def delete(self, user_id: int) -> None:
        """
        Elimina un usuario.

        Args:
            user_id: ID del usuario a eliminar

        Raises:
            UserNotFoundError: Si el usuario no existe
            DatabaseError: Si hay error de base de datos
        """
        try:
            # Buscar usuario
            stmt = select(UserModel).where(UserModel.id == user_id)
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()

            if model is None:
                raise UserNotFoundError(f"Usuario con ID {user_id} no encontrado")

            # Eliminar
            await self.session.delete(model)
            await self.session.flush()

            logger.info("User deleted", user_id=user_id)

        except UserNotFoundError:
            raise
        except Exception as e:
            await self.session.rollback()
            logger.error("Error deleting user", user_id=user_id, error=str(e))
            raise DatabaseError(f"Error al eliminar usuario: {str(e)}")

    async def count_active_users(self) -> int:
        """
        Cuenta cuántos usuarios activos hay en el sistema.

        Returns:
            Cantidad de usuarios activos
        """
        try:
            stmt = select(func.count()).select_from(UserModel).where(UserModel.is_active == True)
            result = await self.session.execute(stmt)
            count = result.scalar()

            return count

        except Exception as e:
            logger.error("Error counting active users", error=str(e))
            raise DatabaseError(f"Error al contar usuarios activos: {str(e)}")

    async def count_all_users(self) -> int:
        """
        Cuenta cuántos usuarios hay en el sistema (activos e inactivos).

        Returns:
            Cantidad total de usuarios
        """
        try:
            stmt = select(func.count()).select_from(UserModel)
            result = await self.session.execute(stmt)
            count = result.scalar()

            return count

        except Exception as e:
            logger.error("Error counting all users", error=str(e))
            raise DatabaseError(f"Error al contar todos los usuarios: {str(e)}")

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
        try:
            stmt = select(UserModel)

            if not include_inactive:
                stmt = stmt.where(UserModel.is_active == True)

            stmt = stmt.order_by(UserModel.created_at.desc())
            stmt = stmt.offset(offset).limit(limit)

            result = await self.session.execute(stmt)
            models = result.scalars().all()

            return [self._to_domain(model) for model in models]

        except Exception as e:
            logger.error("Error listing users", error=str(e))
            raise DatabaseError(f"Error al listar usuarios: {str(e)}")
