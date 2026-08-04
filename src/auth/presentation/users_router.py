"""
Router para gestión de usuarios (endpoints de administración).
"""
from typing import Annotated
from fastapi import APIRouter, Depends, Query, Path, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.database.connection import get_session
from src.auth.domain.user import User
from src.auth.presentation.dependencies import get_current_user
from src.auth.presentation.dtos import (
    UserResponse,
    UserListResponse,
    UpdateUserRequest,
    ResetPasswordRequest,
    ToggleStatusRequest,
    UserStatsResponse,
)
from src.auth.infrastructure.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.auth.application.list_users import ListUsers
from src.auth.application.update_user import UpdateUser
from src.auth.application.reset_user_password import ResetUserPassword
from src.auth.application.toggle_user_status import ToggleUserStatus
from src.auth.application.get_user_stats import GetUserStats
from src.shared.errors.exceptions import UserNotFoundError, UserAlreadyExistsError

router = APIRouter(prefix="/users", tags=["Users Management"])


def get_repository(session: AsyncSession = Depends(get_session)) -> SQLAlchemyUserRepository:
    """Dependency para obtener el repositorio de usuarios."""
    return SQLAlchemyUserRepository(session)


@router.get("", response_model=UserListResponse)
async def list_users(
    page: Annotated[int, Query(ge=1, description="Número de página")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Tamaño de página")] = 50,
    include_inactive: Annotated[bool, Query(description="Incluir usuarios inactivos")] = False,
    current_user: User = Depends(get_current_user),
    repository: SQLAlchemyUserRepository = Depends(get_repository),
):
    """
    Lista todos los usuarios con paginación.

    Requiere autenticación.
    """
    use_case = ListUsers(repository)
    users, total = await use_case.execute(
        page=page,
        page_size=page_size,
        include_inactive=include_inactive,
    )

    # Convertir a DTOs
    user_responses = [UserResponse.model_validate(user) for user in users]

    return UserListResponse.create(
        items=user_responses,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: Annotated[int, Path(description="ID del usuario")],
    current_user: User = Depends(get_current_user),
    repository: SQLAlchemyUserRepository = Depends(get_repository),
):
    """
    Obtiene un usuario por ID.

    Requiere autenticación.
    """
    user = await repository.find_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado",
        )

    return UserResponse.model_validate(user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: Annotated[int, Path(description="ID del usuario")],
    request: UpdateUserRequest,
    current_user: User = Depends(get_current_user),
    repository: SQLAlchemyUserRepository = Depends(get_repository),
):
    """
    Actualiza la información de un usuario.

    Requiere autenticación.
    """
    try:
        use_case = UpdateUser(repository)
        updated_user = await use_case.execute(
            user_id=user_id,
            full_name=request.full_name,
            email=request.email,
        )

        return UserResponse.model_validate(updated_user)

    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/{user_id}/reset-password", response_model=UserResponse)
async def reset_password(
    user_id: Annotated[int, Path(description="ID del usuario")],
    current_user: User = Depends(get_current_user),
    repository: SQLAlchemyUserRepository = Depends(get_repository),
):
    """
    Resetea la contraseña de un usuario (solo admin).

    La contraseña temporal será igual al username del usuario.
    El usuario deberá cambiarla en el próximo login.

    Requiere autenticación.
    """
    try:
        use_case = ResetUserPassword(repository)
        updated_user = await use_case.execute(user_id=user_id)

        return UserResponse.model_validate(updated_user)

    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.patch("/{user_id}/status", response_model=UserResponse)
async def toggle_status(
    user_id: Annotated[int, Path(description="ID del usuario")],
    request: ToggleStatusRequest,
    current_user: User = Depends(get_current_user),
    repository: SQLAlchemyUserRepository = Depends(get_repository),
):
    """
    Activa o desactiva un usuario.

    Requiere autenticación.
    """
    try:
        use_case = ToggleUserStatus(repository)
        updated_user = await use_case.execute(
            user_id=user_id,
            is_active=request.is_active,
        )

        return UserResponse.model_validate(updated_user)

    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get("/{user_id}/stats", response_model=UserStatsResponse)
async def get_stats(
    user_id: Annotated[int, Path(description="ID del usuario")],
    current_user: User = Depends(get_current_user),
    user_repository: SQLAlchemyUserRepository = Depends(get_repository),
):
    """
    Obtiene estadísticas de un usuario (objetos creados, etc.).

    Requiere autenticación.
    """
    try:
        # Por ahora no tenemos los repositorios de object_type y genexus_object
        # así que retornaremos valores básicos
        user = await user_repository.find_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado",
            )

        return UserStatsResponse(
            user_id=user.id,
            username=user.username,
            full_name=user.full_name,
            total_object_types_created=0,  # TODO: implementar conteo
            total_genexus_objects_created=0,  # TODO: implementar conteo
        )

    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
