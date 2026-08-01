"""
Script para resetear la contraseña de un usuario.

Uso:
    python scripts/reset_password.py

El script pedirá el username/email del usuario y la nueva contraseña.
"""
import sys
import asyncio
from pathlib import Path
from getpass import getpass

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from dotenv import load_dotenv

# Cargar variables de entorno
env_path = root_dir / ".env"
load_dotenv(env_path, override=True)

from src.shared.config.settings import settings
from src.auth.infrastructure.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.auth.infrastructure.password_hasher import hash_password


async def reset_user_password():
    """Resetea la contraseña de un usuario."""

    print("=" * 60)
    print("  RESETEAR CONTRASENA DE USUARIO")
    print("=" * 60)
    print()

    # Conectar a la base de datos
    engine = create_async_engine(
        settings.database_url,
        echo=False,
        pool_pre_ping=True,
    )

    AsyncSessionLocal = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    async with AsyncSessionLocal() as session:
        try:
            repository = SQLAlchemyUserRepository(session)

            # Solicitar identificador del usuario
            print("Buscar usuario por:")
            identifier = input("Username o Email: ").strip()

            if not identifier:
                print("\nERROR: Debes ingresar un username o email.")
                return

            # Buscar usuario
            user = None

            # Intentar buscar por username primero
            if "@" not in identifier:
                user = await repository.find_by_username(identifier)

            # Si no se encontró, intentar por email
            if user is None:
                user = await repository.find_by_email(identifier)

            if user is None:
                print(f"\nERROR: No se encontro ningun usuario con '{identifier}'")
                return

            # Mostrar información del usuario
            print()
            print("-" * 60)
            print("Usuario encontrado:")
            print(f"  ID:       {user.id}")
            print(f"  Username: {user.username}")
            print(f"  Email:    {user.email}")
            print(f"  Nombre:   {user.full_name or '(no especificado)'}")
            print(f"  Activo:   {'Si' if user.is_active else 'No'}")
            print("-" * 60)
            print()

            # Confirmar que es el usuario correcto
            confirm = input(f"Deseas resetear la contrasena de '{user.username}'? (s/N): ").strip().lower()
            if confirm not in ['s', 'si', 'yes', 'y']:
                print("\nOperacion cancelada.")
                return

            print()

            # Solicitar nueva contraseña
            while True:
                new_password = getpass("Nueva contrasena (minimo 6 caracteres): ")
                if len(new_password) >= 6:
                    password_confirm = getpass("Confirmar contrasena: ")
                    if new_password == password_confirm:
                        break
                    else:
                        print("ERROR: Las contrasenas no coinciden. Intenta nuevamente.")
                else:
                    print("ERROR: La contrasena debe tener al menos 6 caracteres.")

            # Hashear la nueva contraseña
            hashed_password = hash_password(new_password)

            # Actualizar la contraseña en la base de datos
            user.hashed_password = hashed_password

            # Guardar cambios usando el repositorio
            await repository.update(user)
            await session.commit()

            print()
            print("=" * 60)
            print("  CONTRASENA ACTUALIZADA EXITOSAMENTE")
            print("=" * 60)
            print()
            print(f"La contrasena de '{user.username}' ha sido actualizada.")
            print()
            print("El usuario puede iniciar sesion en: http://localhost:8000/web/login")
            print()

        except Exception as e:
            await session.rollback()
            print(f"\nERROR al resetear contrasena: {str(e)}")
            print()
            raise

        finally:
            await engine.dispose()


def main():
    """Punto de entrada principal."""
    try:
        asyncio.run(reset_user_password())
    except KeyboardInterrupt:
        print("\n\nOperacion cancelada por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR inesperado: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
