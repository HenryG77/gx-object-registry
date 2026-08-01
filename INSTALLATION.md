# Guía de Instalación - GeneXus Object Registry

Esta guía explica paso a paso cómo instalar, configurar y ejecutar el proyecto GeneXus Object Registry desde cero.

---

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

### Sistema Operativo
- **Windows** 10/11 o **Linux** (Ubuntu 20.04+) o **macOS** 11+

### Software Requerido

#### 1. Python
- **Versión**: Python 3.11 o superior
- **Verificar instalación**:
  ```bash
  python --version
  ```
- **Descargar**: https://www.python.org/downloads/

#### 2. PostgreSQL
- **Versión**: PostgreSQL 15 o superior
- **Verificar instalación**:
  ```bash
  psql --version
  ```
- **Descargar**: https://www.postgresql.org/download/

#### 3. Git
- **Verificar instalación**:
  ```bash
  git --version
  ```
- **Descargar**: https://git-scm.com/downloads

#### 4. Gestor de Paquetes Python
- **pip** viene incluido con Python 3.11+
- **Verificar instalación**:
  ```bash
  pip --version
  ```

### Opcional (pero recomendado)

#### Docker y Docker Compose
- **Docker Desktop** para ejecutar el proyecto en contenedores
- **Verificar instalación**:
  ```bash
  docker --version
  docker-compose --version
  ```
- **Descargar**: https://www.docker.com/products/docker-desktop/

---

## 1. Clonar o Descargar el Repositorio

### Opción A: Clonar con Git
```bash
git clone <URL_DEL_REPOSITORIO>
cd gx-object-registry
```

### Opción B: Descargar ZIP
1. Descargar el archivo ZIP del repositorio
2. Extraer el contenido
3. Abrir terminal en la carpeta extraída

---

## 2. Instalación de Dependencias

### Crear Entorno Virtual (Recomendado)

Un entorno virtual aísla las dependencias del proyecto del sistema.

#### En Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### En Linux/macOS:
```bash
python -m venv venv
source venv/bin/activate
```

Deberías ver `(venv)` al inicio de tu línea de comando.

### Instalar Dependencias del Proyecto

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Este comando instalará todas las dependencias necesarias:
- FastAPI 0.109.0+ (framework web)
- Uvicorn 0.27.0+ (servidor ASGI)
- SQLAlchemy 2.0.25+ (ORM para base de datos)
- asyncpg 0.29.0+ (driver PostgreSQL async)
- Alembic 1.13.1+ (migraciones de BD)
- Pydantic 2.5.3+ (validación de datos)
- python-jose 3.3.0+ (manejo de JWT)
- bcrypt 4.0.0+ (hash de contraseñas)
- structlog 24.1.0+ (logging estructurado)
- Y más (ver `requirements.txt` completo)

**Tiempo estimado**: 2-5 minutos dependiendo de tu conexión.

---

## 3. Configuración de Variables de Entorno

### Crear archivo .env

El proyecto utiliza un archivo `.env` para almacenar la configuración.

#### Opción A: Copiar desde .env.example (si existe)
```bash
cp .env.example .env
```

#### Opción B: Crear manualmente
Crea un archivo llamado `.env` en la raíz del proyecto con el siguiente contenido:

```env
# DATABASE - Configuración de PostgreSQL
DATABASE_URL=postgresql+asyncpg://gxregistry:gxregistry123@localhost:5432/gxregistry_db
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# APPLICATION - Configuración de la aplicación
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO

# API - Configuración del API REST
API_PREFIX=/api
API_VERSION=v1
API_TITLE=GeneXus Object Registry
API_DESCRIPTION=API para administrar objetos de GeneXus

# CORS - Orígenes permitidos para acceso desde frontend
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# IMPORT - Configuración de importación CSV
MAX_FILE_SIZE_MB=50
MAX_ERRORS_TO_REPORT=100
CSV_BATCH_SIZE=500

# SECURITY - Clave secreta para firmar tokens JWT
SECRET_KEY=CAMBIA_ESTO_EN_PRODUCCION_POR_ALGO_MUY_SEGURO
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT - Configuración de autenticación
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=365
```

### Descripción de Variables Importantes

#### Obligatorias

**DATABASE_URL**
- **Descripción**: Cadena de conexión a PostgreSQL en formato asyncpg
- **Formato**: `postgresql+asyncpg://usuario:contraseña@host:puerto/nombre_bd`
- **Ejemplo**: `postgresql+asyncpg://gxregistry:gxregistry123@localhost:5432/gxregistry_db`

**SECRET_KEY**
- **Descripción**: Clave para firmar tokens JWT (autenticación)
- **Producción**: Debe ser una cadena aleatoria y segura de al menos 32 caracteres
- **Generar**:
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```

#### Opcionales (tienen valores por defecto)

- **APP_ENV**: Entorno (`development`, `staging`, `production`)
- **DEBUG**: Habilitar modo debug (`true` o `false`)
- **LOG_LEVEL**: Nivel de logging (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`)
- **DATABASE_POOL_SIZE**: Tamaño del pool de conexiones (default: 20)
- **DATABASE_MAX_OVERFLOW**: Conexiones adicionales permitidas (default: 10)
- **MAX_FILE_SIZE_MB**: Tamaño máximo de archivos CSV (default: 50)
- **CORS_ORIGINS**: Orígenes permitidos para CORS

> ⚠️ **IMPORTANTE**: Nunca compartas el archivo `.env` ni subas valores reales de `SECRET_KEY` a repositorios públicos.

---

## 4. Configuración de la Base de Datos

### Opción A: PostgreSQL Local

#### Paso 1: Crear la Base de Datos

Accede a PostgreSQL:

```bash
# En Windows
psql -U postgres

# En Linux/macOS
sudo -u postgres psql
```

Ejecuta los siguientes comandos SQL:

```sql
-- Crear usuario
CREATE USER gxregistry WITH PASSWORD 'gxregistry123';

-- Crear base de datos
CREATE DATABASE gxregistry_db OWNER gxregistry;

-- Otorgar privilegios
GRANT ALL PRIVILEGES ON DATABASE gxregistry_db TO gxregistry;

-- Salir
\q
```

#### Paso 2: Verificar Conexión

```bash
psql -U gxregistry -d gxregistry_db -h localhost
```

Si puedes conectarte, la configuración es correcta.

#### Paso 3: Ejecutar Migraciones

Las migraciones crean las tablas necesarias en la base de datos.

```bash
alembic upgrade head
```

Deberías ver:

```
INFO  [alembic.runtime.migration] Running upgrade -> 001, create_object_types_and_genexus_objects
INFO  [alembic.runtime.migration] Running upgrade 001 -> 55adc69b9133, add_auth_system_and_created_by_fields
INFO  [alembic.runtime.migration] Running upgrade 55adc69b9133 -> <next>, add_last_login_to_users
INFO  [alembic.runtime.migration] Running upgrade <next> -> <next>, add_must_change_password
```

#### Paso 4: Cargar Datos Iniciales (Opcional)

Ejecuta el script de seeders para crear tipos de objetos predefinidos:

```bash
python scripts/seed_database.py
```

#### Paso 5: Crear Usuario Administrador

```bash
python scripts/create_admin.py
```

El script te pedirá:
- **Username**: `admin`
- **Email**: `admin@example.com`
- **Full Name**: `Administrador`
- **Password**: `admin123` (o la que prefieras)

---

### Opción B: PostgreSQL con Docker

Si tienes Docker instalado, puedes levantar PostgreSQL fácilmente:

#### Paso 1: Levantar PostgreSQL con Docker Compose

```bash
docker-compose up -d postgres
```

Esto crea:
- Contenedor PostgreSQL 15
- Usuario: `gxuser`
- Contraseña: `gxpassword`
- Base de datos: `gx_object_registry`
- Puerto: 5432

#### Paso 2: Actualizar .env

```env
DATABASE_URL=postgresql+asyncpg://gxuser:gxpassword@localhost:5432/gx_object_registry
```

#### Paso 3: Ejecutar Migraciones

```bash
alembic upgrade head
```

#### Paso 4: Crear Usuario Administrador

```bash
python scripts/create_admin.py
```

---

## 5. Ejecución en Entorno de Desarrollo

Una vez completada la configuración, puedes iniciar el servidor de desarrollo.

### Iniciar el Servidor

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Parámetros**:
- `--reload`: Reinicia automáticamente al detectar cambios en el código
- `--host 0.0.0.0`: Permite acceso desde cualquier IP (útil para desarrollo)
- `--port 8000`: Puerto en el que escucha la aplicación

**Salida esperada**:

```
INFO:     Will watch for changes in these directories: ['c:\\...\\gx-object-registry']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [67890]
INFO:     Waiting for application startup.
[2026-08-01 10:00:00.000] Starting application app_env=development debug=True
INFO:     Application startup complete.
```

### Acceder a la Aplicación

Abre tu navegador y accede a:

- **Interfaz Web**: http://localhost:8000/web
- **Login**: http://localhost:8000/web/login
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Iniciar Sesión

Usa las credenciales del usuario administrador que creaste:
- **Usuario**: `admin`
- **Contraseña**: `admin123` (o la que configuraste)

---

## 6. Ejecución con Docker (Completa)

Si prefieres ejecutar toda la aplicación en contenedores:

### Levantar Todo el Stack

```bash
docker-compose up
```

Esto levanta:
1. **PostgreSQL** (puerto 5432)
2. **API FastAPI** (puerto 8000)

### Ejecutar Migraciones dentro del Contenedor

```bash
docker-compose exec api alembic upgrade head
```

### Crear Usuario Administrador

```bash
docker-compose exec api python scripts/create_admin.py
```

### Acceder a la Aplicación

- **Web**: http://localhost:8000/web
- **API**: http://localhost:8000/docs

### Detener los Contenedores

```bash
docker-compose down
```

---

## 7. Ejecución en Producción

### Preparación

#### 1. Configurar Variables de Entorno

Actualiza `.env` con valores de producción:

```env
APP_ENV=production
DEBUG=false
LOG_LEVEL=WARNING
SECRET_KEY=<GENERA_UNA_CLAVE_SEGURA_AQUI>
DATABASE_URL=postgresql+asyncpg://<usuario>:<password>@<host>:<puerto>/<database>
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
CORS_ORIGINS=https://tudominio.com
```

#### 2. Instalar Solo Dependencias de Producción

Si tienes un `requirements-prod.txt` separado, úsalo. Si no, instala todo:

```bash
pip install -r requirements.txt
```

#### 3. Ejecutar Migraciones

```bash
alembic upgrade head
```

#### 4. Crear Usuario Administrador

```bash
python scripts/create_admin.py
```

### Iniciar con Uvicorn

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Parámetros de Producción**:
- `--workers 4`: Número de procesos worker (ajustar según CPU)
- Sin `--reload`: No reinicia automáticamente
- `--host 0.0.0.0`: Escucha en todas las interfaces

### Usar Gunicorn (Recomendado)

```bash
pip install gunicorn
gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Usar Supervisor o Systemd

Para mantener el proceso corriendo en segundo plano, usa un gestor de procesos como **Supervisor** o **systemd**.

#### Ejemplo systemd (`/etc/systemd/system/gxregistry.service`):

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

```bash
sudo systemctl daemon-reload
sudo systemctl enable gxregistry
sudo systemctl start gxregistry
sudo systemctl status gxregistry
```

### Configurar Nginx como Reverse Proxy

Instala Nginx:

```bash
sudo apt install nginx
```

Configura un sitio (`/etc/nginx/sites-available/gxregistry`):

```nginx
server {
    listen 80;
    server_name tudominio.com www.tudominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Habilita el sitio:

```bash
sudo ln -s /etc/nginx/sites-available/gxregistry /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### HTTPS con Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tudominio.com -d www.tudominio.com
```

---

## 8. Estructura Inicial del Proyecto

Después de la instalación, tu proyecto debería verse así:

```
gx-object-registry/
├── .env                    # ✅ Configuración (creado por ti)
├── venv/                   # ✅ Entorno virtual (creado)
├── alembic/
│   └── versions/           # ✅ Migraciones aplicadas
├── src/
│   ├── main.py             # Punto de entrada
│   ├── auth/               # Módulo de autenticación
│   ├── object_types/       # Tipos de objetos
│   ├── genexus_objects/    # Objetos GeneXus
│   ├── imports/            # Importación CSV
│   ├── web/                # Interfaz web
│   └── shared/             # Código compartido
├── scripts/                # Scripts de utilidad
├── requirements.txt        # Dependencias
└── docker-compose.yml      # Configuración Docker
```

---

## 9. Solución de Problemas

### Error: "No module named 'fastapi'"

**Causa**: Dependencias no instaladas.

**Solución**:
```bash
pip install -r requirements.txt
```

---

### Error: "could not connect to server: Connection refused"

**Causa**: PostgreSQL no está ejecutándose o la configuración de conexión es incorrecta.

**Solución**:

1. Verifica que PostgreSQL esté corriendo:
   ```bash
   # Linux/macOS
   sudo systemctl status postgresql

   # Windows
   # Busca "Services" y verifica que PostgreSQL esté iniciado
   ```

2. Verifica que `DATABASE_URL` en `.env` sea correcto.

3. Prueba la conexión manualmente:
   ```bash
   psql -U gxregistry -d gxregistry_db -h localhost
   ```

---

### Error: "alembic: command not found"

**Causa**: Alembic no está instalado o el entorno virtual no está activado.

**Solución**:

1. Activa el entorno virtual:
   ```bash
   # Windows
   venv\Scripts\activate

   # Linux/macOS
   source venv/bin/activate
   ```

2. Instala Alembic:
   ```bash
   pip install alembic
   ```

---

### Error: "relation 'users' does not exist"

**Causa**: Las migraciones no se han ejecutado.

**Solución**:
```bash
alembic upgrade head
```

---

### Error: "Port 8000 is already in use"

**Causa**: Otro proceso está usando el puerto 8000.

**Solución**:

1. Detén el proceso que está usando el puerto.

2. O usa otro puerto:
   ```bash
   uvicorn src.main:app --reload --port 8001
   ```

---

### Error: "Invalid signature" al hacer login

**Causa**: La `SECRET_KEY` cambió después de generar el token.

**Solución**:

1. Limpia las cookies del navegador.

2. O genera una nueva `SECRET_KEY` y vuelve a hacer login.

---

### Problemas con permisos en Linux

**Causa**: El usuario no tiene permisos para acceder a la base de datos o archivos.

**Solución**:

1. Asegúrate de que el usuario de PostgreSQL tenga los permisos correctos:
   ```sql
   GRANT ALL PRIVILEGES ON DATABASE gxregistry_db TO gxregistry;
   GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO gxregistry;
   ```

2. Asegúrate de tener permisos de escritura en el directorio del proyecto.

---

### Error al importar CSV: "Invalid header"

**Causa**: El formato del CSV no es el esperado.

**Solución**:

1. Asegúrate de que el CSV tenga el delimitador correcto (`;`).

2. Verifica que los headers sean exactamente: `name;description;objectType`

3. Ejemplo correcto:
   ```csv
   name;description;objectType
   AhrPr001;Recupera Tasa Interés;PROCEDURE
   ```

---

## 10. Verificar Instalación Exitosa

Después de completar todos los pasos, verifica que todo funcione:

### 1. Servidor Ejecutándose
```bash
curl http://localhost:8000/health
```

**Respuesta esperada**:
```json
{"status": "healthy"}
```

### 2. API Docs Accesibles

Abre en el navegador: http://localhost:8000/docs

Deberías ver la documentación interactiva de Swagger UI.

### 3. Login Funcional

1. Accede a: http://localhost:8000/web/login
2. Ingresa credenciales del admin
3. Deberías ser redirigido al dashboard

### 4. Base de Datos Conectada

Ejecuta:
```bash
python -c "from src.shared.database.connection import get_engine; import asyncio; asyncio.run(get_engine().dispose())"
```

Si no hay errores, la conexión es exitosa.

---

## Próximos Pasos

Una vez completada la instalación:

1. **Explora la interfaz web**: http://localhost:8000/web
2. **Crea tipos de objetos**: Desde el módulo de tipos
3. **Importa objetos desde CSV**: Usa el módulo de importación
4. **Lee la documentación técnica**: Consulta `TECHNOLOGIES.md` y `SYSTEM.md`
5. **Revisa comandos disponibles**: Consulta `COMMANDS.md`

---

## Soporte

Si encuentras problemas no cubiertos en esta guía:

1. Revisa los logs del servidor para mensajes de error detallados
2. Verifica que todas las dependencias estén instaladas correctamente
3. Asegúrate de que PostgreSQL esté ejecutándose
4. Consulta la documentación de FastAPI: https://fastapi.tiangolo.com/
5. Consulta la documentación de Alembic: https://alembic.sqlalchemy.org/

---

**¡Instalación completada! El sistema está listo para usar.**
