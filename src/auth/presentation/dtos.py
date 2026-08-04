"""
DTOs (Data Transfer Objects) para autenticación.

Define los modelos de Request y Response para la API REST de auth.
"""
from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime
from typing import Optional


class RegisterRequest(BaseModel):
    """Request para registrar un nuevo usuario."""

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Nombre de usuario único",
        examples=["admin", "usuario123"],
    )

    email: EmailStr = Field(
        ...,
        description="Email del usuario",
        examples=["admin@example.com", "usuario@example.com"],
    )

    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Contraseña (mínimo 6 caracteres)",
        examples=["password123"],
    )

    full_name: Optional[str] = Field(
        None,
        max_length=100,
        description="Nombre completo del usuario",
        examples=["Juan Pérez", "María García"],
    )

    @field_validator("username")
    @classmethod
    def username_must_not_be_empty(cls, v: str) -> str:
        """Valida que el username no esté vacío después de trim."""
        stripped = v.strip()
        if not stripped:
            raise ValueError("El username no puede estar vacío")
        return stripped

    @field_validator("password")
    @classmethod
    def password_must_not_be_empty(cls, v: str) -> str:
        """Valida que la contraseña no esté vacía."""
        if not v or len(v.strip()) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        return v


class LoginRequest(BaseModel):
    """Request para iniciar sesión."""

    username: str = Field(
        ...,
        min_length=1,
        description="Nombre de usuario",
        examples=["admin"],
    )

    password: str = Field(
        ...,
        min_length=1,
        description="Contraseña",
        examples=["admin123"],
    )


class TokenResponse(BaseModel):
    """Response con token de acceso."""

    access_token: str = Field(
        ...,
        description="Token JWT de acceso",
    )

    token_type: str = Field(
        default="bearer",
        description="Tipo de token",
    )

    user: "UserResponse" = Field(
        ...,
        description="Datos del usuario autenticado",
    )


class UserResponse(BaseModel):
    """Response con datos del usuario."""

    id: int = Field(
        ...,
        description="ID del usuario",
        examples=[1, 2, 3],
    )

    username: str = Field(
        ...,
        description="Nombre de usuario",
        examples=["admin", "usuario123"],
    )

    email: str = Field(
        ...,
        description="Email del usuario",
        examples=["admin@example.com"],
    )

    full_name: Optional[str] = Field(
        None,
        description="Nombre completo",
        examples=["Juan Pérez"],
    )

    is_active: bool = Field(
        ...,
        description="Si el usuario está activo",
        examples=[True],
    )

    created_at: datetime = Field(
        ...,
        description="Fecha de creación",
    )

    last_login: Optional[datetime] = Field(
        None,
        description="Fecha y hora del último login",
    )

    must_change_password: bool = Field(
        ...,
        description="Si el usuario debe cambiar su contraseña",
        examples=[False],
    )

    class Config:
        from_attributes = True


# Para que TokenResponse pueda referenciar a UserResponse
TokenResponse.model_rebuild()


class UpdateUserRequest(BaseModel):
    """Request para actualizar un usuario."""

    full_name: Optional[str] = Field(
        None,
        max_length=100,
        description="Nuevo nombre completo",
        examples=["Juan Pérez"],
    )

    email: Optional[EmailStr] = Field(
        None,
        description="Nuevo email",
        examples=["nuevo@example.com"],
    )


class ChangePasswordRequest(BaseModel):
    """Request para cambiar la propia contraseña."""

    current_password: Optional[str] = Field(
        None,
        min_length=6,
        max_length=100,
        description="Contraseña actual (requerida si no es cambio forzado)",
        examples=["oldpassword123"],
    )

    new_password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Nueva contraseña (mínimo 6 caracteres)",
        examples=["newpassword123"],
    )

    @field_validator("new_password")
    @classmethod
    def password_must_not_be_empty(cls, v: str) -> str:
        """Valida que la nueva contraseña no esté vacía."""
        if not v or len(v.strip()) < 6:
            raise ValueError("La nueva contraseña debe tener al menos 6 caracteres")
        return v


class ResetPasswordRequest(BaseModel):
    """
    Request para resetear la contraseña de un usuario (admin).

    Ya no requiere password - se genera automáticamente usando el username.
    """

    pass


class ToggleStatusRequest(BaseModel):
    """Request para activar/desactivar un usuario."""

    is_active: bool = Field(
        ...,
        description="True para activar, False para desactivar",
        examples=[True, False],
    )


class UserListResponse(BaseModel):
    """Response con lista paginada de usuarios."""

    items: list[UserResponse] = Field(..., description="Lista de usuarios")
    total: int = Field(..., description="Total de registros")
    page: int = Field(..., description="Página actual")
    page_size: int = Field(..., description="Tamaño de página")
    total_pages: int = Field(..., description="Total de páginas")

    @staticmethod
    def create(
        items: list[UserResponse],
        total: int,
        page: int,
        page_size: int,
    ) -> "UserListResponse":
        """
        Factory method para crear la respuesta paginada.

        Args:
            items: Lista de usuarios
            total: Total de registros
            page: Página actual
            page_size: Tamaño de página

        Returns:
            Respuesta paginada
        """
        total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0

        return UserListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )


class UserStatsResponse(BaseModel):
    """Response con estadísticas de un usuario."""

    user_id: int = Field(..., description="ID del usuario")
    username: str = Field(..., description="Nombre de usuario")
    full_name: Optional[str] = Field(None, description="Nombre completo")
    total_object_types_created: int = Field(..., description="Total de tipos de objetos creados")
    total_genexus_objects_created: int = Field(..., description="Total de objetos GeneXus creados")

    class Config:
        from_attributes = True
