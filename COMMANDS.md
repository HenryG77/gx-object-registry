# Comandos - GeneXus Object Registry

Este documento contiene **todos los comandos disponibles** para trabajar con el proyecto, organizados por tecnología, herramienta y propósito.

---

## Tabla de Contenidos

1. [Comandos Generales del Proyecto](#1-comandos-generales-del-proyecto)
2. [Gestión de Dependencias](#2-gestión-de-dependencias)
3. [Backend (FastAPI)](#3-backend-fastapi)
4. [Base de Datos](#4-base-de-datos)
5. [Scripts de Utilidad](#5-scripts-de-utilidad)
6. [Docker](#6-docker)
7. [Git y Flujo de Trabajo](#7-git-y-flujo-de-trabajo)
8. [Variables de Entorno](#8-variables-de-entorno)
9. [Testing](#9-testing)
10. [Linting y Formateo](#10-linting-y-formateo)
11. [Build y Producción](#11-build-y-producción)
12. [Comandos Peligrosos](#12-comandos-peligrosos)
13. [Tabla de Referencia Rápida](#13-tabla-de-referencia-rápida)

---

## 1. Comandos Generales del Proyecto

### Instalación Inicial

| Comando | Descripción |
|---------|-------------|
| `python -m venv venv` | Crear entorno virtual Python |
| `venv\Scripts\activate` | Activar entorno virtual (Windows) |
| `source venv/bin/activate` | Activar entorno virtual (Linux/macOS) |
| `pip install -r requirements.txt` | Instalar todas las dependencias |
| `alembic upgrade head` | Ejecutar migraciones de base de datos |
| `python scripts/create_admin.py` | Crear usuario administrador inicial |

### Iniciar Servidor

| Comando | Descripción |
|---------|-------------|
| `uvicorn src.main:app --reload` | Iniciar servidor en modo desarrollo (localhost:8000) |
| `uvicorn src.main:app --reload --host 0.0.0.0 --port 8000` | Iniciar y permitir acceso desde red local |
| `uvicorn src.main:app --reload --port 8001` | Iniciar en puerto diferente (8001) |

### Detener Servidor

| Comando | Descripción |
|---------|-------------|
| `Ctrl+C` | Detener servidor Uvicorn (en la terminal donde está corriendo) |

---

## 2. Gestión de Dependencias

**Gestor de paquetes**: `pip`

### Dependencias del Proyecto

| Comando | Descripción |
|---------|-------------|
| `pip install -r requirements.txt` | Instalar todas las dependencias |
| `pip install --upgrade pip` | Actualizar pip a la última versión |
| `pip list` | Ver paquetes instalados |
| `pip freeze > requirements.txt` | Generar archivo de dependencias |
| `pip install <paquete>` | Instalar un paquete específico |
| `pip uninstall <paquete>` | Desinstalar un paquete |
| `pip show <paquete>` | Ver información de un paquete instalado |

### Verificar Dependencias

| Comando | Descripción |
|---------|-------------|
| `pip check` | Verificar dependencias instaladas |
| `pip list --outdated` | Ver paquetes desactualizados |

---

## 3. Backend (FastAPI)

### Servidor de Desarrollo

| Comando | Descripción |
|---------|-------------|
| `uvicorn src.main:app --reload` | Iniciar con auto-reload |
| `uvicorn src.main:app --reload --log-level debug` | Iniciar con logs detallados |
| `uvicorn src.main:app --reload --host 0.0.0.0` | Permitir acceso desde cualquier IP |
| `uvicorn src.main:app --reload --port 8080` | Usar puerto personalizado |

### Servidor de Producción

| Comando | Descripción |
|---------|-------------|
| `uvicorn src.main:app --host 0.0.0.0 --port 8000` | Iniciar sin reload (producción) |
| `uvicorn src.main:app --workers 4 --host 0.0.0.0` | Iniciar con 4 workers |
| `gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000` | Producción con Gunicorn |

### Verificar Aplicación

| Comando | Descripción |
|---------|-------------|
| `curl http://localhost:8000/health` | Verificar health check |
| `curl http://localhost:8000/docs` | Acceder a docs (en navegador mejor) |

---

## 4. Base de Datos

### Configuración Inicial

#### Crear Base de Datos PostgreSQL

```bash
# Conectar a PostgreSQL
psql -U postgres

# En el shell de PostgreSQL:
CREATE USER gxregistry WITH PASSWORD 'gxregistry123';
CREATE DATABASE gxregistry_db OWNER gxregistry;
GRANT ALL PRIVILEGES ON DATABASE gxregistry_db TO gxregistry;
\q
```

#### Verificar Conexión

| Comando | Descripción |
|---------|-------------|
| `psql -U gxregistry -d gxregistry_db -h localhost` | Conectar a la base de datos |
| `psql -U postgres -d gxregistry_db` | Conectar como superusuario |

### Migraciones con Alembic

#### Ver Estado

| Comando | Descripción |
|---------|-------------|
| `alembic current` | Ver revisión actual de la base de datos |
| `alembic history` | Ver historial de migraciones |
| `alembic history --verbose` | Ver historial detallado |

#### Ejecutar Migraciones

| Comando | Descripción |
|---------|-------------|
| `alembic upgrade head` | Aplicar todas las migraciones pendientes |
| `alembic upgrade +1` | Aplicar solo la siguiente migración |
| `alembic upgrade <revision>` | Aplicar hasta una revisión específica |

#### Revertir Migraciones

| Comando | Descripción |
|---------|-------------|
| `alembic downgrade -1` | Revertir la última migración |
| `alembic downgrade <revision>` | Revertir hasta una revisión específica |
| `alembic downgrade base` | ⚠️ Revertir TODAS las migraciones |

#### Crear Migraciones

| Comando | Descripción |
|---------|-------------|
| `alembic revision --autogenerate -m "Descripción del cambio"` | Crear migración automática |
| `alembic revision -m "Descripción"` | Crear migración vacía (manual) |

**Ejemplo**:
```bash
# Modificar modelo en src/auth/infrastructure/models.py
# Luego crear migración automática:
alembic revision --autogenerate -m "Add phone_number to users"

# Revisar archivo generado en alembic/versions/
# Aplicar migración:
alembic upgrade head
```

### Consultas Directas

| Comando | Descripción |
|---------|-------------|
| `psql -U gxregistry -d gxregistry_db -c "SELECT * FROM users;"` | Consultar usuarios |
| `psql -U gxregistry -d gxregistry_db -c "SELECT COUNT(*) FROM genexus_objects;"` | Contar objetos |

---

## 5. Scripts de Utilidad

Todos los scripts se encuentran en la carpeta `/scripts/`.

### Gestión de Usuarios

| Comando | Descripción |
|---------|-------------|
| `python scripts/create_admin.py` | Crear un nuevo usuario (interactivo) |
| `python scripts/reset_password.py` | Resetear contraseña de un usuario (interactivo) |

**Ejemplo de uso**:
```bash
# Crear usuario
python scripts/create_admin.py
# Te pedirá: username, email, full_name, password

# Resetear contraseña
python scripts/reset_password.py
# Te pedirá: username o email, nueva contraseña
```

### Gestión de Base de Datos

| Comando | Descripción |
|---------|-------------|
| `python scripts/seed_database.py` | Cargar datos iniciales (tipos de objetos) |
| `python scripts/setup_completo.py` | Setup completo de base de datos |
| `python scripts/limpiar_datos.py` | ⚠️ Limpiar datos de tablas |
| `python scripts/reset_database.py` | ⚠️ Resetear base de datos completamente |
| `python scripts/permitir_ids_manuales.py` | Configurar IDs manuales en tablas |

> ⚠️ **ADVERTENCIA**: Los scripts marcados con ⚠️ pueden eliminar datos. Úsalos con precaución.

---

## 6. Docker

### Docker Compose

#### Levantar Servicios

| Comando | Descripción |
|---------|-------------|
| `docker-compose up` | Levantar todos los servicios (foreground) |
| `docker-compose up -d` | Levantar en segundo plano (detached) |
| `docker-compose up postgres` | Levantar solo PostgreSQL |
| `docker-compose up --build` | Reconstruir imágenes y levantar |
| `docker-compose up --force-recreate` | Forzar recreación de contenedores |

#### Detener Servicios

| Comando | Descripción |
|---------|-------------|
| `docker-compose down` | Detener y eliminar contenedores |
| `docker-compose down -v` | ⚠️ Detener y eliminar volúmenes (datos de BD) |
| `docker-compose stop` | Detener contenedores (sin eliminar) |
| `docker-compose stop postgres` | Detener solo PostgreSQL |

#### Ver Estado y Logs

| Comando | Descripción |
|---------|-------------|
| `docker-compose ps` | Ver estado de servicios |
| `docker-compose logs` | Ver logs de todos los servicios |
| `docker-compose logs -f` | Ver logs en tiempo real (follow) |
| `docker-compose logs -f api` | Ver logs solo del servicio API |
| `docker-compose logs --tail=50 postgres` | Ver últimas 50 líneas de PostgreSQL |

#### Ejecutar Comandos en Contenedores

| Comando | Descripción |
|---------|-------------|
| `docker-compose exec api bash` | Abrir shell en contenedor API |
| `docker-compose exec postgres psql -U gxuser -d gx_object_registry` | Abrir psql en PostgreSQL |
| `docker-compose exec api alembic upgrade head` | Ejecutar migraciones en contenedor |
| `docker-compose exec api python scripts/create_admin.py` | Crear admin en contenedor |

#### Reconstruir y Limpiar

| Comando | Descripción |
|---------|-------------|
| `docker-compose build` | Reconstruir imágenes |
| `docker-compose build --no-cache` | Reconstruir sin usar cache |
| `docker-compose down --rmi all` | ⚠️ Eliminar contenedores e imágenes |
| `docker-compose down -v --rmi all --remove-orphans` | ⚠️ Limpieza completa |

### Docker (sin Compose)

| Comando | Descripción |
|---------|-------------|
| `docker ps` | Ver contenedores corriendo |
| `docker ps -a` | Ver todos los contenedores |
| `docker images` | Ver imágenes descargadas |
| `docker logs <container_id>` | Ver logs de un contenedor |
| `docker exec -it <container_id> bash` | Entrar a un contenedor |
| `docker stop <container_id>` | Detener un contenedor |
| `docker rm <container_id>` | Eliminar un contenedor |
| `docker rmi <image_id>` | Eliminar una imagen |

---

## 7. Git y Flujo de Trabajo

### Comandos Básicos

| Comando | Descripción |
|---------|-------------|
| `git clone <url>` | Clonar repositorio |
| `git status` | Ver estado de cambios |
| `git add .` | Agregar todos los cambios al stage |
| `git add <archivo>` | Agregar archivo específico |
| `git commit -m "Mensaje"` | Crear commit con mensaje |
| `git push` | Subir cambios al repositorio remoto |
| `git pull` | Descargar cambios del repositorio remoto |

### Ramas

| Comando | Descripción |
|---------|-------------|
| `git branch` | Ver ramas locales |
| `git branch <nombre>` | Crear nueva rama |
| `git checkout <rama>` | Cambiar a rama |
| `git checkout -b <rama>` | Crear y cambiar a nueva rama |
| `git merge <rama>` | Fusionar rama actual con otra |
| `git branch -d <rama>` | Eliminar rama local |

### Historial

| Comando | Descripción |
|---------|-------------|
| `git log` | Ver historial de commits |
| `git log --oneline` | Ver historial resumido |
| `git log --graph --all` | Ver historial gráfico |
| `git diff` | Ver cambios no staged |
| `git diff --staged` | Ver cambios staged |

---

## 8. Variables de Entorno

### Crear y Configurar

| Comando | Descripción |
|---------|-------------|
| `cp .env.example .env` | Copiar plantilla (Linux/macOS) |
| `copy .env.example .env` | Copiar plantilla (Windows) |
| `nano .env` | Editar con nano (Linux/macOS) |
| `notepad .env` | Editar con notepad (Windows) |
| `code .env` | Editar con VS Code |

### Generar SECRET_KEY

| Comando | Descripción |
|---------|-------------|
| `python -c "import secrets; print(secrets.token_urlsafe(32))"` | Generar clave secreta segura |

**Ejemplo**:
```bash
# Generar y guardar en .env
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
# Copia el resultado a tu archivo .env
```

### Verificar Variables

| Comando | Descripción |
|---------|-------------|
| `cat .env` | Ver contenido (Linux/macOS) |
| `type .env` | Ver contenido (Windows) |

---

## 9. Testing

### Ejecutar Tests

| Comando | Descripción |
|---------|-------------|
| `pytest` | Ejecutar todos los tests |
| `pytest -v` | Ejecutar con salida verbose |
| `pytest tests/unit/` | Ejecutar solo tests unitarios |
| `pytest tests/integration/` | Ejecutar solo tests de integración |
| `pytest tests/unit/auth/test_user.py` | Ejecutar archivo específico |
| `pytest tests/unit/auth/test_user.py::test_create_user` | Ejecutar test específico |
| `pytest -k "user"` | Ejecutar tests que contengan "user" |
| `pytest --maxfail=1` | Detener al primer fallo |

### Cobertura de Código

| Comando | Descripción |
|---------|-------------|
| `pytest --cov=src` | Ejecutar tests con cobertura |
| `pytest --cov=src --cov-report=html` | Generar reporte HTML |
| `pytest --cov=src --cov-report=term-missing` | Ver líneas sin cobertura |
| `pytest --cov=src --cov-report=xml` | Generar reporte XML |

**Ver reporte HTML**:
```bash
pytest --cov=src --cov-report=html
# Abre htmlcov/index.html en el navegador
```

### Tests en Modo Watch

| Comando | Descripción |
|---------|-------------|
| `pytest-watch` | Ejecutar tests automáticamente al guardar cambios |

**Nota**: Requiere instalar `pytest-watch`:
```bash
pip install pytest-watch
```

---

## 10. Linting y Formateo

### Black (Formateador)

| Comando | Descripción |
|---------|-------------|
| `black src/` | Formatear código en src/ |
| `black src/ tests/` | Formatear src/ y tests/ |
| `black src/ --check` | Verificar sin modificar archivos |
| `black src/ --diff` | Ver diferencias sin aplicar |
| `black .` | Formatear todo el proyecto |

### Ruff (Linter)

| Comando | Descripción |
|---------|-------------|
| `ruff check src/` | Verificar código en src/ |
| `ruff check src/ --fix` | Corregir errores automáticamente |
| `ruff check .` | Verificar todo el proyecto |
| `ruff check src/ --watch` | Modo watch (auto-check al guardar) |

### mypy (Type Checker)

| Comando | Descripción |
|---------|-------------|
| `mypy src/` | Verificar tipos en src/ |
| `mypy src/ --strict` | Verificar con modo strict |
| `mypy src/ --ignore-missing-imports` | Ignorar imports sin tipos |

---

## 11. Build y Producción

### Preparación para Producción

| Paso | Comando |
|------|---------|
| 1. Actualizar .env | `nano .env` (configurar variables de producción) |
| 2. Instalar dependencias | `pip install -r requirements.txt` |
| 3. Ejecutar migraciones | `alembic upgrade head` |
| 4. Crear usuario admin | `python scripts/create_admin.py` |
| 5. Verificar configuración | `python -c "from src.shared.config.settings import settings; print(settings.app_env)"` |

### Iniciar en Producción

#### Con Uvicorn

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Con Gunicorn (Recomendado)

```bash
# Instalar Gunicorn
pip install gunicorn

# Iniciar
gunicorn src.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

**Parámetros recomendados**:
- `--workers`: Número de workers (recomendado: 2 x CPU cores + 1)
- `--worker-class`: Usar UvicornWorker para async
- `--bind`: IP y puerto
- `--access-logfile`: Log de accesos
- `--error-logfile`: Log de errores

### Systemd Service (Linux)

Crear archivo `/etc/systemd/system/gxregistry.service`:

```ini
[Unit]
Description=GeneXus Object Registry
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/gx-object-registry
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

**Comandos systemd**:

| Comando | Descripción |
|---------|-------------|
| `sudo systemctl daemon-reload` | Recargar configuración |
| `sudo systemctl enable gxregistry` | Habilitar inicio automático |
| `sudo systemctl start gxregistry` | Iniciar servicio |
| `sudo systemctl stop gxregistry` | Detener servicio |
| `sudo systemctl restart gxregistry` | Reiniciar servicio |
| `sudo systemctl status gxregistry` | Ver estado del servicio |
| `sudo systemctl logs -f gxregistry` | Ver logs en tiempo real |

---

## 12. Comandos Peligrosos

> ⚠️ **ADVERTENCIA**: Los siguientes comandos pueden eliminar información existente. Ejecutar únicamente cuando sea necesario y con precaución.

### Base de Datos

| Comando | Descripción | Impacto |
|---------|-------------|---------|
| `alembic downgrade base` | Revertir todas las migraciones | Elimina todas las tablas |
| `python scripts/reset_database.py` | Resetear base de datos | Elimina toda la información |
| `python scripts/limpiar_datos.py` | Limpiar datos de tablas | Elimina registros pero mantiene estructura |
| `psql -U gxregistry -d gxregistry_db -c "DROP DATABASE gxregistry_db;"` | Eliminar base de datos | Elimina la base de datos completa |

### Docker

| Comando | Descripción | Impacto |
|---------|-------------|---------|
| `docker-compose down -v` | Detener y eliminar volúmenes | Elimina datos de PostgreSQL |
| `docker-compose down --rmi all` | Eliminar contenedores e imágenes | Elimina imágenes descargadas |
| `docker system prune -a` | Limpiar todo el sistema Docker | Elimina contenedores, redes, imágenes sin usar |

### Archivos

| Comando | Descripción | Impacto |
|---------|-------------|---------|
| `rm -rf venv/` | Eliminar entorno virtual | Requiere reinstalar dependencias |
| `rm -rf __pycache__/` | Eliminar cache de Python | Inofensivo, se regenera |
| `rm -rf alembic/versions/` | Eliminar migraciones | Pérdida de historial de BD |

---

## 13. Tabla de Referencia Rápida

### Comandos Más Usados

| Acción | Comando |
|--------|---------|
| **Iniciar desarrollo** | `uvicorn src.main:app --reload` |
| **Activar entorno virtual (Windows)** | `venv\Scripts\activate` |
| **Activar entorno virtual (Linux/macOS)** | `source venv/bin/activate` |
| **Instalar dependencias** | `pip install -r requirements.txt` |
| **Ejecutar migraciones** | `alembic upgrade head` |
| **Crear migración** | `alembic revision --autogenerate -m "Mensaje"` |
| **Ver estado de migraciones** | `alembic current` |
| **Crear usuario admin** | `python scripts/create_admin.py` |
| **Resetear contraseña** | `python scripts/reset_password.py` |
| **Ejecutar tests** | `pytest` |
| **Ejecutar tests con cobertura** | `pytest --cov=src` |
| **Formatear código** | `black src/` |
| **Verificar código (linting)** | `ruff check src/` |
| **Levantar Docker (todo)** | `docker-compose up` |
| **Levantar Docker (background)** | `docker-compose up -d` |
| **Ver logs Docker** | `docker-compose logs -f` |
| **Detener Docker** | `docker-compose down` |
| **Entrar a contenedor API** | `docker-compose exec api bash` |
| **Entrar a PostgreSQL** | `docker-compose exec postgres psql -U gxuser -d gx_object_registry` |

### Flujo de Trabajo Típico

**Inicio de proyecto (primera vez)**:
```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno virtual
venv\Scripts\activate  # Windows
# o
source venv/bin/activate  # Linux/macOS

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar .env
cp .env.example .env
# Editar .env con tus valores

# 5. Ejecutar migraciones
alembic upgrade head

# 6. Crear usuario admin
python scripts/create_admin.py

# 7. Iniciar servidor
uvicorn src.main:app --reload
```

**Desarrollo diario**:
```bash
# 1. Activar entorno virtual
venv\Scripts\activate  # Windows

# 2. Actualizar código
git pull

# 3. Actualizar dependencias (si cambiaron)
pip install -r requirements.txt

# 4. Ejecutar migraciones (si hay nuevas)
alembic upgrade head

# 5. Iniciar servidor
uvicorn src.main:app --reload

# 6. Trabajar...

# 7. Formatear código antes de commit
black src/

# 8. Verificar código
ruff check src/ --fix

# 9. Ejecutar tests
pytest

# 10. Commit y push
git add .
git commit -m "Descripción de cambios"
git push
```

**Con Docker**:
```bash
# 1. Levantar servicios
docker-compose up -d

# 2. Ejecutar migraciones
docker-compose exec api alembic upgrade head

# 3. Crear admin
docker-compose exec api python scripts/create_admin.py

# 4. Ver logs
docker-compose logs -f api

# 5. Detener servicios
docker-compose down
```

---

## Notas Importantes

### Dependencias de Comandos

Algunos comandos requieren que otros servicios estén ejecutándose:

1. **Migraciones (`alembic upgrade head`)**: Requiere PostgreSQL corriendo
2. **Scripts de utilidad**: Requieren PostgreSQL corriendo
3. **Tests de integración**: Requieren PostgreSQL corriendo
4. **Servidor FastAPI**: Requiere PostgreSQL corriendo

### Entorno Virtual

**Siempre activa el entorno virtual** antes de ejecutar comandos de Python:

```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

Sabrás que está activado cuando veas `(venv)` al inicio de tu prompt.

### Puertos

- **8000**: FastAPI (por defecto)
- **5432**: PostgreSQL (por defecto)
- **5434**: PostgreSQL (en configuración actual de .env)

Si tienes conflictos de puertos, cámbialos en:
- FastAPI: `--port 8001` en comando uvicorn
- PostgreSQL: Edita `DATABASE_URL` en `.env`

---

**Esta guía de comandos cubre todas las operaciones necesarias para instalar, desarrollar, probar y desplegar GeneXus Object Registry.**
