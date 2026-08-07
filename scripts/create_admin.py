"""
Script para crear el usuario administrador inicial.

Uso:
    python scripts/create_admin.py

El script pedirá las credenciales del usuario administrador.
Si ya existe un usuario admin, se mostrará un mensaje y no se creará otro.
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
from src.auth.domain.user import User
from src.auth.infrastructure.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.auth.application.register_user import RegisterUser


async def create_admin_user():
    """Crea el usuario administrador inicial."""

    print("=" * 60)
    print("  CREAR USUARIO ADMINISTRADOR")
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

            # Verificar si ya existe algún usuario
            total_users = await repository.count_active_users()

            if total_users > 0:
                print(f"⚠️  Ya existen {total_users} usuario(s) en el sistema.")
                print()

                response = input("¿Deseas crear un usuario adicional de todos modos? (s/N): ").strip().lower()
                if response not in ['s', 'si', 'yes', 'y']:
                    print("\nOperación cancelada.")
                    return
                print()

            # Solicitar datos del usuario
            print("Ingresa los datos del nuevo usuario:")
            print("-" * 60)

            # Username
            while True:
                username = input("Username (3-50 caracteres): ").strip()
                if len(username) >= 3 and len(username) <= 50:
                    break
                print("❌ El username debe tener entre 3 y 50 caracteres.")

            # Email
            while True:
                email = input("Email: ").strip()
                if '@' in email and '.' in email:
                    break
                print("❌ El email no es válido.")

            # Full name
            full_name = input("Nombre completo (opcional): ").strip()
            if not full_name:
                full_name = None

            # Password
            while True:
                password = getpass("Contraseña (mínimo 6 caracteres): ")
                if len(password) >= 6:
                    password_confirm = getpass("Confirmar contraseña: ")
                    if password == password_confirm:
                        break
                    else:
                        print("❌ Las contraseñas no coinciden. Intenta nuevamente.")
                else:
                    print("❌ La contraseña debe tener al menos 6 caracteres.")

            print()
            print("-" * 60)
            print("Datos del usuario:")
            print(f"  Username:  {username}")
            print(f"  Email:     {email}")
            print(f"  Nombre:    {full_name or '(no especificado)'}")
            print("-" * 60)
            print()

            # Confirmar creación
            confirm = input("¿Crear este usuario? (S/n): ").strip().lower()
            if confirm in ['n', 'no']:
                print("\nOperación cancelada.")
                return

            # Crear usuario
            print("\nCreando usuario...")

            use_case = RegisterUser(repository)
            user = await use_case.execute(
                username=username,
                email=email,
                password=password,
                full_name=full_name,
            )

            await session.commit()

            print()
            print("✅ Usuario creado exitosamente!")
            print()
            print("=" * 60)
            print("  CREDENCIALES DE ACCESO")
            print("=" * 60)
            print(f"  Username:  {user.username}")
            print(f"  Email:     {user.email}")
            print(f"  Nombre:    {user.full_name or '(no especificado)'}")
            print(f"  ID:        {user.id}")
            print("=" * 60)
            print()
            #print("Puedes iniciar sesión en: http://localhost:8000/web/login")
            print()

        except Exception as e:
            await session.rollback()
            print(f"\n❌ Error al crear usuario: {str(e)}")
            print()
            raise

        finally:
            await engine.dispose()


def main():
    """Punto de entrada principal."""
    try:
        asyncio.run(create_admin_user())
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
