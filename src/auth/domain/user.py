"""
Entidad de dominio User.

Representa un usuario del sistema con credenciales de autenticación.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """
    Usuario del sistema.

    Invariantes de dominio:
    - username no puede estar vacío después de trim
    - username no puede superar 50 caracteres
    - username debe ser único (case-sensitive)
    - email debe ser válido y único
    - email no puede superar 100 caracteres
    - hashed_password no puede estar vacío
    - full_name no puede superar 100 caracteres si está presente

    Attributes:
        id: Identificador único (autoincremental)
        username: Nombre de usuario único para login
        email: Email del usuario (único)
        hashed_password: Contraseña hasheada con bcrypt
        full_name: Nombre completo del usuario (opcional)
        is_active: Indica si el usuario está activo
        created_at: Fecha de creación del usuario
        updated_at: Fecha de última actualización
        last_login: Fecha y hora del último login (opcional)
        must_change_password: Indica si debe cambiar contraseña en próximo login
    """

    id: Optional[int]
    username: str
    email: str
    hashed_password: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    must_change_password: bool = False

    def __post_init__(self):
        """Valida la entidad después de inicializarla."""
        self._validate()

    def _validate(self):
        """
        Valida las reglas de negocio de la entidad.

        Raises:
            ValueError: Si alguna regla de negocio es violada
        """
        # Validar username
        if not self.username or not self.username.strip():
            raise ValueError("El nombre de usuario no puede estar vacío")

        if len(self.username) > 50:
            raise ValueError("El nombre de usuario no puede superar 50 caracteres")

        # Validar email
        if not self.email or not self.email.strip():
            raise ValueError("El email no puede estar vacío")

        if len(self.email) > 100:
            raise ValueError("El email no puede superar 100 caracteres")

        if "@" not in self.email:
            raise ValueError("El email debe ser válido")

        # Validar password
        if not self.hashed_password:
            raise ValueError("La contraseña no puede estar vacía")

        # Validar full_name si está presente
        if self.full_name and len(self.full_name) > 100:
            raise ValueError("El nombre completo no puede superar 100 caracteres")

    @staticmethod
    def create(
        username: str,
        email: str,
        hashed_password: str,
        full_name: Optional[str] = None,
        is_active: bool = True,
        must_change_password: bool = False,
    ) -> "User":
        """
        Factory method para crear un nuevo usuario.

        Args:
            username: Nombre de usuario único
            email: Email del usuario
            hashed_password: Contraseña ya hasheada con bcrypt
            full_name: Nombre completo (opcional)
            is_active: Si el usuario está activo (default: True)
            must_change_password: Si debe cambiar contraseña en próximo login (default: False)

        Returns:
            Nueva instancia de User

        Example:
            >>> user = User.create("admin", "admin@example.com", "hashed_pwd", "Admin User")
        """
        now = datetime.utcnow()

        return User(
            id=None,  # Se asignará al guardar
            username=username.strip(),
            email=email.strip().lower(),  # Normalizar email a minúsculas
            hashed_password=hashed_password,
            full_name=full_name.strip() if full_name else None,
            is_active=is_active,
            created_at=now,
            updated_at=now,
            last_login=None,
            must_change_password=must_change_password,
        )

    def deactivate(self) -> None:
        """Desactiva el usuario."""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """Activa el usuario."""
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def update_profile(self, full_name: Optional[str] = None, email: Optional[str] = None) -> None:
        """
        Actualiza el perfil del usuario.

        Args:
            full_name: Nuevo nombre completo (opcional)
            email: Nuevo email (opcional)

        Raises:
            ValueError: Si los datos son inválidos
        """
        if full_name is not None:
            self.full_name = full_name.strip() if full_name else None

        if email is not None:
            self.email = email.strip().lower()

        self.updated_at = datetime.utcnow()
        self._validate()

    def change_password(self, new_hashed_password: str) -> None:
        """
        Cambia la contraseña del usuario.

        Args:
            new_hashed_password: Nueva contraseña ya hasheada
        """
        if not new_hashed_password:
            raise ValueError("La contraseña no puede estar vacía")

        self.hashed_password = new_hashed_password
        self.updated_at = datetime.utcnow()

    def record_login(self) -> None:
        """Registra el momento del último login del usuario."""
        self.last_login = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def __str__(self) -> str:
        return f"User(id={self.id}, username={self.username}, email={self.email})"

    def __repr__(self) -> str:
        return self.__str__()
