"""
Utilidades para hashear y verificar contraseñas.

Usa bcrypt para hashear las contraseñas de forma segura.
"""
import bcrypt


def hash_password(password: str) -> str:
    """
    Hashea una contraseña usando bcrypt.

    Args:
        password: Contraseña en texto plano

    Returns:
        Contraseña hasheada

    Example:
        >>> hashed = hash_password("mi_password_segura")
        >>> print(hashed)  # $2b$12$...
    """
    # Convertir a bytes y generar hash
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con su hash.

    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Contraseña hasheada

    Returns:
        True si coincide, False si no

    Example:
        >>> hashed = hash_password("mi_password")
        >>> verify_password("mi_password", hashed)
        True
        >>> verify_password("otra_password", hashed)
        False
    """
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)
