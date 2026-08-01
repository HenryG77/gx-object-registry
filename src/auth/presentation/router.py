"""
Router de FastAPI para autenticación.

Define los endpoints REST para registro, login, logout y obtener usuario actual.
"""
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.application.authenticate_user import AuthenticateUser
from src.auth.application.register_user import RegisterUser
from src.auth.application.change_own_password import ChangeOwnPassword
from src.auth.infrastructure.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.auth.presentation.dependencies import get_current_user
from src.auth.presentation.dtos import (
    ChangePasswordRequest,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from src.shared.database.connection import get_session

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# ============================================================================
# Dependency para obtener el repositorio
# ============================================================================


def get_repository(
    session: AsyncSession = Depends(get_session),
) -> SQLAlchemyUserRepository:
    """
    Dependency injection del repositorio de usuarios.

    Args:
        session: Sesión de base de datos

    Returns:
        Repositorio de usuarios
    """
    return SQLAlchemyUserRepository(session)


# ============================================================================
# Endpoints
# ============================================================================


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuario",
    description="Registra un nuevo usuario en el sistema.",
)
async def register(
    request: RegisterRequest,
    repository: SQLAlchemyUserRepository = Depends(get_repository),
):
    """
    Registra un nuevo usuario.

    Args:
        request: Datos del usuario a registrar
        repository: Repositorio de usuarios

    Returns:
        Usuario creado

    Raises:
        409: Si ya existe un usuario con ese username o email
        400: Si los datos son inválidos
    """
    use_case = RegisterUser(repository)
    user = await use_case.execute(
        username=request.username,
        email=request.email,
        password=request.password,
        full_name=request.full_name,
    )
    return UserResponse.model_validate(user)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Iniciar sesión",
    description="Autentica un usuario y devuelve un token JWT.",
)
async def login(
    request: LoginRequest,
    response: Response,
    repository: SQLAlchemyUserRepository = Depends(get_repository),
):
    """
    Inicia sesión y devuelve un token JWT.

    El token también se guarda en una cookie HttpOnly para mayor seguridad.

    Args:
        request: Credenciales del usuario
        response: Response de FastAPI para configurar cookies
        repository: Repositorio de usuarios

    Returns:
        Token de acceso y datos del usuario

    Raises:
        401: Si las credenciales son incorrectas
    """
    use_case = AuthenticateUser(repository)
    user, access_token = await use_case.execute(
        username=request.username,
        password=request.password,
    )

    # Configurar cookie HttpOnly con el token
    # max_age en segundos (365 días = 31536000 segundos)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # No accesible desde JavaScript (protección XSS)
        samesite="lax",  # Protección CSRF
        max_age=31536000,  # 365 días en segundos
        secure=False,  # TODO: Cambiar a True en producción (requiere HTTPS)
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario actual",
    description="Obtiene los datos del usuario autenticado actualmente.",
)
async def get_me(
    current_user=Depends(get_current_user),
):
    """
    Obtiene el usuario actual desde el token JWT.

    Args:
        current_user: Usuario autenticado (inyectado por dependencia)

    Returns:
        Datos del usuario actual

    Raises:
        401: Si no está autenticado o el token es inválido
    """
    return UserResponse.model_validate(current_user)


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cerrar sesión",
    description="Cierra la sesión del usuario eliminando la cookie de autenticación.",
)
async def logout(
    response: Response,
):
    """
    Cierra la sesión eliminando la cookie de autenticación.

    Args:
        response: Response de FastAPI para eliminar cookies

    Returns:
        Sin contenido (204)
    """
    # Eliminar cookie de autenticación
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
    )
    return None


@router.post(
    "/change-password",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Cambiar contraseña",
    description="Permite al usuario cambiar su propia contraseña.",
)
async def change_password(
    request: ChangePasswordRequest,
    current_user=Depends(get_current_user),
    repository: SQLAlchemyUserRepository = Depends(get_repository),
):
    """
    Cambia la contraseña del usuario actual.

    Si el usuario tiene must_change_password=True (contraseña temporal),
    no necesita proporcionar la contraseña actual.

    Args:
        request: Nueva contraseña y opcionalmente contraseña actual
        current_user: Usuario autenticado
        repository: Repositorio de usuarios

    Returns:
        Usuario actualizado

    Raises:
        400: Si los datos son inválidos o la contraseña actual es incorrecta
        401: Si no está autenticado
    """
    use_case = ChangeOwnPassword(repository)
    updated_user = await use_case.execute(
        user_id=current_user.id,
        new_password=request.new_password,
        current_password=request.current_password,
    )
    return UserResponse.model_validate(updated_user)
