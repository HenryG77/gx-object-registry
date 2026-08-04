"""
Dependencias de autenticación para FastAPI.

Define las dependencias que se inyectan en los endpoints protegidos.
"""
from typing import Optional

from fastapi import Cookie, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.application.get_current_user import GetCurrentUser
from src.auth.domain.user import User
from src.auth.infrastructure.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.shared.database.connection import get_session
from src.shared.errors.exceptions import UnauthorizedError


async def get_current_user(
    access_token: Optional[str] = Cookie(None),
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_session),
) -> User:
    """
    Dependencia para obtener el usuario actual desde el token JWT.

    Busca el token en (por orden de prioridad):
    1. Cookie "access_token"
    2. Header "Authorization" (formato: "Bearer {token}")

    Args:
        access_token: Token JWT desde cookie
        authorization: Header de autorización
        db: Sesión de base de datos

    Returns:
        Usuario autenticado

    Raises:
        HTTPException 401: Si no se proporciona token o es inválido
    """
    # Extraer token desde cookie o header
    token = None

    if access_token:
        token = access_token
    elif authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Ejecutar caso de uso
    repository = SQLAlchemyUserRepository(db)
    use_case = GetCurrentUser(repository)

    try:
        user = await use_case.execute(token)
        return user
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e.message),
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_optional_current_user(
    access_token: Optional[str] = Cookie(None),
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_session),
) -> Optional[User]:
    """
    Dependencia opcional para obtener el usuario actual si está autenticado.

    Similar a get_current_user pero NO lanza excepción si no hay token.
    Útil para endpoints que funcionan con o sin autenticación.

    Args:
        access_token: Token JWT desde cookie
        authorization: Header de autorización
        db: Sesión de base de datos

    Returns:
        Usuario autenticado o None si no hay token
    """
    # Extraer token desde cookie o header
    token = None

    if access_token:
        token = access_token
    elif authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")

    if not token:
        return None

    # Ejecutar caso de uso
    repository = SQLAlchemyUserRepository(db)
    use_case = GetCurrentUser(repository)

    try:
        user = await use_case.execute(token)
        return user
    except UnauthorizedError:
        return None
