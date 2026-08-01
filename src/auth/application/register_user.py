"""
Caso de uso: Registrar nuevo usuario.
"""
from typing import Optional

from src.auth.domain.user import User
from src.auth.domain.user_repository import UserRepository
from src.auth.infrastructure.password_hasher import hash_password
from src.shared.errors.exceptions import UserAlreadyExistsError, ValidationError
from src.shared.logging.logger import logger


class RegisterUser:
    """
    Caso de uso para registrar un nuevo usuario.

    Flujo:
    1. Validar datos del usuario
    2. Verificar que no exista username duplicado
    3. Verificar que no exista email duplicado
    4. Hashear la contraseña
    5. Crear la entidad de dominio
    6. Persistir en el repositorio
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
        username: str,
        email: str,
        password: str,
        full_name: Optional[str] = None,
    ) -> User:
        """
        Ejecuta el caso de uso.

        Args:
            username: Nombre de usuario único
            email: Email del usuario
            password: Contraseña en texto plano (será hasheada)
            full_name: Nombre completo (opcional)

        Returns:
            Usuario creado

        Raises:
            UserAlreadyExistsError: Si ya existe un usuario con ese username o email
            ValidationError: Si los datos son inválidos
        """
        # Validar que la contraseña no esté vacía
        if not password or len(password.strip()) < 6:
            raise ValidationError("La contraseña debe tener al menos 6 caracteres")

        # Normalizar datos
        normalized_username = username.strip()
        normalized_email = email.strip().lower()

        # Verificar que no exista el username
        if await self.repository.exists_by_username(normalized_username):
            logger.warning(
                "Attempt to register user with duplicate username",
                username=normalized_username,
            )
            raise UserAlreadyExistsError(f"Ya existe un usuario con el username '{normalized_username}'")

        # Verificar que no exista el email
        if await self.repository.exists_by_email(normalized_email):
            logger.warning(
                "Attempt to register user with duplicate email",
                email=normalized_email,
            )
            raise UserAlreadyExistsError(f"Ya existe un usuario con el email '{normalized_email}'")

        # Hashear la contraseña
        hashed_password = hash_password(password)

        # Detectar si la contraseña es temporal (igual al username)
        is_temp_password = password.strip() == normalized_username

        # Crear entidad de dominio (se valida automáticamente)
        user = User.create(
            username=normalized_username,
            email=normalized_email,
            hashed_password=hashed_password,
            full_name=full_name,
            is_active=True,
            must_change_password=is_temp_password,
        )

        # Persistir
        created = await self.repository.create(user)

        logger.info(
            "User registered successfully",
            user_id=created.id,
            username=created.username,
        )

        return created
