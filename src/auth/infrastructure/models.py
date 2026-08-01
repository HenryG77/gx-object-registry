"""
Modelos SQLAlchemy para autenticación.
"""
from sqlalchemy import Column, String, DateTime, Boolean, Integer, func

from src.shared.database.base import Base


class UserModel(Base):
    """
    Modelo SQLAlchemy para la tabla users.

    Representa un usuario del sistema con credenciales de autenticación.
    """

    __tablename__ = "users"

    # Columnas
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Identificador único del usuario",
    )

    username = Column(
        String(50),
        nullable=False,
        unique=True,
        comment="Nombre de usuario único para login",
    )

    email = Column(
        String(100),
        nullable=False,
        unique=True,
        comment="Email del usuario (único)",
    )

    hashed_password = Column(
        String(255),
        nullable=False,
        comment="Contraseña hasheada con bcrypt",
    )

    full_name = Column(
        String(100),
        nullable=True,
        comment="Nombre completo del usuario",
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
        comment="Indica si el usuario está activo",
    )

    created_at = Column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now(),
        comment="Fecha de creación del usuario",
    )

    updated_at = Column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="Fecha de última actualización",
    )

    last_login = Column(
        DateTime(timezone=False),
        nullable=True,
        comment="Fecha y hora del último login",
    )

    must_change_password = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
        comment="Indica si el usuario debe cambiar su contraseña en el próximo login",
    )

    # Índices y restricciones
    __table_args__ = (
        {"comment": "Usuarios del sistema"},
    )

    def __repr__(self) -> str:
        return f"<UserModel(id={self.id}, username={self.username}, email={self.email})>"
