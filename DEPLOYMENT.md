# Guía de Despliegue en Producción - GeneXus Object Registry

> **Versión:** 1.0
> **Última actualización:** 2026-08-03
> **Autor:** Documentación Técnica

Esta guía proporciona instrucciones paso a paso para instalar, configurar y desplegar la aplicación **GeneXus Object Registry** en un entorno de producción.

---

## Tabla de Contenidos

1. [Requisitos Previos](#1-requisitos-previos)
2. [Preparación del Servidor](#2-preparación-del-servidor)
3. [Instalación de PostgreSQL](#3-instalación-de-postgresql)
4. [Transferencia del Proyecto](#4-transferencia-del-proyecto)
5. [Configuración del Entorno Virtual Python](#5-configuración-del-entorno-virtual-python)
6. [Configuración de Variables de Entorno](#6-configuración-de-variables-de-entorno)
7. [Configuración de la Base de Datos](#7-configuración-de-la-base-de-datos)
8. [Migraciones y Datos Iniciales](#8-migraciones-y-datos-iniciales)
9. [Configuración del Servicio Systemd](#9-configuración-del-servicio-systemd)
10. [Instalación y Configuración de Nginx](#10-instalación-y-configuración-de-nginx)
11. [Configuración del Firewall UFW](#11-configuración-del-firewall-ufw)
12. [Configuración de Backups Automáticos](#12-configuración-de-backups-automáticos)
13. [Configuración de HTTPS con Let's Encrypt](#13-configuración-de-https-con-lets-encrypt)
14. [Verificación Final](#14-verificación-final)
15. [Monitoreo y Logs](#15-monitoreo-y-logs)
16. [Solución de Problemas](#16-solución-de-problemas)
17. [Actualización de la Aplicación](#17-actualización-de-la-aplicación)
18. [Checklist de Despliegue](#18-checklist-de-despliegue)

---

## 1. Requisitos Previos

### 1.1 Sistema Operativo

- **Recomendado:** Ubuntu Server 22.04 LTS o superior
- **Alternativas compatibles:** Debian 11+, CentOS 8+, Rocky Linux 8+

### 1.2 Requisitos de Hardware

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| CPU | 2 cores | 4 cores |
| RAM | 2 GB | 4 GB |
| Disco | 20 GB | 50 GB (SSD preferible) |
| Red | 100 Mbps | 1 Gbps |

### 1.3 Software Requerido

| Software | Versión | Propósito |
|----------|---------|-----------|
| Python | 3.10+ | Runtime de la aplicación |
| PostgreSQL | 15+ | Base de datos |
| Nginx | 1.18+ | Reverse proxy |
| Git | 2.x+ | Control de versiones |
| pip | 23.x+ | Gestor de paquetes Python |
| virtualenv | 20.x+ | Entornos virtuales Python |

### 1.4 Puertos Requeridos

| Puerto | Protocolo | Uso |
|--------|-----------|-----|
| 22 | TCP | SSH (administración) |
| 80 | TCP | HTTP (redirige a HTTPS) |
| 443 | TCP | HTTPS (aplicación web) |
| 5432 | TCP | PostgreSQL (solo localhost) |
| 8000 | TCP | Uvicorn (solo localhost) |

### 1.5 Accesos Necesarios

- Acceso root o sudo al servidor
- Dominio o subdominio apuntando al servidor (para HTTPS)
- Cliente SSH (PuTTY, OpenSSH, etc.)

---

## 2. Preparación del Servidor

### 2.1 Actualizar el Sistema

**Dónde ejecutar:** Servidor de producción
**Usuario:** root o con sudo
**Directorio:** Cualquiera

```bash
sudo apt update
sudo apt upgrade -y
```

**Qué hace:** Actualiza la lista de paquetes disponibles e instala las actualizaciones de seguridad y bugfixes.

**Resultado esperado:** El sistema muestra una lista de paquetes actualizados sin errores.

### 2.2 Instalar Herramientas Básicas

```bash
sudo apt install -y \
    build-essential \
    git \
    curl \
    wget \
    vim \
    htop \
    net-tools \
    software-properties-common \
    ca-certificates \
    apt-transport-https \
    gnupg \
    lsb-release
```

**Qué hace:** Instala herramientas de compilación, editores de texto, utilidades de red y certificados necesarios.

### 2.3 Configurar Zona Horaria

```bash
sudo timedatectl set-timezone UTC
timedatectl
```

**Qué hace:** Configura la zona horaria del servidor a UTC (recomendado para producción).

**Resultado esperado:**
```
Time zone: UTC (UTC, +0000)
```

⚠️ **Nota:** Puedes usar otra zona horaria si lo prefieres, por ejemplo `America/Asuncion` para Paraguay.

### 2.4 Crear Usuario de Aplicación

**Por qué:** Nunca ejecutar aplicaciones web como root por seguridad.

```bash
sudo adduser gxapp
```

**Qué hace:** Crea un usuario dedicado para ejecutar la aplicación.

**Interacción esperada:** Te pedirá una contraseña y datos opcionales (nombre completo, etc.). Puedes dejar los datos opcionales en blanco presionando Enter.

### 2.5 Agregar Usuario al Grupo sudo (opcional)

```bash
sudo usermod -aG sudo gxapp
```

**Qué hace:** Permite al usuario `gxapp` ejecutar comandos con sudo.

**Nota:** Solo hazlo si necesitas que este usuario administre el servidor. Para mayor seguridad, puedes omitir este paso.

### 2.6 Configurar SSH de Forma Segura

#### 2.6.1 Deshabilitar Login Root (Recomendado)

Edita el archivo de configuración SSH:

```bash
sudo vim /etc/ssh/sshd_config
```

Busca y modifica estas líneas:

```
PermitRootLogin no
PasswordAuthentication yes  # Cambia a 'no' cuando configures SSH keys
```

Reinicia el servicio SSH:

```bash
sudo systemctl restart sshd
```

⚠️ **Advertencia:** Asegúrate de tener otra forma de acceso antes de deshabilitar PasswordAuthentication.

### 2.7 Instalar Python 3.10 y pip

En Ubuntu 22.04, Python 3.10 ya viene instalado. Verifica:

```bash
python3 --version
```

**Resultado esperado:**
```
Python 3.10.12
```

Instala pip y venv:

```bash
sudo apt install -y python3-pip python3-venv python3-dev
```

**Qué hace:** Instala el gestor de paquetes pip, soporte para entornos virtuales y headers de desarrollo de Python.

### 2.8 Instalar Dependencias del Sistema para PostgreSQL

```bash
sudo apt install -y \
    libpq-dev \
    postgresql-client
```

**Qué hace:** Instala bibliotecas necesarias para que Python pueda conectarse a PostgreSQL (psycopg2, asyncpg).

---

## 3. Instalación de PostgreSQL

### 3.1 Escenario A: PostgreSQL NO está instalado

#### 3.1.1 Agregar Repositorio Oficial de PostgreSQL

```bash
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt update
```

**Qué hace:** Agrega el repositorio oficial de PostgreSQL para obtener la versión más reciente (15+).

#### 3.1.2 Instalar PostgreSQL 15

```bash
sudo apt install -y postgresql-15 postgresql-contrib-15
```

**Qué hace:** Instala PostgreSQL 15 y extensiones adicionales.

**Resultado esperado:** PostgreSQL se instala y el servicio inicia automáticamente.

#### 3.1.3 Verificar Instalación

```bash
sudo systemctl status postgresql
```

**Resultado esperado:**
```
● postgresql.service - PostgreSQL RDBMS
     Loaded: loaded (...)
     Active: active (running)
```

#### 3.1.4 Habilitar Inicio Automático

```bash
sudo systemctl enable postgresql
```

**Qué hace:** Configura PostgreSQL para iniciar automáticamente al reiniciar el servidor.

### 3.2 Escenario B: PostgreSQL YA está instalado

#### 3.2.1 Verificar Instalación

```bash
psql --version
sudo systemctl status postgresql
```

**Resultado esperado:**
```
psql (PostgreSQL) 15.x
Active: active (running)
```

#### 3.2.2 Verificar Versión

Si la versión es menor a 15, considera actualizar:

```bash
# Ver versiones instaladas
dpkg -l | grep postgresql

# Si necesitas actualizar, sigue la documentación oficial de PostgreSQL
```

### 3.3 Crear Base de Datos y Usuario

#### 3.3.1 Conectarse como Usuario postgres

```bash
sudo -u postgres psql
```

**Dónde ejecutar:** Servidor
**Usuario:** postgres (superusuario de PostgreSQL)
**Qué hace:** Abre la consola interactiva de PostgreSQL como administrador.

#### 3.3.2 Crear Usuario de Base de Datos

Dentro de la consola `psql`:

```sql
CREATE USER gxapp_user WITH PASSWORD 'CONTRASEÑA_SEGURA_AQUI';
```

**⚠️ IMPORTANTE:**
- Reemplaza `CONTRASEÑA_SEGURA_AQUI` con una contraseña fuerte
- Guarda esta contraseña en un lugar seguro
- Usa al menos 16 caracteres con letras, números y símbolos

**Ejemplo de contraseña segura:** `7k$mP9#xL2qR5wN8@vT3`

#### 3.3.3 Crear Base de Datos

```sql
CREATE DATABASE gx_object_registry OWNER gxapp_user;
```

**Qué hace:** Crea la base de datos y asigna al usuario `gxapp_user` como propietario.

#### 3.3.4 Asignar Permisos

```sql
GRANT ALL PRIVILEGES ON DATABASE gx_object_registry TO gxapp_user;

-- Conectarse a la base de datos
\c gx_object_registry

-- Otorgar permisos en el esquema public
GRANT ALL PRIVILEGES ON SCHEMA public TO gxapp_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO gxapp_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO gxapp_user;
```

**Qué hace:** Asegura que el usuario tenga todos los permisos necesarios para crear/modificar tablas y secuencias.

#### 3.3.5 Verificar y Salir

```sql
-- Listar bases de datos
\l

-- Listar usuarios
\du

-- Salir
\q
```

#### 3.3.6 Probar Conexión

```bash
PGPASSWORD='TU_CONTRASEÑA' psql -h localhost -U gxapp_user -d gx_object_registry -c "SELECT version();"
```

**Resultado esperado:** Muestra la versión de PostgreSQL sin errores de autenticación.

### 3.4 Configuración de PostgreSQL Remoto (Opcional)

Si utilizas PostgreSQL en otro servidor o servicio cloud:

#### 3.4.1 Obtener Datos de Conexión

Necesitarás:
- **Host:** IP o dominio del servidor PostgreSQL
- **Puerto:** Generalmente 5432
- **Usuario:** Usuario de base de datos
- **Contraseña:** Contraseña del usuario
- **Nombre de BD:** Nombre de la base de datos

#### 3.4.2 Configurar DATABASE_URL

El formato será:

```
postgresql+asyncpg://USUARIO:CONTRASEÑA@HOST:PUERTO/NOMBRE_BD
```

Ejemplo:

```
postgresql+asyncpg://gxapp_user:mi_password@db.ejemplo.com:5432/gx_object_registry
```

#### 3.4.3 Configurar Firewall

Si PostgreSQL está en otro servidor, asegúrate de:

- Abrir el puerto 5432 en el firewall del servidor PostgreSQL
- Configurar `pg_hba.conf` para permitir conexiones desde la IP del servidor de aplicación
- **NO exponer PostgreSQL públicamente a Internet**

**Configuración segura en `pg_hba.conf`:**

```
# Permitir solo desde la IP del servidor de aplicación
host    gx_object_registry    gxapp_user    IP_SERVIDOR_APP/32    md5
```

---

## 4. Transferencia del Proyecto

### 4.1 Opción A: Clonar desde Git (Recomendado)

#### 4.1.1 Cambiar al Usuario de Aplicación

```bash
su - gxapp
```

#### 4.1.2 Crear Directorio de Aplicaciones

```bash
mkdir -p ~/apps
cd ~/apps
```

#### 4.1.3 Clonar el Repositorio

```bash
git clone https://github.com/TU_USUARIO/gx-object-registry.git
cd gx-object-registry
```

**Qué hace:** Descarga el código fuente del repositorio Git.

**Nota:** Reemplaza la URL con la de tu repositorio real.

#### 4.1.4 Seleccionar Rama de Producción

```bash
git checkout main  # o la rama que uses para producción
```

### 4.2 Opción B: Transferir Manualmente vía SCP

Si no usas Git, puedes transferir el código desde tu máquina local:

#### 4.2.1 En tu Máquina Local (Windows)

Comprimir el proyecto (excluyendo archivos innecesarios):

**PowerShell:**

```powershell
# Navegar al proyecto
cd C:\Users\operador\Proyectos\web\gx-object-registry

# Crear archivo ZIP (excluir venv, __pycache__, node_modules, etc.)
Compress-Archive -Path .\* -DestinationPath gx-registry.zip -Force
```

**Transferir al servidor:**

```powershell
scp -P 22 gx-registry.zip gxapp@TU_SERVIDOR_IP:~/
```

#### 4.2.2 En el Servidor

```bash
su - gxapp
mkdir -p ~/apps
cd ~/apps
unzip ~/gx-registry.zip -d gx-object-registry
cd gx-object-registry
```

**Qué hace:** Descomprime el proyecto en el directorio de aplicaciones.

### 4.3 Verificar Estructura del Proyecto

```bash
pwd
ls -la
```

**Resultado esperado:**

```
/home/gxapp/apps/gx-object-registry
```

Deberías ver directorios como:
- `src/`
- `alembic/`
- `scripts/`
- `requirements.txt`
- `.env.example`
- `README.md`

---

## 5. Configuración del Entorno Virtual Python

### 5.1 Crear Entorno Virtual

**Dónde ejecutar:** Servidor
**Usuario:** gxapp
**Directorio:** `/home/gxapp/apps/gx-object-registry`

```bash
cd /home/gxapp/apps/gx-object-registry
python3 -m venv venv
```

**Qué hace:** Crea un entorno virtual Python aislado en el directorio `venv/`.

**Resultado esperado:** Se crea el directorio `venv/` con Python y pip aislados.

### 5.2 Activar Entorno Virtual

```bash
source venv/bin/activate
```

**Qué hace:** Activa el entorno virtual. El prompt cambiará a `(venv) gxapp@servidor:~$`.

**Resultado esperado:** El prompt ahora muestra `(venv)` al inicio.

### 5.3 Actualizar pip

```bash
pip install --upgrade pip
```

**Qué hace:** Actualiza pip a la última versión dentro del entorno virtual.

### 5.4 Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Qué hace:** Instala todas las dependencias de Python listadas en `requirements.txt`.

**Resultado esperado:** Instalación exitosa de paquetes como:
- fastapi
- uvicorn
- sqlalchemy
- alembic
- asyncpg
- psycopg2-binary
- python-jose
- passlib
- bcrypt
- python-multipart
- python-dotenv
- structlog
- jinja2

**Tiempo estimado:** 2-5 minutos dependiendo de la conexión.

### 5.5 Verificar Dependencias Críticas

Asegúrate de que `jinja2` esté instalado (necesario para templates):

```bash
pip list | grep jinja2
```

**Resultado esperado:**
```
jinja2        3.1.6
```

Si no está instalado:

```bash
pip install jinja2
```

---

## 6. Configuración de Variables de Entorno

### 6.1 Copiar Archivo de Ejemplo

```bash
cp .env.example .env
```

**Qué hace:** Crea una copia del archivo de ejemplo para configurarlo.

### 6.2 Editar Archivo .env

```bash
vim .env
# o
nano .env
```

### 6.3 Variables de Entorno Requeridas

Configura las siguientes variables en el archivo `.env`:

#### 6.3.1 Configuración General

```ini
# Entorno de ejecución
APP_ENV=production
DEBUG=false
```

**Explicación:**
- `APP_ENV`: Define el entorno (`development`, `production`)
- `DEBUG`: NUNCA usar `true` en producción (expone información sensible)

#### 6.3.2 Configuración de Base de Datos

```ini
DATABASE_URL=postgresql+asyncpg://gxapp_user:TU_CONTRASEÑA@localhost/gx_object_registry
```

**Formato:**
```
postgresql+asyncpg://USUARIO:CONTRASEÑA@HOST:PUERTO/NOMBRE_BD
```

**Ejemplo con PostgreSQL remoto:**
```ini
DATABASE_URL=postgresql+asyncpg://gxapp_user:mi_password@192.168.1.100:5432/gx_object_registry
```

**⚠️ IMPORTANTE:**
- Reemplaza `TU_CONTRASEÑA` con la contraseña real que creaste
- NO subas este archivo a Git
- NO compartas esta contraseña

#### 6.3.3 Clave Secreta (SECRET_KEY)

```ini
SECRET_KEY=GENERA_UNA_CLAVE_ALEATORIA_AQUI
```

**Cómo generar una SECRET_KEY segura:**

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Resultado (ejemplo):**
```
7xG9mK3pL_8nQ2vR5wT0yU4aB1cD6eF
```

Copia ese valor y úsalo como SECRET_KEY.

**⚠️ CRÍTICO:**
- Esta clave firma los tokens JWT
- Si la cambias, todos los usuarios deberán volver a iniciar sesión
- NUNCA la compartas ni la subas a Git
- Usa al menos 32 caracteres

#### 6.3.4 Configuración de CORS y Hosts

```ini
# Dominios permitidos para CORS (separados por comas)
CORS_ORIGINS=https://tudominio.com,https://www.tudominio.com

# Hosts permitidos
ALLOWED_HOSTS=tudominio.com,www.tudominio.com,localhost
```

**Explicación:**
- `CORS_ORIGINS`: Dominios desde los cuales se permiten peticiones desde el navegador
- `ALLOWED_HOSTS`: Lista de hosts que pueden acceder a la aplicación

**Para desarrollo/pruebas locales:**
```ini
CORS_ORIGINS=http://localhost:8000,http://localhost:9000
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Para producción con dominio:**
```ini
CORS_ORIGINS=https://gxregistry.ejemplo.com
ALLOWED_HOSTS=gxregistry.ejemplo.com
```

#### 6.3.5 Configuración de Tokens

```ini
# Días de expiración del token JWT (365 = 1 año)
ACCESS_TOKEN_EXPIRE_DAYS=365
```

**Nota:** Puedes reducir este valor si necesitas mayor seguridad (por ejemplo, 30 días).

### 6.4 Archivo .env Completo de Ejemplo

```ini
# Configuración del entorno
APP_ENV=production
DEBUG=false

# Base de datos PostgreSQL
DATABASE_URL=postgresql+asyncpg://gxapp_user:7k$mP9#xL2qR5wN8@vT3@localhost/gx_object_registry

# Seguridad
SECRET_KEY=7xG9mK3pL_8nQ2vR5wT0yU4aB1cD6eF9hJ8kL3mN0pQ5rS
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=365

# CORS y Hosts
CORS_ORIGINS=https://gxregistry.ejemplo.com
ALLOWED_HOSTS=gxregistry.ejemplo.com,localhost

# Servidor
HOST=0.0.0.0
PORT=8000
```

### 6.5 Asegurar el Archivo .env

**IMPORTANTE:** Protege el archivo `.env` para que solo el usuario de la aplicación pueda leerlo:

```bash
chmod 600 .env
chown gxapp:gxapp .env
```

**Qué hace:**
- `chmod 600`: Solo el propietario puede leer/escribir el archivo
- `chown`: Asegura que el propietario sea el usuario de la aplicación

### 6.6 Verificar Configuración

```bash
cat .env
```

Asegúrate de que:
- ✅ No hay espacios antes/después del `=`
- ✅ No hay comillas innecesarias
- ✅ DATABASE_URL está correctamente formado
- ✅ SECRET_KEY es aleatorio y largo
- ✅ APP_ENV es `production`
- ✅ DEBUG es `false`

---

## 7. Configuración de la Base de Datos

### 7.1 Verificar Conexión a PostgreSQL

**Dónde ejecutar:** Servidor
**Usuario:** gxapp
**Directorio:** `/home/gxapp/apps/gx-object-registry`

```bash
# Con el entorno virtual activado
cd /home/gxapp/apps/gx-object-registry
source venv/bin/activate

# Probar conexión Python
python3 -c "
from src.shared.config.settings import settings
print('DATABASE_URL:', settings.database_url.split('@')[-1])
"
```

**Resultado esperado:** Muestra la parte pública de la DATABASE_URL (sin la contraseña).

### 7.2 Probar Conexión con psql

```bash
PGPASSWORD='TU_CONTRASEÑA' psql -h localhost -U gxapp_user -d gx_object_registry -c "\dt"
```

**Resultado esperado:**
```
Did not find any relations.
```

O si ya hay tablas:
```
List of relations
 Schema |      Name       | Type  |   Owner
--------+-----------------+-------+------------
 public | users           | table | gxapp_user
 ...
```

---

## 8. Migraciones y Datos Iniciales

### 8.1 Verificar Alembic

```bash
alembic --version
```

**Resultado esperado:**
```
alembic 1.x.x
```

Si no está instalado:

```bash
pip install alembic
```

### 8.2 Opción A: Ejecutar Migraciones con Alembic

#### 8.2.1 Verificar Estado de Migraciones

```bash
alembic current
```

**Qué hace:** Muestra la versión actual de la base de datos.

**Resultado esperado (base de datos nueva):**
```
(vacio o None)
```

#### 8.2.2 Ejecutar Migraciones

```bash
alembic upgrade head
```

**Qué hace:** Ejecuta todas las migraciones pendientes para crear/actualizar las tablas.

**Resultado esperado:**
```
INFO  [alembic.runtime.migration] Running upgrade -> b2c3d4e5f6g7, initial migration
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
```

#### 8.2.3 Verificar Tablas Creadas

```bash
PGPASSWORD='TU_CONTRASEÑA' psql -h localhost -U gxapp_user -d gx_object_registry -c "\dt"
```

**Resultado esperado:**
```
List of relations
 Schema |      Name       | Type  |   Owner
--------+-----------------+-------+------------
 public | users           | table | gxapp_user
 public | object_types    | table | gxapp_user
 public | genexus_objects | table | gxapp_user
 public | alembic_version | table | gxapp_user
```

### 8.3 Opción B: Crear Tablas Manualmente (Si Alembic falla)

Si Alembic da error con ENUM types, usa este método alternativo:

#### 8.3.1 Crear Script de Creación de Tablas

```bash
cat > create_tables.py << 'EOF'
import asyncio
from src.shared.database.base import Base
from src.shared.database.connection import engine
from src.shared.config.settings import settings

# Importar modelos para registrarlos
from src.auth.infrastructure.models import UserModel
from src.object_types.infrastructure.models import ObjectTypeModel
from src.genexus_objects.infrastructure.models import GeneXusObjectModel

async def create_tables():
    async with engine.begin() as conn:
        print(f'Creando tablas en: {settings.database_url.split("@")[-1]}')
        print(f'Número de tablas a crear: {len(Base.metadata.tables)}')
        await conn.run_sync(Base.metadata.create_all)
    print('¡Tablas creadas exitosamente!')

if __name__ == '__main__':
    asyncio.run(create_tables())
EOF
```

#### 8.3.2 Ejecutar Script

```bash
python create_tables.py
```

**Resultado esperado:**
```
Creando tablas en: localhost/gx_object_registry
Número de tablas a crear: 3
¡Tablas creadas exitosamente!
```

#### 8.3.3 Crear Secuencias para Autoincremento

```bash
PGPASSWORD='TU_CONTRASEÑA' psql -h localhost -U gxapp_user -d gx_object_registry << 'SQL'
-- Crear secuencias
CREATE SEQUENCE IF NOT EXISTS users_id_seq;
CREATE SEQUENCE IF NOT EXISTS object_types_id_seq;
CREATE SEQUENCE IF NOT EXISTS genexus_objects_id_seq;

-- Asociar secuencias a tablas
ALTER TABLE users ALTER COLUMN id SET DEFAULT nextval('users_id_seq');
ALTER TABLE object_types ALTER COLUMN id SET DEFAULT nextval('object_types_id_seq');
ALTER TABLE genexus_objects ALTER COLUMN id SET DEFAULT nextval('genexus_objects_id_seq');

ALTER SEQUENCE users_id_seq OWNED BY users.id;
ALTER SEQUENCE object_types_id_seq OWNED BY object_types.id;
ALTER SEQUENCE genexus_objects_id_seq OWNED BY genexus_objects.id;

-- Inicializar valores
SELECT setval('users_id_seq', 1, false);
SELECT setval('object_types_id_seq', 1, false);
SELECT setval('genexus_objects_id_seq', 1, false);
SQL
```

**Qué hace:** Crea las secuencias necesarias para que los IDs se generen automáticamente.

#### 8.3.4 Marcar Migración como Aplicada

```bash
alembic stamp head
```

**Qué hace:** Marca la migración como completada sin ejecutarla (porque ya creamos las tablas manualmente).

### 8.4 Insertar Datos Iniciales (Seed)

#### 8.4.1 Insertar Tipos de Objetos de GeneXus

```bash
PGPASSWORD='TU_CONTRASEÑA' psql -h localhost -U gxapp_user -d gx_object_registry << 'SQL'
-- Insertar los 27 tipos de objetos de GeneXus con sus códigos correctos
INSERT INTO object_types (id, name, created_at, updated_at) VALUES
(0, 'TRANSACTION', NOW(), NOW()),
(1, 'PROCEDURE', NOW(), NOW()),
(2, 'REPORT', NOW(), NOW()),
(3, 'MENU', NOW(), NOW()),
(4, 'WORK_PANEL', NOW(), NOW()),
(5, 'ATTRIBUTE', NOW(), NOW()),
(6, 'DATA_VIEW', NOW(), NOW()),
(7, 'TABLE', NOW(), NOW()),
(8, 'FOLDER', NOW(), NOW()),
(9, 'MODEL', NOW(), NOW()),
(10, 'GROUP', NOW(), NOW()),
(11, 'DOMAIN', NOW(), NOW()),
(12, 'PROMPT', NOW(), NOW()),
(13, 'WEB_PANEL', NOW(), NOW()),
(14, 'EXTERNAL_PROGRAM', NOW(), NOW()),
(17, 'MENU_BAR', NOW(), NOW()),
(18, 'TRANSACTION_STYLE', NOW(), NOW()),
(19, 'PROCEDURE_STYLE', NOW(), NOW()),
(20, 'REPORT_STYLE', NOW(), NOW()),
(21, 'WORK_PANEL_STYLE', NOW(), NOW()),
(22, 'PROMPT_STYLE', NOW(), NOW()),
(23, 'WEB_PANEL_STYLE', NOW(), NOW()),
(24, 'MENU_BAR_STYLE', NOW(), NOW()),
(25, 'THEME', NOW(), NOW()),
(26, 'STRUCTURED_DATA_TYPE', NOW(), NOW()),
(27, 'API_OBJECT', NOW(), NOW()),
(28, 'LANGUAGE', NOW(), NOW())
ON CONFLICT (id) DO NOTHING;

-- Verificar
SELECT COUNT(*) as total FROM object_types;
SQL
```

**Resultado esperado:**
```
 total
-------
    27
```

#### 8.4.2 Crear Usuario Administrador

Genera un hash de contraseña:

```bash
python3 << 'PYTHON'
from src.auth.infrastructure.password_hasher import hash_password
password = 'admin123456'  # Cambia esto por una contraseña segura
hashed = hash_password(password)
print(f"Hash generado: {hashed}")
PYTHON
```

**Resultado (ejemplo):**
```
Hash generado: $2b$12$5cuEg6XwMsEkWOmqAH.QxeWB9mELL6J2dieL8E374h9KXvyDlb.vS
```

Inserta el usuario administrador:

```bash
PGPASSWORD='TU_CONTRASEÑA' psql -h localhost -U gxapp_user -d gx_object_registry << 'SQL'
INSERT INTO users (username, email, hashed_password, full_name, is_active, must_change_password)
VALUES (
    'admin',
    'admin@tuempresa.com',
    '$2b$12$5cuEg6XwMsEkWOmqAH.QxeWB9mELL6J2dieL8E374h9KXvyDlb.vS',  -- Reemplaza con tu hash
    'Administrador del Sistema',
    true,
    false
);

-- Verificar
SELECT id, username, email, full_name FROM users;
SQL
```

**Resultado esperado:**
```
 id | username |       email        |        full_name
----+----------+--------------------+-------------------------
  1 | admin    | admin@tuempresa.com| Administrador del Sistema
```

**⚠️ IMPORTANTE:**
- Reemplaza el hash con el que generaste
- Cambia el email a uno real de tu organización
- Cambia la contraseña después del primer login
- Nunca uses `admin123456` en producción

### 8.5 Verificar Estado Final de la Base de Datos

```bash
PGPASSWORD='TU_CONTRASEÑA' psql -h localhost -U gxapp_user -d gx_object_registry << 'SQL'
-- Ver todas las tablas
\dt

-- Contar registros
SELECT 'users' as tabla, COUNT(*) as registros FROM users
UNION ALL
SELECT 'object_types', COUNT(*) FROM object_types
UNION ALL
SELECT 'genexus_objects', COUNT(*) FROM genexus_objects;

-- Ver secuencias
\ds
SQL
```

**Resultado esperado:**
```
       tabla       | registros
-------------------+-----------
 users             |         1
 object_types      |        27
 genexus_objects   |         0
```

---

## 9. Configuración del Servicio Systemd

### 9.1 Crear Archivo de Servicio

**Dónde ejecutar:** Servidor
**Usuario:** root o con sudo

```bash
sudo vim /etc/systemd/system/gxregistry.service
```

### 9.2 Contenido del Archivo de Servicio

```ini
[Unit]
Description=GeneXus Object Registry Service
After=network.target postgresql.service
Requires=postgresql.service

[Service]
Type=simple
User=gxapp
Group=gxapp
WorkingDirectory=/home/gxapp/apps/gx-object-registry
Environment="PATH=/home/gxapp/apps/gx-object-registry/venv/bin"
ExecStart=/home/gxapp/apps/gx-object-registry/venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

# Configuración de seguridad
NoNewPrivileges=true
PrivateTmp=true

# Logs
StandardOutput=journal
StandardError=journal
SyslogIdentifier=gxregistry

[Install]
WantedBy=multi-user.target
```

**Explicación de parámetros:**

| Parámetro | Descripción |
|-----------|-------------|
| `After=` | Inicia después de la red y PostgreSQL |
| `Requires=` | Requiere que PostgreSQL esté corriendo |
| `User=` | Usuario que ejecuta el servicio |
| `WorkingDirectory=` | Directorio del proyecto |
| `ExecStart=` | Comando para iniciar la aplicación |
| `Restart=always` | Reinicia automáticamente si falla |
| `RestartSec=10` | Espera 10 segundos antes de reiniciar |
| `NoNewPrivileges=` | Seguridad: no permite escalada de privilegios |
| `PrivateTmp=` | Seguridad: directorio temporal privado |

### 9.3 Recargar Systemd

```bash
sudo systemctl daemon-reload
```

**Qué hace:** Recarga la configuración de systemd para reconocer el nuevo servicio.

### 9.4 Habilitar el Servicio

```bash
sudo systemctl enable gxregistry
```

**Qué hace:** Configura el servicio para iniciar automáticamente al arrancar el servidor.

**Resultado esperado:**
```
Created symlink /etc/systemd/system/multi-user.target.wants/gxregistry.service → /etc/systemd/system/gxregistry.service.
```

### 9.5 Iniciar el Servicio

```bash
sudo systemctl start gxregistry
```

**Qué hace:** Inicia la aplicación.

### 9.6 Verificar Estado

```bash
sudo systemctl status gxregistry
```

**Resultado esperado:**
```
● gxregistry.service - GeneXus Object Registry Service
     Loaded: loaded (/etc/systemd/system/gxregistry.service; enabled)
     Active: active (running) since Mon 2026-08-03 18:00:00 UTC; 5s ago
   Main PID: 1234 (uvicorn)
      Tasks: 7
     Memory: 65.3M
        CPU: 489ms
     CGroup: /system.slice/gxregistry.service
             └─1234 /home/gxapp/apps/gx-object-registry/venv/bin/python3 ...

Aug 03 18:00:00 servidor uvicorn[1234]: INFO:     Started server process [1234]
Aug 03 18:00:00 servidor uvicorn[1234]: INFO:     Waiting for application startup.
Aug 03 18:00:00 servidor uvicorn[1234]: INFO:     Application startup complete.
Aug 03 18:00:00 servidor uvicorn[1234]: INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Estado correcto:** `Active: active (running)`

### 9.7 Ver Logs en Tiempo Real

```bash
sudo journalctl -u gxregistry -f
```

**Qué hace:** Muestra los logs del servicio en tiempo real (similar a `tail -f`).

**Para salir:** Presiona `Ctrl + C`

### 9.8 Comandos Útiles del Servicio

```bash
# Reiniciar servicio
sudo systemctl restart gxregistry

# Detener servicio
sudo systemctl stop gxregistry

# Ver estado
sudo systemctl status gxregistry

# Ver logs (últimas 100 líneas)
sudo journalctl -u gxregistry -n 100

# Ver logs con scroll
sudo journalctl -u gxregistry --no-pager
```

---

## 10. Instalación y Configuración de Nginx

### 🎯 Dos Opciones de Despliegue

Puedes elegir entre:

**Opción A:** Acceso directo por IP:PUERTO (más simple, recomendado para redes internas)
**Opción B:** Usar Nginx como proxy reverso (para producción con dominio)

---

### 📍 Opción A: Acceso Directo por IP:PUERTO (Recomendado para Red Corporativa)

Esta opción es **más simple** y **no requiere dominio**.

#### 10.A.1 Elegir Puerto de Acceso

Elige un puerto que no esté en uso. Recomendaciones:

| Puerto | Uso Común | ¿Disponible? |
|--------|-----------|--------------|
| 8080 | HTTP alternativo | ✅ Generalmente sí |
| 8081 | HTTP alternativo | ✅ Generalmente sí |
| 9000 | Aplicaciones web | ✅ Generalmente sí |
| 5000 | Aplicaciones web | ✅ Generalmente sí |

**Para este ejemplo usaremos el puerto 8080.**

#### 10.A.2 Modificar Servicio Systemd

Edita el archivo de servicio:

```bash
sudo vim /etc/systemd/system/gxregistry.service
```

Cambia la línea `ExecStart` para usar el puerto 8080:

```ini
ExecStart=/home/gxapp/apps/gx-object-registry/venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8080
```

**Qué hace `--host 0.0.0.0`:** Permite conexiones desde cualquier IP (no solo localhost).

**⚠️ IMPORTANTE:** Si cambias el puerto, actualiza también esta sección.

#### 10.A.3 Recargar y Reiniciar Servicio

```bash
sudo systemctl daemon-reload
sudo systemctl restart gxregistry
```

#### 10.A.4 Verificar que Escucha en el Puerto

```bash
sudo netstat -tlnp | grep :8080
```

**Resultado esperado:**
```
tcp        0      0 0.0.0.0:8080            0.0.0.0:*               LISTEN      1234/python3
```

#### 10.A.5 Probar Acceso Local

```bash
curl -I http://localhost:8080/web/login
```

**Resultado esperado:** `HTTP/1.1 200 OK`

#### 10.A.6 Abrir Puerto en Firewall UFW

```bash
sudo ufw allow 8080/tcp comment 'GX Registry Web App'
sudo ufw status
```

**Resultado esperado:**
```
8080/tcp                   ALLOW       Anywhere    # GX Registry Web App
```

#### 10.A.7 Información para el Administrador de Red

Proporciona esta información a Jorge (administrador de red) para abrir el puerto en el firewall/router:

```
┌─────────────────────────────────────────────────────┐
│     SOLICITUD DE APERTURA DE PUERTO                 │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Aplicación:  GeneXus Object Registry               │
│  Servidor:    [IP_DEL_SERVIDOR]                     │
│  Puerto:      8080                                   │
│  Protocolo:   TCP                                    │
│  Dirección:   Entrante (Inbound)                    │
│  Desde:       Red interna de la empresa             │
│  Uso:         Acceso web a la aplicación            │
│                                                      │
│  URL de acceso:                                      │
│  http://[IP_DEL_SERVIDOR]:8080/web/login            │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Ejemplo concreto:**
```
IP del servidor: 192.168.1.100
Puerto: 8080
URL: http://192.168.1.100:8080/web/login
```

#### 10.A.8 Probar Acceso desde Otra Computadora

Desde cualquier computadora en la red interna:

1. Abre un navegador
2. Ve a: `http://IP_DEL_SERVIDOR:8080/web/login`
3. Deberías ver la página de login

**Si no funciona:**
- Verifica que el firewall del servidor permite el puerto (UFW)
- Verifica que el router/firewall de red permite el puerto
- Verifica que el servicio está corriendo: `sudo systemctl status gxregistry`

#### 10.A.9 Flujo de Conexión (Opción A)

```
Cliente (Navegador)
    ↓ Puerto 8080
Uvicorn (FastAPI App) - 0.0.0.0:8080
    ↓ Puerto 5432 (localhost)
PostgreSQL
```

**Ventajas:**
- ✅ Configuración simple
- ✅ No requiere Nginx
- ✅ No requiere dominio
- ✅ No requiere HTTPS (para red interna)
- ✅ Un servicio menos que mantener

**Desventajas:**
- ❌ Sin SSL/HTTPS (no recomendado para Internet público)
- ❌ Sin caché de archivos estáticos
- ❌ Sin protección adicional de Nginx

---

### 📍 Opción B: Nginx como Proxy Reverso (Para Dominio Público)

Si necesitas un dominio o HTTPS, usa esta opción.

#### 10.B.1 Instalar Nginx

```bash
sudo apt install -y nginx
```

#### 10.B.2 Verificar Instalación

```bash
sudo systemctl status nginx
nginx -v
```

**Resultado esperado:**
```
Active: active (running)
nginx version: nginx/1.18.0
```

#### 10.B.3 Habilitar Inicio Automático

```bash
sudo systemctl enable nginx
```

#### 10.B.4 Crear Configuración del Sitio

```bash
sudo vim /etc/nginx/sites-available/gxregistry
```

#### 10.B.5 Contenido de la Configuración

**Para acceso por puerto específico (ej: 8080):**

```nginx
server {
    listen 8080;
    server_name _;  # Acepta cualquier host

    # Logs
    access_log /var/log/nginx/gxregistry-access.log;
    error_log /var/log/nginx/gxregistry-error.log;

    # Configuración del proxy reverso
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Archivos estáticos (si existen)
    location /static {
        alias /home/gxapp/apps/gx-object-registry/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Tamaño máximo de carga de archivos
    client_max_body_size 10M;
}
```

**Para acceso por dominio (puerto 80):**

```nginx
server {
    listen 80;
    server_name tudominio.com www.tudominio.com;  # Reemplaza con tu dominio

    # Logs
    access_log /var/log/nginx/gxregistry-access.log;
    error_log /var/log/nginx/gxregistry-error.log;

    # Configuración del proxy reverso
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Archivos estáticos (si existen)
    location /static {
        alias /home/gxapp/apps/gx-object-registry/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Tamaño máximo de carga de archivos
    client_max_body_size 10M;
}
```

#### 10.B.6 Habilitar el Sitio

```bash
sudo ln -s /etc/nginx/sites-available/gxregistry /etc/nginx/sites-enabled/
```

#### 10.B.7 Deshabilitar Sitio Predeterminado

```bash
sudo rm /etc/nginx/sites-enabled/default
```

#### 10.B.8 Verificar Configuración

```bash
sudo nginx -t
```

**Resultado esperado:**
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

#### 10.B.9 Reiniciar Nginx

```bash
sudo systemctl restart nginx
```

#### 10.B.10 Verificar que Funciona

```bash
curl -I http://localhost:8080
# o
curl -I http://localhost
```

#### 10.B.11 Flujo de Conexión (Opción B)

```
Cliente (Navegador)
    ↓ Puerto 8080 (o 80)
Nginx (Reverse Proxy)
    ↓ Puerto 8000 (localhost)
Uvicorn (FastAPI App)
    ↓ Puerto 5432 (localhost)
PostgreSQL
```

**Ventajas:**
- ✅ Proxy reverso profesional
- ✅ Mejor manejo de archivos estáticos
- ✅ Fácil agregar HTTPS después
- ✅ Headers de seguridad
- ✅ Rate limiting (configurable)

**Desventajas:**
- ❌ Un servicio adicional que mantener
- ❌ Configuración más compleja

---

## 11. Configuración del Firewall UFW

### 11.1 Instalar UFW (si no está instalado)

```bash
sudo apt install -y ufw
```

### 11.2 Configurar Reglas Básicas

**⚠️ IMPORTANTE:** Configura SSH primero para no perder acceso.

```bash
# Permitir SSH
sudo ufw allow 22/tcp comment 'SSH'
```

### 11.3 Configurar Puerto de la Aplicación

**Elige según la opción que elegiste en la sección 10:**

#### Si usas Opción A (Acceso directo por IP:PUERTO):

```bash
# Permitir el puerto de tu aplicación (ejemplo: 8080)
sudo ufw allow 8080/tcp comment 'GX Registry'
```

**⚠️ Reemplaza 8080 con el puerto que elegiste.**

#### Si usas Opción B (Nginx con dominio):

```bash
# Permitir HTTP
sudo ufw allow 80/tcp comment 'HTTP'

# Permitir HTTPS (si configurarás SSL)
sudo ufw allow 443/tcp comment 'HTTPS'
```

**Nota:** PostgreSQL (5432) NO debe estar abierto externamente.

### 11.3 Habilitar Firewall

```bash
sudo ufw --force enable
```

**Qué hace:** Activa el firewall con las reglas configuradas.

**Resultado esperado:**
```
Firewall is active and enabled on system startup
```

### 11.4 Verificar Estado

```bash
sudo ufw status verbose
```

**Resultado esperado:**
```
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    Anywhere    # SSH
80/tcp                     ALLOW IN    Anywhere    # HTTP
443/tcp                    ALLOW IN    Anywhere    # HTTPS
```

### 11.5 Comandos Útiles de UFW

```bash
# Ver reglas numeradas
sudo ufw status numbered

# Eliminar una regla (por número)
sudo ufw delete 3

# Deshabilitar firewall
sudo ufw disable

# Ver logs
sudo tail -f /var/log/ufw.log
```

---

## 12. Configuración de Backups Automáticos

### 12.1 Crear Directorio de Backups

```bash
su - gxapp
mkdir -p ~/backups
```

### 12.2 Crear Script de Backup

```bash
cat > ~/backups/backup.sh << 'EOF'
#!/bin/bash

# Script de backup automático para GeneXus Object Registry
# Ejecutar diariamente mediante cron

BACKUP_DIR="/home/gxapp/backups"
APP_DIR="/home/gxapp/apps/gx-object-registry"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="gxregistry_backup_${DATE}.tar.gz"
DB_NAME="gx_object_registry"
DB_USER="gxapp_user"
DB_PASSWORD="TU_CONTRASEÑA_AQUI"  # ⚠️ Reemplazar con la contraseña real

# Crear directorio temporal para el backup
TEMP_DIR="${BACKUP_DIR}/temp_${DATE}"
mkdir -p "${TEMP_DIR}"

# Backup de la base de datos
echo "[$(date)] Creando backup de la base de datos..."
PGPASSWORD="${DB_PASSWORD}" pg_dump -h localhost -U ${DB_USER} -d ${DB_NAME} > "${TEMP_DIR}/database.sql"

if [ $? -ne 0 ]; then
    echo "[$(date)] ERROR: Falló el backup de la base de datos"
    rm -rf "${TEMP_DIR}"
    exit 1
fi

# Backup del archivo .env
echo "[$(date)] Copiando archivo .env..."
cp "${APP_DIR}/.env" "${TEMP_DIR}/.env"

# Crear archivo comprimido
echo "[$(date)] Comprimiendo backup..."
cd "${BACKUP_DIR}"
tar -czf "${BACKUP_FILE}" -C "${TEMP_DIR}" .

if [ $? -ne 0 ]; then
    echo "[$(date)] ERROR: Falló la compresión del backup"
    rm -rf "${TEMP_DIR}"
    exit 1
fi

# Eliminar directorio temporal
rm -rf "${TEMP_DIR}"

# Eliminar backups antiguos (mantener últimos 7 días)
echo "[$(date)] Eliminando backups antiguos..."
find "${BACKUP_DIR}" -name "gxregistry_backup_*.tar.gz" -type f -mtime +7 -delete

echo "[$(date)] Backup completado: ${BACKUP_FILE}"
echo "[$(date)] Tamaño: $(du -h ${BACKUP_DIR}/${BACKUP_FILE} | cut -f1)"

# Verificar integridad
tar -tzf "${BACKUP_DIR}/${BACKUP_FILE}" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "[$(date)] Verificación de integridad: OK"
else
    echo "[$(date)] ERROR: El archivo de backup está corrupto"
    exit 1
fi

exit 0
EOF
```

**⚠️ IMPORTANTE:** Reemplaza `TU_CONTRASEÑA_AQUI` con la contraseña real de PostgreSQL.

### 12.3 Dar Permisos de Ejecución

```bash
chmod +x ~/backups/backup.sh
```

### 12.4 Probar el Script

```bash
~/backups/backup.sh
```

**Resultado esperado:**
```
[2026-08-03 18:30:00] Creando backup de la base de datos...
[2026-08-03 18:30:01] Copiando archivo .env...
[2026-08-03 18:30:01] Comprimiendo backup...
[2026-08-03 18:30:02] Eliminando backups antiguos...
[2026-08-03 18:30:02] Backup completado: gxregistry_backup_20260803_183000.tar.gz
[2026-08-03 18:30:02] Tamaño: 4.5K
[2026-08-03 18:30:02] Verificación de integridad: OK
```

### 12.5 Configurar Cron Job

```bash
crontab -e
```

Agrega esta línea al final del archivo:

```cron
# Backup diario a las 2:00 AM
0 2 * * * /home/gxapp/backups/backup.sh >> /home/gxapp/backups/backup.log 2>&1
```

**Explicación:**
- `0 2 * * *`: Ejecuta a las 2:00 AM todos los días
- `>> backup.log`: Guarda los logs del backup
- `2>&1`: Redirige errores al mismo archivo de log

**Para guardar y salir en vim:** Presiona `Esc`, luego escribe `:wq` y presiona `Enter`.

### 12.6 Verificar Cron Job

```bash
crontab -l
```

**Resultado esperado:**
```
0 2 * * * /home/gxapp/backups/backup.sh >> /home/gxapp/backups/backup.log 2>&1
```

### 12.7 Restaurar un Backup

Para restaurar desde un backup:

```bash
# Descomprimir backup
cd ~/backups
tar -xzf gxregistry_backup_YYYYMMDD_HHMMSS.tar.gz -C /tmp/restore

# Restaurar base de datos
PGPASSWORD='TU_CONTRASEÑA' psql -h localhost -U gxapp_user -d gx_object_registry < /tmp/restore/database.sql

# Restaurar .env (opcional)
cp /tmp/restore/.env ~/apps/gx-object-registry/.env

# Limpiar
rm -rf /tmp/restore
```

### 12.8 Backups Off-Site (Recomendado)

Para máxima seguridad, copia los backups fuera del servidor:

**Opción 1: Usar rsync (a otro servidor)**

```bash
# Agregar al script de backup
rsync -avz ~/backups/*.tar.gz usuario@servidor-backup:/ruta/backups/
```

**Opción 2: Subir a S3, Google Cloud Storage, etc.**

```bash
# Ejemplo con AWS S3
aws s3 cp ${BACKUP_DIR}/${BACKUP_FILE} s3://mi-bucket/backups/
```

**Opción 3: Copiar manualmente via SCP**

```bash
# Desde el servidor de backups
scp gxapp@servidor-produccion:~/backups/*.tar.gz /local/backups/
```

---

## 13. Configuración de HTTPS con Let's Encrypt (OPCIONAL)

**⚠️ Esta sección es OPCIONAL.**

**Solo necesitas HTTPS si:**
- ✅ Tienes un dominio público
- ✅ La aplicación será accesible desde Internet
- ✅ Necesitas encriptar el tráfico entre clientes y servidor

**NO necesitas HTTPS si:**
- ❌ Solo usarás la aplicación en red interna/corporativa
- ❌ Accedes por IP:PUERTO (ejemplo: http://192.168.1.100:8080)
- ❌ No tienes dominio

**Si NO necesitas HTTPS, salta esta sección y ve a la Sección 14.**

---

### 13.1 Requisitos Previos

- ✅ Dominio apuntando al servidor
- ✅ Puertos 80 y 443 abiertos en el firewall
- ✅ Nginx funcionando (Opción B)
- ✅ DNS propagado (puedes verificar con `dig tudominio.com` o `nslookup tudominio.com`)

### 13.2 Instalar Certbot

```bash
sudo apt install -y certbot python3-certbot-nginx
```

**Qué hace:** Instala Certbot y el plugin para Nginx.

### 13.3 Obtener Certificado SSL

```bash
sudo certbot --nginx -d tudominio.com -d www.tudominio.com
```

**Reemplaza:**
- `tudominio.com` con tu dominio real
- Agrega `-d subdominio.tudominio.com` para subdominios adicionales

**Interacción esperada:**

1. **Email:** Ingresa tu email para notificaciones de expiración
2. **Términos:** Acepta los términos de servicio (`A`)
3. **Newsletter:** Opcional (`N` para no suscribirse)
4. **Redirect:** Selecciona `2` para redirigir HTTP a HTTPS (recomendado)

**Resultado esperado:**
```
Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/tudominio.com/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/tudominio.com/privkey.pem
```

### 13.4 Verificar Configuración de Nginx

Certbot modifica automáticamente la configuración de Nginx:

```bash
sudo cat /etc/nginx/sites-available/gxregistry
```

**Deberías ver algo como:**

```nginx
server {
    server_name tudominio.com www.tudominio.com;

    # ... configuración existente ...

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/tudominio.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/tudominio.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}

server {
    if ($host = www.tudominio.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    if ($host = tudominio.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    listen 80;
    server_name tudominio.com www.tudominio.com;
    return 404; # managed by Certbot
}
```

### 13.5 Probar el Certificado

```bash
# Verificar sintaxis de Nginx
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx

# Probar HTTPS
curl -I https://tudominio.com
```

**Resultado esperado:**
```
HTTP/2 200
server: nginx/1.18.0
...
```

### 13.6 Configurar Renovación Automática

Certbot instala automáticamente un timer de systemd para renovar certificados.

**Verificar timer:**

```bash
sudo systemctl status certbot.timer
```

**Resultado esperado:**
```
Active: active (waiting)
```

**Probar renovación (dry-run):**

```bash
sudo certbot renew --dry-run
```

**Resultado esperado:**
```
Congratulations, all simulated renewals succeeded
```

**El certificado se renovará automáticamente antes de expirar (cada 60-90 días).**

### 13.7 Verificar Seguridad SSL

Prueba tu configuración SSL en: https://www.ssllabs.com/ssltest/

**Objetivo:** Obtener calificación A o A+.

### 13.8 Configuración SSL Avanzada (Opcional)

Para mejorar la seguridad SSL, puedes agregar headers adicionales:

```bash
sudo vim /etc/nginx/sites-available/gxregistry
```

Agrega dentro del bloque `server` para HTTPS:

```nginx
# Headers de seguridad
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
```

**Qué hace:**
- `HSTS`: Fuerza conexiones HTTPS por 1 año
- `X-Frame-Options`: Previene clickjacking
- `X-Content-Type-Options`: Previene MIME sniffing
- `X-XSS-Protection`: Protección contra XSS
- `Referrer-Policy`: Controla información de referrer

Reinicia Nginx:

```bash
sudo nginx -t
sudo systemctl restart nginx
```

---

## 14. Verificación Final

### 14.1 Checklist de Servicios

Verifica que todos los servicios estén corriendo:

```bash
sudo systemctl status postgresql
sudo systemctl status gxregistry
sudo systemctl status nginx
sudo systemctl status ufw
```

**Todos deben mostrar:** `Active: active (running)`

### 14.2 Verificar Conectividad

#### 14.2.1 Desde el Servidor (localhost)

```bash
# Probar FastAPI directamente
curl -I http://localhost:8000/docs

# Probar Nginx → FastAPI
curl -I http://localhost/web/login

# Probar HTTPS (si configurado)
curl -I https://tudominio.com/web/login
```

#### 14.2.2 Desde tu Navegador

Accede a:

- **HTTP:** http://tudominio.com/web/login
- **HTTPS:** https://tudominio.com/web/login

**Resultado esperado:** Página de login se carga correctamente.

#### 14.2.3 Probar Login

1. Accede a: https://tudominio.com/web/login
2. Ingresa credenciales:
   - **Usuario:** `admin`
   - **Contraseña:** La que configuraste al crear el usuario
3. **Resultado esperado:** Redirige al dashboard sin errores

#### 14.2.4 Verificar Navegación

Prueba navegar a todas las secciones:

- ✅ Dashboard: `/web/`
- ✅ Tipos de Objetos: `/web/object-types`
- ✅ Objetos: `/web/objects`
- ✅ Importar: `/web/import`
- ✅ Usuarios: `/web/users`

**Todas deben cargar sin error "Token inválido o expirado".**

### 14.3 Verificar Base de Datos

```bash
PGPASSWORD='TU_CONTRASEÑA' psql -h localhost -U gxapp_user -d gx_object_registry << 'SQL'
-- Contar registros
SELECT 'users' as tabla, COUNT(*) FROM users
UNION ALL
SELECT 'object_types', COUNT(*) FROM object_types
UNION ALL
SELECT 'genexus_objects', COUNT(*) FROM genexus_objects;

-- Ver estado de servicios de PostgreSQL
SELECT datname, numbackends, xact_commit, xact_rollback
FROM pg_stat_database
WHERE datname = 'gx_object_registry';
SQL
```

### 14.4 Verificar Logs

#### 14.4.1 Logs de la Aplicación

```bash
sudo journalctl -u gxregistry -n 50
```

**Buscar:**
- ✅ `Application startup complete`
- ✅ `Uvicorn running on http://0.0.0.0:8000`
- ❌ Errores o excepciones

#### 14.4.2 Logs de Nginx

```bash
sudo tail -n 50 /var/log/nginx/gxregistry-access.log
sudo tail -n 50 /var/log/nginx/gxregistry-error.log
```

**Logs de acceso deben mostrar:** Peticiones con código 200 o 307.

**Logs de error deben estar:** Vacíos o sin errores críticos.

#### 14.4.3 Logs de PostgreSQL

```bash
sudo tail -n 50 /var/log/postgresql/postgresql-15-main.log
```

### 14.5 Health Check Endpoint

Prueba el endpoint de salud:

```bash
curl http://localhost:8000/health
```

**Resultado esperado:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

**Nota:** Este endpoint puede no existir en el proyecto actual. Si da 404, es normal.

### 14.6 Verificar Recursos del Sistema

```bash
# Uso de CPU y memoria
htop

# O usar comandos básicos
free -h
df -h
uptime
```

**Verificar:**
- ✅ Uso de RAM < 80%
- ✅ Espacio en disco disponible > 20%
- ✅ Load average razonable (< número de CPUs)

---

## 15. Monitoreo y Logs

### 15.1 Logs de la Aplicación

#### 15.1.1 Ver Logs en Tiempo Real

```bash
sudo journalctl -u gxregistry -f
```

**Para salir:** `Ctrl + C`

#### 15.1.2 Ver Logs con Filtros

```bash
# Últimas 100 líneas
sudo journalctl -u gxregistry -n 100

# Logs desde hace 1 hora
sudo journalctl -u gxregistry --since "1 hour ago"

# Logs de hoy
sudo journalctl -u gxregistry --since today

# Logs con nivel de error
sudo journalctl -u gxregistry -p err

# Buscar texto específico
sudo journalctl -u gxregistry | grep "ERROR"
```

#### 15.1.3 Exportar Logs

```bash
# Guardar logs en archivo
sudo journalctl -u gxregistry -n 1000 > ~/logs_gxregistry_$(date +%Y%m%d).log
```

### 15.2 Logs de Nginx

```bash
# Accesos (últimas 50 líneas)
sudo tail -n 50 /var/log/nginx/gxregistry-access.log

# Errores
sudo tail -n 50 /var/log/nginx/gxregistry-error.log

# En tiempo real
sudo tail -f /var/log/nginx/gxregistry-access.log
```

#### 15.2.1 Analizar Logs de Acceso

```bash
# Ver IPs más frecuentes
sudo cat /var/log/nginx/gxregistry-access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -10

# Ver URLs más visitadas
sudo cat /var/log/nginx/gxregistry-access.log | awk '{print $7}' | sort | uniq -c | sort -rn | head -10

# Ver códigos de respuesta
sudo cat /var/log/nginx/gxregistry-access.log | awk '{print $9}' | sort | uniq -c | sort -rn
```

### 15.3 Logs de PostgreSQL

```bash
# Ver logs generales
sudo tail -f /var/log/postgresql/postgresql-15-main.log

# Ver logs de queries lentas (si está habilitado)
sudo grep "duration:" /var/log/postgresql/postgresql-15-main.log
```

### 15.4 Monitoreo de Recursos

#### 15.4.1 CPU y RAM en Tiempo Real

```bash
htop
```

**O instala htop si no está:**

```bash
sudo apt install htop
htop
```

**Buscar proceso:** `python3` (aplicación) y `postgres` (base de datos)

#### 15.4.2 Espacio en Disco

```bash
df -h
```

**Monitorear específicamente:**

```bash
# Uso del directorio de backups
du -sh ~/backups/

# Uso de PostgreSQL
sudo du -sh /var/lib/postgresql/

# Uso de logs
sudo du -sh /var/log/nginx/
sudo du -sh /var/log/postgresql/
```

#### 15.4.3 Conexiones de Red

```bash
# Ver puertos en escucha
sudo netstat -tlnp

# Ver conexiones activas
sudo netstat -anp | grep :8000
sudo netstat -anp | grep :5432
```

### 15.5 Monitoreo con Prometheus/Grafana (Avanzado - Opcional)

Para monitoreo avanzado, considera instalar:

- **Prometheus:** Recolección de métricas
- **Grafana:** Visualización de métricas
- **Node Exporter:** Métricas del sistema
- **Postgres Exporter:** Métricas de PostgreSQL

**No cubierto en esta guía.** Consulta documentación oficial para configuración.

---

## 16. Solución de Problemas

### 16.1 La Aplicación No Inicia

#### Síntoma:

```bash
sudo systemctl status gxregistry
```

Muestra: `Active: failed` o `Active: inactive (dead)`

#### Diagnóstico:

```bash
sudo journalctl -u gxregistry -n 50
```

#### Causas Comunes:

**1. Error de Import o Módulo Faltante**

**Síntoma en logs:**
```
ModuleNotFoundError: No module named 'jinja2'
```

**Solución:**
```bash
su - gxapp
cd ~/apps/gx-object-registry
source venv/bin/activate
pip install jinja2
sudo systemctl restart gxregistry
```

**2. Error de Conexión a PostgreSQL**

**Síntoma en logs:**
```
connection to server at "localhost" failed
```

**Solución:**
```bash
# Verificar que PostgreSQL está corriendo
sudo systemctl status postgresql

# Verificar DATABASE_URL en .env
cat ~/apps/gx-object-registry/.env | grep DATABASE_URL

# Probar conexión manual
PGPASSWORD='contraseña' psql -h localhost -U gxapp_user -d gx_object_registry -c "SELECT 1;"
```

**3. Puerto 8000 Ya en Uso**

**Síntoma en logs:**
```
[Errno 98] Address already in use
```

**Solución:**
```bash
# Ver qué está usando el puerto
sudo netstat -tlnp | grep :8000

# Matar proceso si es necesario
sudo kill -9 PID_DEL_PROCESO

# Reiniciar servicio
sudo systemctl restart gxregistry
```

**4. Permisos Incorrectos**

**Síntoma:**
```
PermissionError: [Errno 13] Permission denied
```

**Solución:**
```bash
# Corregir propietario
sudo chown -R gxapp:gxapp /home/gxapp/apps/gx-object-registry

# Verificar permisos de .env
chmod 600 /home/gxapp/apps/gx-object-registry/.env
```

### 16.2 Error 502 Bad Gateway (Nginx)

#### Síntoma:

Navegador muestra: "502 Bad Gateway"

#### Diagnóstico:

```bash
# Ver logs de Nginx
sudo tail -n 50 /var/log/nginx/gxregistry-error.log

# Verificar que la aplicación está corriendo
sudo systemctl status gxregistry

# Verificar que el puerto 8000 está escuchando
sudo netstat -tlnp | grep :8000
```

#### Causas Comunes:

**1. Aplicación No Está Corriendo**

```bash
sudo systemctl start gxregistry
sudo systemctl status gxregistry
```

**2. Nginx No Puede Conectarse al Puerto 8000**

Verificar configuración de Nginx:

```bash
sudo cat /etc/nginx/sites-available/gxregistry | grep proxy_pass
```

Debe ser: `proxy_pass http://127.0.0.1:8000;`

**3. Firewall Bloqueando Conexión Interna**

(Poco probable pero posible)

```bash
sudo ufw status
```

Asegúrate de que NO bloques localhost.

### 16.3 Error "Token Inválido o Expirado"

#### Síntoma:

Al navegar entre páginas sale: `{"detail":"Token inválido o expirado"}`

#### Causa:

Cookies no se están enviando correctamente entre rutas.

#### Solución:

Verificar que el archivo `src/auth/presentation/router.py` tiene `path="/"` en las cookies:

```bash
grep -A 10 "set_cookie" ~/apps/gx-object-registry/src/auth/presentation/router.py
```

Debe incluir:
```python
path="/",
```

Si falta, edita el archivo y reinicia:

```bash
sudo systemctl restart gxregistry
```

### 16.4 Error de Base de Datos: "relation does not exist"

#### Síntoma:

```
ProgrammingError: relation "users" does not exist
```

#### Causa:

Las tablas no se crearon o las migraciones no se ejecutaron.

#### Solución:

```bash
su - gxapp
cd ~/apps/gx-object-registry
source venv/bin/activate

# Verificar tablas
PGPASSWORD='contraseña' psql -h localhost -U gxapp_user -d gx_object_registry -c "\dt"

# Si no hay tablas, ejecutar migraciones
alembic upgrade head

# O crear manualmente (ver sección 8.3)
```

### 16.5 Error: "sequence does not exist"

#### Síntoma:

```
UndefinedTableError: relation "genexus_objects_id_seq" does not exist
```

#### Causa:

Las secuencias de autoincremento no se crearon.

#### Solución:

Ver sección **8.3.3** de esta guía para crear secuencias.

### 16.6 Logs Muestran Muchos Errores de Autenticación

#### Síntoma:

```bash
sudo journalctl -u gxregistry | grep "Invalid or expired token"
```

Muestra muchos resultados.

#### Causas:

1. Usuarios intentando acceder con tokens expirados
2. Bots o scanners intentando acceder
3. SECRET_KEY cambió y tokens anteriores ya no son válidos

#### Solución:

Normal en ciertos casos. Si es excesivo:

```bash
# Limpiar sesiones antiguas (pedir a usuarios que vuelvan a hacer login)
# No hay tabla de sesiones, los tokens JWT son stateless

# Opcional: Agregar rate limiting en Nginx (avanzado)
```

### 16.7 HTTPS No Funciona

#### Síntoma:

`ERR_SSL_PROTOCOL_ERROR` o certificado inválido.

#### Diagnóstico:

```bash
# Verificar certificado
sudo certbot certificates

# Verificar configuración Nginx
sudo nginx -t
```

#### Solución:

```bash
# Renovar certificado
sudo certbot renew

# Verificar firewall
sudo ufw status | grep 443

# Reiniciar Nginx
sudo systemctl restart nginx
```

### 16.8 Dominio No Resuelve

#### Síntoma:

`nslookup tudominio.com` no devuelve la IP del servidor.

#### Diagnóstico:

```bash
nslookup tudominio.com
dig tudominio.com
```

#### Causa:

Configuración DNS incorrecta o propagación pendiente.

#### Solución:

1. Verificar registros DNS en tu proveedor de dominio:
   - Registro A: `tudominio.com` → `IP_DEL_SERVIDOR`
   - Registro A: `www.tudominio.com` → `IP_DEL_SERVIDOR`

2. Esperar propagación DNS (puede tomar 24-48 horas)

3. Usar herramientas online: https://dnschecker.org

### 16.9 La Aplicación Funciona Localmente Pero No en Producción

#### Causas Comunes:

1. **Variables de entorno diferentes:**
   - Verificar `.env` en producción vs desarrollo

2. **BASE_URL incorrecta:**
   - Verificar CORS_ORIGINS y ALLOWED_HOSTS

3. **Permisos de archivos:**
   - Verificar `chmod` y `chown`

4. **PostgreSQL remoto no accesible:**
   - Verificar firewall, pg_hba.conf

5. **Puertos cerrados:**
   - Verificar UFW

---

## 17. Actualización de la Aplicación

### 17.1 Preparación

#### 17.1.1 Crear Backup Antes de Actualizar

**⚠️ CRÍTICO:** Siempre haz backup antes de actualizar.

```bash
su - gxapp
~/backups/backup.sh
```

**Verificar que el backup se creó:**

```bash
ls -lht ~/backups/*.tar.gz | head -1
```

### 17.2 Proceso de Actualización (Con Git)

#### 17.2.1 Conectarse al Servidor

```bash
ssh gxapp@tu-servidor
```

#### 17.2.2 Ir al Directorio del Proyecto

```bash
cd ~/apps/gx-object-registry
```

#### 17.2.3 Verificar Rama Actual

```bash
git branch
git status
```

#### 17.2.4 Descargar Cambios

```bash
git fetch origin
git pull origin main  # o la rama de producción
```

**Qué hace:** Descarga y aplica los últimos cambios del repositorio.

#### 17.2.5 Instalar Nuevas Dependencias (si hay)

```bash
source venv/bin/activate
pip install -r requirements.txt
```

#### 17.2.6 Ejecutar Migraciones (si hay)

```bash
alembic upgrade head
```

**Qué hace:** Aplica cambios de estructura de base de datos.

#### 17.2.7 Reiniciar el Servicio

```bash
sudo systemctl restart gxregistry
```

#### 17.2.8 Verificar Logs

```bash
sudo journalctl -u gxregistry -n 50
```

**Buscar:**
- ✅ `Application startup complete`
- ❌ Errores

#### 17.2.9 Probar la Aplicación

```bash
curl -I http://localhost/web/login
```

**Resultado esperado:** `HTTP/1.1 200 OK`

#### 17.2.10 Verificar en Navegador

Accede a: https://tudominio.com/web/login

### 17.3 Proceso de Actualización (Sin Git - Manual)

#### 17.3.1 En tu Máquina Local

```bash
# Crear archivo ZIP del proyecto actualizado
cd C:\Users\operador\Proyectos\web\gx-object-registry
Compress-Archive -Path .\* -DestinationPath gx-registry-v2.zip -Force
```

#### 17.3.2 Transferir al Servidor

```bash
scp gx-registry-v2.zip gxapp@tu-servidor:~/
```

#### 17.3.3 En el Servidor

```bash
# Conectarse
ssh gxapp@tu-servidor

# Detener servicio
sudo systemctl stop gxregistry

# Crear backup del código actual
cd ~/apps
mv gx-object-registry gx-object-registry.backup.$(date +%Y%m%d)

# Descomprimir nueva versión
mkdir gx-object-registry
cd gx-object-registry
unzip ~/gx-registry-v2.zip

# Copiar .env de la versión anterior
cp ~/apps/gx-object-registry.backup.*/env .env

# Reinstalar dependencias
source venv/bin/activate
pip install -r requirements.txt

# Ejecutar migraciones
alembic upgrade head

# Reiniciar servicio
sudo systemctl start gxregistry

# Verificar
sudo systemctl status gxregistry
```

### 17.4 Rollback (Revertir Actualización)

Si algo sale mal, revierte a la versión anterior:

#### 17.4.1 Con Git

```bash
cd ~/apps/gx-object-registry
git log --oneline -10  # Ver últimos commits
git checkout COMMIT_ANTERIOR
sudo systemctl restart gxregistry
```

#### 17.4.2 Sin Git (Restaurar desde Backup)

```bash
# Detener servicio
sudo systemctl stop gxregistry

# Restaurar código anterior
cd ~/apps
rm -rf gx-object-registry
cp -r gx-object-registry.backup.YYYYMMDD gx-object-registry

# Restaurar base de datos (si es necesario)
cd ~/backups
tar -xzf gxregistry_backup_YYYYMMDD_HHMMSS.tar.gz -C /tmp/restore
PGPASSWORD='contraseña' psql -h localhost -U gxapp_user -d gx_object_registry < /tmp/restore/database.sql

# Reiniciar servicio
sudo systemctl start gxregistry
```

### 17.5 Actualización con Zero Downtime (Avanzado)

Para aplicaciones críticas que no pueden tener tiempo de inactividad:

**Opción 1:** Usar dos instancias con un balanceador de carga (Nginx upstream)

**Opción 2:** Usar contenedores Docker con despliegue blue-green

**No cubierto en detalle en esta guía.**

---

## 18. Checklist de Despliegue

Usa este checklist para verificar que todo está correctamente configurado:

### 18.1 Preparación del Servidor

- [ ] Sistema operativo actualizado
- [ ] Zona horaria configurada
- [ ] Herramientas básicas instaladas
- [ ] Usuario `gxapp` creado
- [ ] SSH configurado de forma segura
- [ ] Python 3.10+ instalado
- [ ] pip actualizado

### 18.2 PostgreSQL

- [ ] PostgreSQL 15+ instalado
- [ ] Servicio PostgreSQL corriendo
- [ ] Base de datos `gx_object_registry` creada
- [ ] Usuario `gxapp_user` creado con contraseña segura
- [ ] Permisos correctamente asignados
- [ ] Conexión probada exitosamente
- [ ] PostgreSQL NO expuesto públicamente

### 18.3 Proyecto

- [ ] Código transferido al servidor
- [ ] Ubicado en `/home/gxapp/apps/gx-object-registry`
- [ ] Entorno virtual creado en `venv/`
- [ ] Dependencias instaladas desde `requirements.txt`
- [ ] `jinja2` instalado

### 18.4 Configuración

- [ ] Archivo `.env` creado y configurado
- [ ] `DATABASE_URL` correcta
- [ ] `SECRET_KEY` generada aleatoriamente
- [ ] `APP_ENV=production`
- [ ] `DEBUG=false`
- [ ] `CORS_ORIGINS` configurado
- [ ] `ALLOWED_HOSTS` configurado
- [ ] Permisos del `.env` establecidos a `600`

### 18.5 Base de Datos

- [ ] Migraciones ejecutadas o tablas creadas
- [ ] Secuencias de autoincremento creadas
- [ ] 27 tipos de objetos insertados
- [ ] Usuario administrador creado
- [ ] Conexión desde la aplicación probada

### 18.6 Servicio Systemd

- [ ] Archivo `/etc/systemd/system/gxregistry.service` creado
- [ ] Servicio habilitado (`systemctl enable`)
- [ ] Servicio iniciado (`systemctl start`)
- [ ] Servicio corriendo (`Active: active (running)`)
- [ ] Se reinicia automáticamente en caso de fallo
- [ ] Logs visibles en `journalctl`

### 18.7 Nginx

- [ ] Nginx instalado
- [ ] Configuración creada en `/etc/nginx/sites-available/gxregistry`
- [ ] Sitio habilitado (enlace simbólico en `sites-enabled/`)
- [ ] Sitio predeterminado deshabilitado
- [ ] Configuración probada (`nginx -t`)
- [ ] Nginx reiniciado
- [ ] Proxy reverso funcionando

### 18.8 Firewall

- [ ] UFW instalado
- [ ] Puerto 22 (SSH) abierto
- [ ] Puerto 80 (HTTP) abierto
- [ ] Puerto 443 (HTTPS) abierto
- [ ] Puerto 5432 (PostgreSQL) NO abierto públicamente
- [ ] UFW habilitado
- [ ] Estado verificado

### 18.9 HTTPS (Si aplicable)

- [ ] Dominio apuntando al servidor
- [ ] DNS propagado
- [ ] Certbot instalado
- [ ] Certificado SSL obtenido
- [ ] HTTP redirige a HTTPS
- [ ] Certificado verificado en navegador
- [ ] Renovación automática configurada
- [ ] Test de renovación exitoso (`--dry-run`)

### 18.10 Backups

- [ ] Directorio de backups creado (`~/backups`)
- [ ] Script de backup creado (`backup.sh`)
- [ ] Permisos de ejecución asignados
- [ ] Script probado manualmente
- [ ] Cron job configurado (2:00 AM diario)
- [ ] Primer backup creado exitosamente
- [ ] Retención configurada (7 días)

### 18.11 Verificación

- [ ] Aplicación accesible desde navegador
- [ ] Login funciona correctamente
- [ ] Dashboard carga sin errores
- [ ] Navegación entre secciones funciona
- [ ] Sin error "Token inválido o expirado"
- [ ] API docs accesible (`/docs`)
- [ ] Logs sin errores críticos

### 18.12 Monitoreo

- [ ] Logs de aplicación accesibles
- [ ] Logs de Nginx accesibles
- [ ] Logs de PostgreSQL accesibles
- [ ] Uso de recursos monitoreado (CPU, RAM, disco)
- [ ] Conexiones de red monitoreadas

### 18.13 Seguridad

- [ ] Contraseñas fuertes utilizadas
- [ ] `.env` no subido a Git
- [ ] `.gitignore` configurado correctamente
- [ ] PostgreSQL solo acepta conexiones desde localhost
- [ ] Aplicación NO corre como root
- [ ] Firewall configurado correctamente
- [ ] HTTPS funcionando (si aplicable)
- [ ] Headers de seguridad configurados
- [ ] Backups encriptados (si aplicable)

### 18.14 Documentación

- [ ] Credenciales de administrador documentadas en lugar seguro
- [ ] Contraseña de base de datos documentada
- [ ] SECRET_KEY respaldada
- [ ] Procedimientos de backup documentados
- [ ] Procedimientos de restauración documentados
- [ ] Contactos de soporte documentados

---

## 19. Información Adicional

### 19.1 Ubicaciones Importantes

| Recurso | Ubicación |
|---------|-----------|
| Código de la aplicación | `/home/gxapp/apps/gx-object-registry` |
| Entorno virtual Python | `/home/gxapp/apps/gx-object-registry/venv` |
| Archivo .env | `/home/gxapp/apps/gx-object-registry/.env` |
| Backups | `/home/gxapp/backups` |
| Servicio systemd | `/etc/systemd/system/gxregistry.service` |
| Configuración Nginx | `/etc/nginx/sites-available/gxregistry` |
| Logs de aplicación | `journalctl -u gxregistry` |
| Logs de Nginx | `/var/log/nginx/gxregistry-*.log` |
| Logs de PostgreSQL | `/var/log/postgresql/postgresql-15-main.log` |
| Certificados SSL | `/etc/letsencrypt/live/tudominio.com/` |

### 19.2 Comandos Rápidos de Referencia

```bash
# Reiniciar todos los servicios
sudo systemctl restart postgresql
sudo systemctl restart gxregistry
sudo systemctl restart nginx

# Ver estado de todos los servicios
sudo systemctl status postgresql gxregistry nginx

# Ver logs en tiempo real
sudo journalctl -u gxregistry -f

# Crear backup manual
~/backups/backup.sh

# Verificar espacio en disco
df -h

# Ver uso de recursos
htop

# Probar conectividad
curl -I http://localhost/web/login
```

### 19.3 Contactos de Soporte

**Documentación oficial:**
- FastAPI: https://fastapi.tiangolo.com
- PostgreSQL: https://www.postgresql.org/docs/
- Nginx: https://nginx.org/en/docs/
- Certbot: https://certbot.eff.org/docs/

**Comunidad:**
- FastAPI Discussions: https://github.com/tiangolo/fastapi/discussions
- Stack Overflow: https://stackoverflow.com

### 19.4 Recursos Adicionales

**Seguridad:**
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- SSL Labs: https://www.ssllabs.com/ssltest/

**Monitoreo:**
- Prometheus: https://prometheus.io
- Grafana: https://grafana.com

**Herramientas útiles:**
- pgAdmin (GUI para PostgreSQL): https://www.pgadmin.org
- Postman (Testing de API): https://www.postman.com

---

## 20. Notas Finales

### 20.1 Buenas Prácticas

1. **Backups:** Realiza backups regulares y pruébalos periódicamente
2. **Actualizaciones:** Mantén el sistema operativo y dependencias actualizadas
3. **Monitoreo:** Revisa logs regularmente
4. **Seguridad:** Cambia contraseñas predeterminadas inmediatamente
5. **Documentación:** Mantén documentada cualquier modificación

### 20.2 Próximos Pasos Recomendados

1. Configurar monitoreo avanzado (Prometheus + Grafana)
2. Implementar CI/CD para despliegues automáticos
3. Configurar alertas por email/Slack para errores
4. Implementar rate limiting en Nginx
5. Configurar backups off-site automáticos
6. Implementar WAF (Web Application Firewall)
7. Realizar auditoría de seguridad

### 20.3 Soporte

Para problemas no cubiertos en esta guía:

1. Revisa los logs detalladamente
2. Busca el error específico en Stack Overflow
3. Consulta la documentación oficial de la herramienta relevante
4. Contacta al equipo de desarrollo del proyecto

---

**🎉 ¡Felicitaciones!** Has completado el despliegue de **GeneXus Object Registry** en producción.

**Versión de esta guía:** 1.0
**Última actualización:** 2026-08-03

---
