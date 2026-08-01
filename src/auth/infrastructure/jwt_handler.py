"""
Utilidades para crear y verificar tokens JWT.

Usa python-jose para manejar JSON Web Tokens de forma segura.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from jose import JWTError, jwt

from src.shared.config.settings import settings


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT de acceso.

    Args:
        data: Datos a incluir en el payload del token (ej: {"sub": "1"})
        expires_delta: Tiempo de expiración personalizado (opcional)

    Returns:
        Token JWT codificado

    Example:
        >>> token = create_access_token({"sub": "1"})
        >>> print(token)  # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    """
    to_encode = data.copy()

    # Calcular tiempo de expiración
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Usar el valor de configuración (365 días por defecto)
        expire = datetime.utcnow() + timedelta(days=settings.access_token_expire_days)

    to_encode.update({"exp": expire})

    # Codificar el token
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verifica y decodifica un token JWT.

    Args:
        token: Token JWT a verificar

    Returns:
        Payload del token si es válido, None si es inválido o expirado

    Example:
        >>> token = create_access_token({"sub": "1"})
        >>> payload = verify_token(token)
        >>> print(payload)  # {"sub": "1", "exp": ...}
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        # Token inválido, expirado o firma incorrecta
        return None


def get_user_id_from_token(token: str) -> Optional[int]:
    """
    Extrae el ID de usuario de un token JWT.

    Args:
        token: Token JWT

    Returns:
        ID del usuario si el token es válido, None si no lo es

    Example:
        >>> token = create_access_token({"sub": "1"})
        >>> user_id = get_user_id_from_token(token)
        >>> print(user_id)  # 1
    """
    payload = verify_token(token)
    if payload is None:
        return None

    user_id_str = payload.get("sub")
    if user_id_str is None:
        return None

    try:
        return int(user_id_str)
    except (ValueError, TypeError):
        return None
