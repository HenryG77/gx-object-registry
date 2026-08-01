# Guía de Instalación Completa - GeneXus Object Registry

Esta es una guía **exhaustiva y detallada paso a paso** para instalar, configurar, ejecutar y desplegar el sistema GeneXus Object Registry.

**Objetivo**: Que cualquier persona, incluso sin experiencia previa, pueda seguir esta guía y tener el sistema funcionando completamente.

---

## Tabla de Contenidos

### PARTE 1: INSTALACIÓN LOCAL DESDE CERO
1. [Introducción](#1-introducción)
2. [Requisitos del Sistema](#2-requisitos-del-sistema)
3. [Preparación del Sistema Operativo](#3-preparación-del-sistema-operativo)
4. [Instalación de Git](#4-instalación-de-git)
5. [Instalación de Python 3.11+](#5-instalación-de-python-311)
6. [Instalación de PostgreSQL 15+](#6-instalación-de-postgresql-15)
7. [Clonar el Repositorio](#7-clonar-el-repositorio)
8. [Analizar la Estructura del Proyecto](#8-analizar-la-estructura-del-proyecto)
9. [Crear Entorno Virtual](#9-crear-entorno-virtual)
10. [Instalar Dependencias](#10-instalar-dependencias)
11. [Configurar Variables de Entorno](#11-configurar-variables-de-entorno)
12. [Configurar Base de Datos](#12-configurar-base-de-datos)
13. [Ejecutar Migraciones](#13-ejecutar-migraciones)
14. [Crear Usuario Administrador](#14-crear-usuario-administrador)
15. [Cargar Datos Iniciales](#15-cargar-datos-iniciales)
16. [Ejecutar el Proyecto en Desarrollo](#16-ejecutar-el-proyecto-en-desarrollo)
17. [Verificar Instalación](#17-verificar-instalación)
18. [Solución de Problemas Comunes](#18-solución-de-problemas-comunes)

### PARTE 2: DESPLIEGUE EN PRODUCCIÓN
19. [Introducción al Despliegue](#19-introducción-al-despliegue)
20. [Preparar Servidor Linux (Ubuntu 22.04 LTS)](#20-preparar-servidor-linux-ubuntu-2204-lts)
21. [Instalar Herramientas en el Servidor](#21-instalar-herramientas-en-el-servidor)
22. [Configurar PostgreSQL en Producción](#22-configurar-postgresql-en-producción)
23. [Clonar y Configurar el Proyecto](#23-clonar-y-configurar-el-proyecto)
24. [Configurar Gunicorn](#24-configurar-gunicorn)
25. [Configurar systemd](#25-configurar-systemd)
26. [Configurar Nginx](#26-configurar-nginx)
27. [Configurar HTTPS con Let's Encrypt](#27-configurar-https-con-lets-encrypt)
28. [Configurar Firewall](#28-configurar-firewall)
29. [Actualizar el Sistema](#29-actualizar-el-sistema)
30. [Backups y Recuperación](#30-backups-y-recuperación)
31. [Monitoreo y Logs](#31-monitoreo-y-logs)
32. [Checklist Final](#32-checklist-final)

---

# PARTE 1: INSTALACIÓN LOCAL DESDE CERO

---

## 1. Introducción

### ¿Qué es GeneXus Object Registry?

**GeneXus Object Registry** es un sistema web desarrollado con Python y FastAPI que permite:

- Gestionar catálogos de objetos GeneXus
- Organizar objetos por tipos (Procedures, Transactions, etc.)
- Importar masivamente desde archivos CSV
- Controlar acceso con autenticación
- Auditar quién crea cada objeto

### Componentes del Sistema

El sistema está compuesto por:

1. **Backend**: FastAPI (Python 3.11+)
   - API REST en `/api/...`
   - Servidor web en `/web/...`

2. **Base de Datos**: PostgreSQL 15+
   - Almacena usuarios, objetos y tipos

3. **Frontend**: HTML + Bootstrap 5 + JavaScript
   - Interfaz web renderizada server-side con Jinja2

4. **Autenticación**: JWT con cookies HttpOnly

### Arquitectura del Proceso de Instalación

```
1. Sistema Operativo Limpio
         ↓
2. Instalar Git
         ↓
3. Instalar Python 3.11+
         ↓
4. Instalar pip (gestor de paquetes)
         ↓
5. Instalar PostgreSQL 15+
         ↓
6. Clonar Repositorio
         ↓
7. Crear Entorno Virtual
         ↓
8. Instalar Dependencias (requirements.txt)
         ↓
9. Configurar Variables de Entorno (.env)
         ↓
10. Crear Base de Datos
         ↓
11. Ejecutar Migraciones (Alembic)
         ↓
12. Crear Usuario Admin
         ↓
13. Cargar Datos Iniciales (opcional)
         ↓
14. Iniciar Servidor (Uvicorn)
         ↓
15. Acceder desde Navegador
```

### Tecnologías Necesarias

| Tecnología | Versión Mínima | Uso |
|------------|----------------|-----|
| Python | 3.11+ | Lenguaje backend |
| pip | 23.0+ | Gestor de paquetes |
| PostgreSQL | 15+ | Base de datos |
| Git | 2.30+ | Control de versiones |
| Navegador | Moderno | Acceso a la UI |

### Sistemas Operativos Compatibles

✅ **Windows** 10/11
✅ **Ubuntu** 20.04 LTS / 22.04 LTS
✅ **Debian** 11+
✅ **macOS** 11+

Esta guía cubre los tres sistemas operativos.

---

## 2. Requisitos del Sistema

### Hardware Mínimo Recomendado

**Desarrollo Local**:
- **CPU**: 2 núcleos
- **RAM**: 4 GB
- **Disco**: 10 GB libres
- **Conexión**: Internet

**Producción**:
- **CPU**: 2 núcleos (4+ recomendado)
- **RAM**: 2 GB (4+ GB recomendado)
- **Disco**: 20 GB (SSD recomendado)
- **Conexión**: Internet estable

### Software Requerido

| Requisito | Versión | Obligatorio | Uso |
|-----------|---------|-------------|-----|
| **Sistema Operativo** | Windows 10+, Ubuntu 20.04+, macOS 11+ | ✅ Sí | Sistema base |
| **Python** | 3.11 o superior | ✅ Sí | Runtime de la aplicación |
| **pip** | 23.0+ (incluido con Python) | ✅ Sí | Gestor de paquetes Python |
| **PostgreSQL** | 15 o superior | ✅ Sí | Base de datos |
| **Git** | 2.30+ | ✅ Sí | Clonar repositorio |
| **Docker** | 20.10+ | ⚪ Opcional | Alternativa para BD |
| **Docker Compose** | 2.0+ | ⚪ Opcional | Orquestar servicios |
| **Navegador** | Chrome 90+, Firefox 88+, Edge 90+ | ✅ Sí | Acceder a la interfaz |

### Puertos Utilizados

| Puerto | Servicio | Configurable |
|--------|----------|--------------|
| 8000 | FastAPI (backend + frontend) | ✅ Sí (`--port`) |
| 5432 | PostgreSQL | ✅ Sí (DATABASE_URL) |

**Importante**: Asegúrate de que estos puertos estén disponibles.

---

## 3. Preparación del Sistema Operativo

Antes de instalar cualquier herramienta, asegúrate de que tu sistema operativo esté actualizado.

### Windows 10/11

#### Actualizar Windows

1. Presiona `Win + I` para abrir Configuración
2. Ve a **Windows Update**
3. Haz clic en **Buscar actualizaciones**
4. Instala todas las actualizaciones disponibles
5. Reinicia si es necesario

#### Abrir PowerShell o CMD

Presiona `Win + X` y selecciona:
- **Windows Terminal** (recomendado si está disponible)
- **PowerShell**
- **Símbolo del sistema (CMD)**

**Para el resto de esta guía, cuando veas comandos, ejecútalos en PowerShell o CMD.**

---

### Ubuntu 20.04 / 22.04 LTS

#### Actualizar Sistema

Abre una terminal (`Ctrl + Alt + T`) y ejecuta:

```bash
sudo apt update
sudo apt upgrade -y
```

**Explicación**:
- `apt update`: Actualiza la lista de paquetes disponibles
- `apt upgrade`: Instala las versiones más recientes de los paquetes

Si te pide confirmación, presiona `Y` y luego `Enter`.

#### Reiniciar si es Necesario

```bash
sudo reboot
```

---

### macOS 11+

#### Actualizar macOS

1. Abre **Preferencias del Sistema**
2. Ve a **Actualización de Software**
3. Instala todas las actualizaciones disponibles
4. Reinicia si es necesario

#### Instalar Homebrew (Gestor de Paquetes)

Homebrew facilita la instalación de herramientas en macOS.

Abre **Terminal** (`Cmd + Espacio`, escribe "Terminal") y ejecuta:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Sigue las instrucciones en pantalla.

**Verificar instalación**:

```bash
brew --version
```

Deberías ver algo como:

```
Homebrew 4.0.0
```

---

## 4. Instalación de Git

Git es necesario para clonar el repositorio del proyecto.

### Verificar si Git Ya Está Instalado

Abre tu terminal y ejecuta:

```bash
git --version
```

**Si ves algo como**:
```
git version 2.39.0
```

✅ **Git ya está instalado**. Puedes saltar a la [sección 5](#5-instalación-de-python-311).

**Si ves un error como**:
```
'git' is not recognized as an internal or external command
```
o
```
command not found: git
```

❌ **Git no está instalado**. Continúa con la instalación.

---

### Instalación de Git en Windows

#### Opción 1: Instalador Oficial

1. Ve a https://git-scm.com/download/win
2. Descarga el instalador (64-bit Git for Windows Setup)
3. Ejecuta el instalador descargado
4. **Configuración recomendada durante la instalación**:
   - ✅ Use Git from the Windows Command Prompt
   - ✅ Use the OpenSSL library
   - ✅ Checkout Windows-style, commit Unix-style line endings
   - ✅ Use MinTTY (the default terminal of MSYS2)
5. Haz clic en **Next** hasta finalizar
6. Haz clic en **Install** y luego en **Finish**

#### Verificar Instalación

**Cierra y vuelve a abrir** PowerShell/CMD (importante para cargar PATH).

Ejecuta:

```bash
git --version
```

Deberías ver:

```
git version 2.39.0
```

✅ Git instalado correctamente.

---

### Instalación de Git en Ubuntu/Debian

```bash
sudo apt update
sudo apt install git -y
```

**Verificar**:

```bash
git --version
```

---

### Instalación de Git en macOS

#### Con Homebrew (Recomendado)

```bash
brew install git
```

#### O Instalador Oficial

1. Ve a https://git-scm.com/download/mac
2. Descarga e instala

**Verificar**:

```bash
git --version
```

---

### Configurar Git (Primera Vez)

Configura tu nombre y email (necesario para commits):

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

**Verificar configuración**:

```bash
git config --global --list
```

Deberías ver:

```
user.name=Tu Nombre
user.email=tu@email.com
```

---

## 5. Instalación de Python 3.11+

Python es el lenguaje en el que está desarrollado el backend.

### Verificar si Python Ya Está Instalado

```bash
python --version
```

**Alternativas** (prueba estas si el comando anterior no funciona):

```bash
python3 --version
```

**En Windows**:

```bash
py --version
```

**Si ves**:

```
Python 3.11.0
```
o
```
Python 3.12.0
```

✅ **Python 3.11+ ya está instalado**. Salta a [verificar pip](#verificar-pip).

**Si ves una versión menor** (ej: `Python 3.9.0`):

❌ **Necesitas actualizar a Python 3.11+**.

**Si ves un error**:

```
'python' is not recognized
```

❌ **Python no está instalado**.

---

### Instalación de Python en Windows

#### Descargar Python

1. Ve a https://www.python.org/downloads/
2. Descarga **Python 3.11** o superior (ej: Python 3.11.8)
3. **Importante**: Durante la instalación:
   - ✅ **Marca la casilla "Add Python to PATH"** (MUY IMPORTANTE)
   - Selecciona "Install Now"

#### Verificar Instalación

**Cierra y vuelve a abrir** PowerShell/CMD.

```bash
python --version
```

Si no funciona, prueba:

```bash
py --version
```

**Si `py` funciona pero `python` no**:

En Windows, usa `py` en lugar de `python` para todos los comandos de esta guía.

---

### Instalación de Python en Ubuntu/Debian

#### Ubuntu 22.04

Python 3.11 no viene por defecto. Instálalo así:

```bash
sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev -y
```

#### Verificar

```bash
python3.11 --version
```

#### Crear Alias (Opcional)

Para usar `python3` en lugar de `python3.11`:

```bash
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
```

---

### Instalación de Python en macOS

#### Con Homebrew

```bash
brew install python@3.11
```

#### Verificar

```bash
python3.11 --version
```

#### Crear Alias

```bash
echo 'alias python=python3.11' >> ~/.zshrc
echo 'alias python3=python3.11' >> ~/.zshrc
source ~/.zshrc
```

---

### Verificar pip

**pip** es el gestor de paquetes de Python. Viene incluido con Python 3.11+.

```bash
python -m pip --version
```

o

```bash
python3 -m pip --version
```

o (Windows):

```bash
py -m pip --version
```

**Deberías ver**:

```
pip 23.0.1 from ... (python 3.11)
```

#### Si pip No Está Disponible

```bash
python -m ensurepip --upgrade
```

#### Actualizar pip

```bash
python -m pip install --upgrade pip
```

---

## 6. Instalación de PostgreSQL 15+

PostgreSQL es la base de datos que utiliza el sistema.

### Verificar si PostgreSQL Ya Está Instalado

```bash
psql --version
```

**Si ves**:

```
psql (PostgreSQL) 15.3
```

✅ PostgreSQL ya está instalado. Verifica que esté corriendo:

```bash
# Linux
sudo systemctl status postgresql

# macOS
brew services list | grep postgresql
```

Si está corriendo, salta a [Configurar Base de Datos](#12-configurar-base-de-datos).

---

### Instalación de PostgreSQL en Windows

#### Descargar PostgreSQL

1. Ve a https://www.postgresql.org/download/windows/
2. Descarga el instalador de **EnterpriseDB** para PostgreSQL 15+
3. Ejecuta el instalador

#### Configuración Durante la Instalación

- **Componentes**: Deja todo seleccionado
- **Directorio de datos**: Deja el predeterminado
- **Contraseña del superusuario (postgres)**:
  - Ingresa una contraseña (ej: `postgres123`)
  - **⚠️ ANOTA ESTA CONTRASEÑA, LA NECESITARÁS**
- **Puerto**: 5432 (predeterminado)
- **Locale**: Deja el predeterminado

Haz clic en **Next** hasta finalizar.

#### Verificar Instalación

Abre **SQL Shell (psql)** desde el menú de inicio.

Te pedirá:
- Server: presiona `Enter` (usa localhost)
- Database: presiona `Enter` (usa postgres)
- Port: presiona `Enter` (usa 5432)
- Username: presiona `Enter` (usa postgres)
- Password: ingresa la contraseña que configuraste

Si te conectas, verás:

```
postgres=#
```

✅ PostgreSQL instalado correctamente.

Escribe `\q` y presiona `Enter` para salir.

---

### Instalación de PostgreSQL en Ubuntu/Debian

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib -y
```

#### Verificar que PostgreSQL Esté Corriendo

```bash
sudo systemctl status postgresql
```

Deberías ver `active (running)`.

#### Configurar Contraseña del Usuario postgres

```bash
sudo -u postgres psql
```

Estás ahora dentro de PostgreSQL. Ejecuta:

```sql
ALTER USER postgres PASSWORD 'postgres123';
\q
```

---

### Instalación de PostgreSQL en macOS

#### Con Homebrew

```bash
brew install postgresql@15
```

#### Iniciar PostgreSQL

```bash
brew services start postgresql@15
```

#### Verificar

```bash
psql --version
```

#### Configurar Contraseña

```bash
psql postgres
```

```sql
ALTER USER postgres PASSWORD 'postgres123';
\q
```

---

### Verificar Conexión a PostgreSQL

Ejecuta:

```bash
psql -U postgres -h localhost
```

Te pedirá la contraseña. Ingresa `postgres123` (o la que configuraste).

Si ves:

```
postgres=#
```

✅ Conexión exitosa.

Sal con `\q`.

---

## 7. Clonar el Repositorio

Ahora que tienes Git instalado, clona el proyecto.

### Obtener la URL del Repositorio

Si el repositorio está en GitHub, GitLab o Bitbucket, copia la URL.

**Ejemplo**:

```
https://github.com/usuario/gx-object-registry.git
```

### Clonar

Abre tu terminal en la carpeta donde quieres guardar el proyecto.

**Por ejemplo**:

```bash
cd C:\Proyectos\     # Windows
cd ~/Proyectos/       # Linux/macOS
```

Si la carpeta no existe:

```bash
mkdir Proyectos
cd Proyectos
```

Ahora clona:

```bash
git clone <URL_DEL_REPOSITORIO>
```

**Ejemplo**:

```bash
git clone https://github.com/usuario/gx-object-registry.git
```

Verás:

```
Cloning into 'gx-object-registry'...
remote: Counting objects: 1234, done.
...
```

✅ Repositorio clonado.

### Entrar al Proyecto

```bash
cd gx-object-registry
```

**Verificar que estás en la carpeta correcta**:

```bash
# Windows
dir

# Linux/macOS
ls
```

Deberías ver archivos como:

```
requirements.txt
src/
alembic/
.env.example
README.md
```

---

## 8. Analizar la Estructura del Proyecto

Ejecuta:

```bash
# Windows
dir

# Linux/macOS
ls -la
```

Deberías ver:

```
alembic/              # Migraciones de base de datos
scripts/              # Scripts de utilidad
src/                  # Código fuente
  ├── auth/           # Autenticación y usuarios
  ├── genexus_objects/ # Objetos GeneXus
  ├── object_types/   # Tipos de objetos
  ├── imports/        # Importación CSV
  ├── web/            # Interfaz web
  └── shared/         # Código compartido
tests/                # Pruebas automatizadas
.env.example          # Plantilla de variables de entorno
requirements.txt      # Dependencias Python
alembic.ini           # Configuración de Alembic
docker-compose.yml    # Configuración Docker (opcional)
```

---

## 9. Crear Entorno Virtual

Un entorno virtual aísla las dependencias del proyecto.

### ¿Por Qué Usar un Entorno Virtual?

- ✅ Aísla las dependencias del proyecto
- ✅ Evita conflictos con otros proyectos
- ✅ Permite tener diferentes versiones de paquetes

### Crear Entorno Virtual

**En la carpeta raíz del proyecto** (`gx-object-registry/`), ejecuta:

```bash
python -m venv venv
```

**Alternativas**:

```bash
python3 -m venv venv
```

o (Windows):

```bash
py -m venv venv
```

**¿Qué hace este comando?**
- Crea una carpeta `venv/` con una copia aislada de Python

Verás:

```
Creating virtual environment...
```

**Verificar**:

```bash
# Windows
dir venv

# Linux/macOS
ls venv
```

Deberías ver carpetas como `Scripts/` (Windows) o `bin/` (Linux/macOS).

---

### Activar Entorno Virtual

**IMPORTANTE**: Debes activar el entorno virtual **cada vez que abras una nueva terminal**.

#### Windows (PowerShell)

```bash
venv\Scripts\activate
```

#### Windows (CMD)

```bash
venv\Scripts\activate.bat
```

#### Linux/macOS

```bash
source venv/bin/activate
```

**¿Cómo saber si está activo?**

Verás `(venv)` al inicio de tu prompt:

```
(venv) C:\Proyectos\gx-object-registry>
```

✅ Entorno virtual activado.

---

### Problema: Script Execution Disabled (Windows PowerShell)

Si ves:

```
... cannot be loaded because running scripts is disabled on this system
```

**Solución**:

Ejecuta PowerShell **como Administrador** y ejecuta:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Confirma con `Y`.

Cierra PowerShell de administrador y vuelve a tu PowerShell normal.

Intenta activar nuevamente:

```bash
venv\Scripts\activate
```

---

## 10. Instalar Dependencias

Con el entorno virtual activado, instala las dependencias del proyecto.

### Actualizar pip (Recomendado)

```bash
python -m pip install --upgrade pip
```

### Instalar Dependencias

```bash
pip install -r requirements.txt
```

**¿Qué hace este comando?**
- Lee el archivo `requirements.txt`
- Instala todas las librerías listadas

Verás:

```
Collecting fastapi>=0.109.0
  Downloading fastapi-0.109.2-py3-none-any.whl
...
Successfully installed fastapi-0.109.2 uvicorn-0.27.1 ...
```

**Tiempo estimado**: 2-5 minutos.

### Verificar Instalación

```bash
pip list
```

Deberías ver paquetes como:

```
fastapi         0.109.2
uvicorn         0.27.1
sqlalchemy      2.0.25
alembic         1.13.1
pydantic        2.5.3
...
```

✅ Dependencias instaladas correctamente.

---

### Problema: Pip Install Falla

#### Error: No module named 'pip'

```bash
python -m ensurepip --upgrade
```

#### Error: Microsoft Visual C++ Required (Windows)

Si ves errores relacionados con compilación:

1. Descarga **Build Tools for Visual Studio**:
   https://visualstudio.microsoft.com/downloads/
2. Instala **Desktop development with C++**
3. Reinicia la terminal e intenta de nuevo

#### Error: Permission Denied (Linux/macOS)

Asegúrate de tener el entorno virtual activado.

NO uses `sudo pip install`.

---

## 11. Configurar Variables de Entorno

El proyecto utiliza un archivo `.env` para configuración.

### Crear Archivo .env

```bash
# Windows
copy .env.example .env

# Linux/macOS
cp .env.example .env
```

### Editar .env

Abre el archivo `.env` con un editor de texto:

```bash
# Con Visual Studio Code
code .env

# Con nano (Linux)
nano .env

# Con notepad (Windows)
notepad .env
```

### Variables Obligatorias

Debes configurar al menos:

#### 1. DATABASE_URL

**Formato**:

```env
DATABASE_URL=postgresql+asyncpg://usuario:contraseña@host:puerto/nombre_bd
```

**Ejemplo para instalación local**:

```env
DATABASE_URL=postgresql+asyncpg://gxregistry:gxregistry123@localhost:5432/gxregistry_db
```

**Componentes**:
- `postgresql+asyncpg://` - Driver asíncrono
- `gxregistry` - Usuario de PostgreSQL
- `gxregistry123` - Contraseña del usuario
- `localhost` - Servidor (local)
- `5432` - Puerto de PostgreSQL
- `gxregistry_db` - Nombre de la base de datos

#### 2. SECRET_KEY

**Generar una clave segura**:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copia el resultado (ejemplo):

```
4zOvFwB0I_DDHXV-qmSeaKOzx1kavJ22q912k17fY08
```

Pégalo en `.env`:

```env
SECRET_KEY=4zOvFwB0I_DDHXV-qmSeaKOzx1kavJ22q912k17fY08
```

---

### Variables Opcionales (con Valores por Defecto)

```env
# APPLICATION
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO

# API
API_PREFIX=/api
API_VERSION=v1

# IMPORT
MAX_FILE_SIZE_MB=50
MAX_ERRORS_TO_REPORT=100
CSV_BATCH_SIZE=500

# JWT
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=365
```

### Archivo .env Completo (Ejemplo)

```env
# DATABASE
DATABASE_URL=postgresql+asyncpg://gxregistry:gxregistry123@localhost:5432/gxregistry_db
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# APPLICATION
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO

# SECURITY
SECRET_KEY=4zOvFwB0I_DDHXV-qmSeaKOzx1kavJ22q912k17fY08

# JWT
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=365
```

**Guarda el archivo** (`Ctrl + S`).

---

## 12. Configurar Base de Datos

Ahora crearemos la base de datos en PostgreSQL.

### Conectar a PostgreSQL

```bash
psql -U postgres -h localhost
```

Te pedirá la contraseña. Ingresa `postgres123` (o la que configuraste).

### Crear Usuario

Dentro de PostgreSQL (`postgres=#`), ejecuta:

```sql
CREATE USER gxregistry WITH PASSWORD 'gxregistry123';
```

Deberías ver:

```
CREATE ROLE
```

### Crear Base de Datos

```sql
CREATE DATABASE gxregistry_db OWNER gxregistry;
```

Deberías ver:

```
CREATE DATABASE
```

### Otorgar Privilegios

```sql
GRANT ALL PRIVILEGES ON DATABASE gxregistry_db TO gxregistry;
```

### Salir

```sql
\q
```

---

### Verificar Conexión como gxregistry

```bash
psql -U gxregistry -d gxregistry_db -h localhost
```

Contraseña: `gxregistry123`

Si te conectas:

```
gxregistry_db=>
```

✅ Base de datos configurada correctamente.

Sal con `\q`.

---

## 13. Ejecutar Migraciones

Las migraciones crean las tablas necesarias en la base de datos.

### ¿Qué son las Migraciones?

Son scripts que modifican el esquema de la base de datos de forma ordenada y versionada.

### Ver Estado Actual

```bash
alembic current
```

Deberías ver:

```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
```

(Vacío porque no hay migraciones aplicadas aún)

### Ver Historial de Migraciones

```bash
alembic history
```

Deberías ver:

```
<base> -> 001 (head), create_object_types_and_genexus_objects
001 -> 55adc69b9133, add_auth_system_and_created_by_fields
55adc69b9133 -> <next>, add_last_login_to_users
<next> -> <last>, add_must_change_password
```

### Ejecutar Migraciones

```bash
alembic upgrade head
```

**¿Qué hace este comando?**
- Aplica todas las migraciones pendientes
- Crea las tablas en la base de datos

Deberías ver:

```
INFO  [alembic.runtime.migration] Running upgrade  -> 001, create_object_types_and_genexus_objects
INFO  [alembic.runtime.migration] Running upgrade 001 -> 55adc69b9133, add_auth_system_and_created_by_fields
INFO  [alembic.runtime.migration] Running upgrade 55adc69b9133 -> <next>, add_last_login_to_users
INFO  [alembic.runtime.migration] Running upgrade <next> -> <last>, add_must_change_password
```

✅ Migraciones aplicadas correctamente.

### Verificar Tablas Creadas

```bash
psql -U gxregistry -d gxregistry_db -h localhost
```

```sql
\dt
```

Deberías ver:

```
               List of relations
 Schema |        Name         | Type  |   Owner
--------+---------------------+-------+------------
 public | alembic_version     | table | gxregistry
 public | genexus_objects     | table | gxregistry
 public | object_types        | table | gxregistry
 public | users               | table | gxregistry
```

✅ Tablas creadas.

Sal con `\q`.

---

### Problema: Alembic No Conecta a la Base de Datos

#### Error: Connection Refused

**Causa**: PostgreSQL no está corriendo.

**Solución**:

```bash
# Linux
sudo systemctl start postgresql

# macOS
brew services start postgresql@15

# Windows
# Abre "Servicios" y asegúrate de que PostgreSQL esté iniciado
```

#### Error: Authentication Failed

**Causa**: Contraseña incorrecta en `DATABASE_URL`.

**Solución**: Verifica que la contraseña en `.env` coincida con la contraseña del usuario `gxregistry`.

---

## 14. Crear Usuario Administrador

El sistema necesita al menos un usuario para poder acceder.

### Ejecutar Script de Creación

```bash
python scripts/create_admin.py
```

El script es **interactivo**. Te pedirá:

#### 1. Username

```
Ingresa el username: admin
```

#### 2. Email

```
Ingresa el email: admin@example.com
```

#### 3. Full Name

```
Ingresa el nombre completo (opcional): Administrador del Sistema
```

Puedes dejarlo vacío presionando `Enter`.

#### 4. Password

```
Ingresa la contraseña:
```

Escribe una contraseña segura (ej: `admin123`)

**⚠️ ANOTA ESTA CONTRASEÑA**

Verás:

```
✅ Usuario creado exitosamente
ID: 1
Username: admin
Email: admin@example.com
```

✅ Usuario administrador creado.

---

## 15. Cargar Datos Iniciales

Opcionalmente, puedes cargar tipos de objetos predefinidos.

### Ejecutar Seeder

```bash
python scripts/seed_database.py
```

Este script carga tipos como:
- PROCEDURE
- TRANSACTION
- WORK_PANEL
- WEB_PANEL
- DATA_PROVIDER
- etc.

Verás:

```
✅ Tipos de objetos creados exitosamente
```

---

## 16. Ejecutar el Proyecto en Desarrollo

Con todo configurado, inicia el servidor.

### Iniciar Servidor

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Parámetros**:
- `src.main:app` - Módulo y aplicación
- `--reload` - Reinicia automáticamente al detectar cambios
- `--host 0.0.0.0` - Permite acceso desde cualquier IP
- `--port 8000` - Puerto (8000 por defecto)

Deberías ver:

```
INFO:     Will watch for changes in these directories: ['C:\\Proyectos\\gx-object-registry']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [67890]
INFO:     Waiting for application startup.
[2026-08-01 10:00:00.000] Starting application app_env=development debug=True
INFO:     Application startup complete.
```

✅ **Servidor ejecutándose**

**No cierres esta terminal**. El servidor se mantiene corriendo aquí.

---

## 17. Verificar Instalación

### Acceder desde el Navegador

Abre tu navegador (Chrome, Firefox, Edge) y accede a:

**Interfaz Web**:
```
http://localhost:8000/web
```

Deberías ser redirigido a:

```
http://localhost:8000/web/login
```

✅ Página de login cargando correctamente.

---

### Iniciar Sesión

1. **Username**: `admin`
2. **Password**: `admin123` (o la que configuraste)
3. Click en **Iniciar Sesión**

Si todo está bien, serás redirigido al dashboard:

```
http://localhost:8000/web/
```

✅ **Sistema funcionando correctamente**

---

### Verificar API Docs

Accede a:

```
http://localhost:8000/docs
```

Deberías ver **Swagger UI** con toda la documentación de la API.

✅ API funcionando.

---

### Health Check

```
http://localhost:8000/health
```

Deberías ver:

```json
{"status":"healthy"}
```

---

### Detener el Servidor

En la terminal donde está corriendo Uvicorn, presiona:

```
Ctrl + C
```

Verás:

```
INFO:     Shutting down
INFO:     Finished server process [67890]
```

✅ Servidor detenido.

---

## 18. Solución de Problemas Comunes

### Problema 1: `ModuleNotFoundError: No module named 'fastapi'`

**Causa**: Dependencias no instaladas o entorno virtual no activado.

**Solución**:

1. Verifica que el entorno virtual esté activado (deberías ver `(venv)`).

```bash
# Si no está activado:
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

2. Instala dependencias:

```bash
pip install -r requirements.txt
```

---

### Problema 2: `psycopg2.OperationalError: could not connect to server`

**Causa**: PostgreSQL no está corriendo.

**Solución**:

```bash
# Linux
sudo systemctl start postgresql
sudo systemctl status postgresql

# macOS
brew services start postgresql@15

# Windows
# Servicios → PostgreSQL → Iniciar
```

---

### Problema 3: `alembic.util.exc.CommandError: Can't locate revision identified by`

**Causa**: Historial de migraciones corrupto.

**Solución**:

```bash
alembic downgrade base
alembic upgrade head
```

---

### Problema 4: `Port 8000 is already in use`

**Causa**: Otro proceso está usando el puerto 8000.

**Solución 1**: Usa otro puerto

```bash
uvicorn src.main:app --reload --port 8001
```

**Solución 2**: Encuentra y mata el proceso

```bash
# Linux/macOS
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

### Problema 5: `relation "users" does not exist`

**Causa**: Migraciones no ejecutadas.

**Solución**:

```bash
alembic upgrade head
```

---

### Problema 6: `Invalid signature` al hacer login

**Causa**: `SECRET_KEY` cambió después de generar el token.

**Solución**:

1. Limpia las cookies del navegador (`Ctrl + Shift + Delete`)
2. Vuelve a hacer login

---

### Problema 7: Uvicorn No Se Encuentra

**Causa**: Entorno virtual no activado.

**Solución**:

```bash
# Activar entorno virtual
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

---

### Problema 8: Error de Encoding al Importar CSV

**Causa**: Archivo CSV con encoding no UTF-8.

**Solución**:

El sistema detecta automáticamente el encoding. Si falla:

1. Abre el CSV en Excel/Notepad++
2. Guarda como UTF-8
3. Vuelve a importar

---

✅ **FIN DE LA PARTE 1: INSTALACIÓN LOCAL DESDE CERO**

Tu sistema debería estar funcionando en http://localhost:8000

Puedes empezar a desarrollar y usar la aplicación localmente.

---

# PARTE 2: DESPLIEGUE EN PRODUCCIÓN

---

## 19. Introducción al Despliegue

Esta sección cubre cómo desplegar GeneXus Object Registry en un **servidor de producción**.

### Objetivo

Tener el sistema accesible públicamente mediante:

```
https://tudominio.com
```

### Arquitectura de Producción

```
Internet
   ↓
Dominio (tudominio.com)
   ↓
Firewall (UFW)
   ↓
Nginx (Reverse Proxy + HTTPS)
   ↓
Gunicorn + Uvicorn Workers (Puerto 8000)
   ↓
FastAPI Application
   ↓
PostgreSQL (Puerto 5432)
```

### Requisitos Previos

1. ✅ Servidor Linux (Ubuntu 22.04 LTS recomendado)
2. ✅ Dominio registrado (ej: tudominio.com)
3. ✅ Acceso SSH al servidor
4. ✅ Usuario con privilegios sudo

### Qué Instalaremos

| Componente | Propósito |
|------------|-----------|
| **Git** | Clonar repositorio |
| **Python 3.11** | Runtime |
| **PostgreSQL 15** | Base de datos |
| **Gunicorn** | Servidor WSGI/ASGI |
| **Nginx** | Reverse proxy + HTTPS |
| **Certbot** | Certificados SSL gratuitos |
| **UFW** | Firewall |
| **systemd** | Gestionar servicio |

---

## 20. Preparar Servidor Linux (Ubuntu 22.04 LTS)

### Conectar al Servidor

```bash
ssh usuario@IP_DEL_SERVIDOR
```

Ejemplo:

```bash
ssh ubuntu@203.0.113.50
```

---

### Actualizar Sistema

```bash
sudo apt update
sudo apt upgrade -y
```

---

### Crear Usuario para la Aplicación

**⚠️ NO ejecutes la aplicación como root.**

```bash
sudo adduser gxapp
```

Te pedirá:
- Contraseña
- Información adicional (puedes dejarla en blanco)

Otorgar privilegios sudo:

```bash
sudo usermod -aG sudo gxapp
```

Cambiar a este usuario:

```bash
su - gxapp
```

---

## 21. Instalar Herramientas en el Servidor

### Instalar Dependencias del Sistema

```bash
sudo apt install -y build-essential libpq-dev python3.11 python3.11-venv python3.11-dev git nginx certbot python3-certbot-nginx ufw
```

**¿Qué instala cada paquete?**
- `build-essential`: Compiladores
- `libpq-dev`: Headers de PostgreSQL
- `python3.11`: Python
- `python3.11-venv`: Entornos virtuales
- `git`: Control de versiones
- `nginx`: Servidor web
- `certbot`: Certificados SSL
- `ufw`: Firewall

---

## 22. Configurar PostgreSQL en Producción

### Instalar PostgreSQL

```bash
sudo apt install postgresql postgresql-contrib -y
```

### Verificar que Esté Corriendo

```bash
sudo systemctl status postgresql
```

Deberías ver `active (running)`.

---

### Configurar PostgreSQL

```bash
sudo -u postgres psql
```

```sql
CREATE USER gxregistry WITH PASSWORD 'CONTRASEÑA_SEGURA_AQUI';
CREATE DATABASE gxregistry_db OWNER gxregistry;
GRANT ALL PRIVILEGES ON DATABASE gxregistry_db TO gxregistry;
\q
```

**⚠️ IMPORTANTE**:
- Usa una contraseña **diferente** a la de desarrollo
- Anota la contraseña, la necesitarás para `.env`

---

### Permitir Conexiones Locales

Edita:

```bash
sudo nano /etc/postgresql/15/main/pg_hba.conf
```

Asegúrate de que exista esta línea:

```
local   all             all                                     md5
```

Reinicia PostgreSQL:

```bash
sudo systemctl restart postgresql
```

---

## 23. Clonar y Configurar el Proyecto

### Clonar Repositorio

```bash
cd /home/gxapp
git clone <URL_DEL_REPOSITORIO>
cd gx-object-registry
```

---

### Crear Entorno Virtual

```bash
python3.11 -m venv venv
source venv/bin/activate
```

---

### Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

---

### Configurar .env para Producción

```bash
cp .env.example .env
nano .env
```

**Configuración de producción**:

```env
# DATABASE
DATABASE_URL=postgresql+asyncpg://gxregistry:CONTRASEÑA_SEGURA@localhost:5432/gxregistry_db
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# APPLICATION
APP_ENV=production
DEBUG=false
LOG_LEVEL=WARNING

# SECURITY
SECRET_KEY=<GENERA_UNA_CLAVE_NUEVA>

# JWT
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=365

# HOSTS
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
CORS_ORIGINS=https://tudominio.com
```

**Generar SECRET_KEY**:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Guarda el archivo (`Ctrl + O`, `Enter`, `Ctrl + X`).

---

### Ejecutar Migraciones

```bash
alembic upgrade head
```

---

### Crear Usuario Administrador

```bash
python scripts/create_admin.py
```

---

## 24. Configurar Gunicorn

Gunicorn es un servidor WSGI/ASGI para producción.

### Crear Archivo de Configuración

```bash
nano /home/gxapp/gx-object-registry/gunicorn_config.py
```

```python
import multiprocessing

# Bind
bind = "127.0.0.1:8000"

# Workers
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"

# Timeout
timeout = 120

# Logging
accesslog = "/home/gxapp/gx-object-registry/logs/access.log"
errorlog = "/home/gxapp/gx-object-registry/logs/error.log"
loglevel = "warning"

# Daemon
daemon = False
```

Guarda (`Ctrl + O`, `Enter`, `Ctrl + X`).

---

### Crear Carpeta de Logs

```bash
mkdir -p /home/gxapp/gx-object-registry/logs
```

---

### Probar Gunicorn Manualmente

```bash
cd /home/gxapp/gx-object-registry
source venv/bin/activate
gunicorn -c gunicorn_config.py src.main:app
```

Si ves:

```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://127.0.0.1:8000
```

✅ Gunicorn funcionando.

Detén con `Ctrl + C`.

---

## 25. Configurar systemd

systemd permitirá que la aplicación se ejecute como un servicio.

### Crear Archivo de Servicio

```bash
sudo nano /etc/systemd/system/gxregistry.service
```

```ini
[Unit]
Description=GeneXus Object Registry
After=network.target postgresql.service

[Service]
Type=notify
User=gxapp
Group=gxapp
WorkingDirectory=/home/gxapp/gx-object-registry
Environment="PATH=/home/gxapp/gx-object-registry/venv/bin"
ExecStart=/home/gxapp/gx-object-registry/venv/bin/gunicorn -c gunicorn_config.py src.main:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Guarda (`Ctrl + O`, `Enter`, `Ctrl + X`).

---

### Habilitar y Iniciar Servicio

```bash
sudo systemctl daemon-reload
sudo systemctl enable gxregistry
sudo systemctl start gxregistry
```

---

### Verificar Estado

```bash
sudo systemctl status gxregistry
```

Deberías ver:

```
● gxregistry.service - GeneXus Object Registry
   Loaded: loaded (/etc/systemd/system/gxregistry.service; enabled)
   Active: active (running) since ...
```

✅ Servicio corriendo.

---

### Ver Logs

```bash
sudo journalctl -u gxregistry -f
```

Presiona `Ctrl + C` para salir.

---

## 26. Configurar Nginx

Nginx actuará como reverse proxy y manejará HTTPS.

### Crear Configuración del Sitio

```bash
sudo nano /etc/nginx/sites-available/gxregistry
```

```nginx
server {
    listen 80;
    server_name tudominio.com www.tudominio.com;

    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Reemplaza**:
- `tudominio.com` por tu dominio real

Guarda (`Ctrl + O`, `Enter`, `Ctrl + X`).

---

### Habilitar Sitio

```bash
sudo ln -s /etc/nginx/sites-available/gxregistry /etc/nginx/sites-enabled/
```

---

### Probar Configuración

```bash
sudo nginx -t
```

Deberías ver:

```
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

---

### Reiniciar Nginx

```bash
sudo systemctl restart nginx
```

---

### Verificar

Abre tu navegador y accede a:

```
http://tudominio.com
```

Deberías ver la página de login del sistema.

✅ Nginx configurado correctamente.

---

## 27. Configurar HTTPS con Let's Encrypt

### Instalar Certbot

Ya lo instalamos anteriormente. Verificar:

```bash
certbot --version
```

---

### Obtener Certificado SSL

```bash
sudo certbot --nginx -d tudominio.com -d www.tudominio.com
```

Te pedirá:
1. **Email**: Para notificaciones de renovación
2. **Terms of Service**: Acepta (`Y`)
3. **Share email**: Opcional (`N` o `Y`)

Certbot configurará automáticamente Nginx para HTTPS.

Verás:

```
Congratulations! You have successfully enabled HTTPS on https://tudominio.com
```

---

### Verificar Configuración

Nginx ahora tendrá:

```nginx
server {
    listen 443 ssl;
    server_name tudominio.com www.tudominio.com;

    ssl_certificate /etc/letsencrypt/live/tudominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tudominio.com/privkey.pem;

    # ... resto de configuración
}

server {
    listen 80;
    server_name tudominio.com www.tudominio.com;
    return 301 https://$server_name$request_uri;
}
```

---

### Verificar HTTPS

Accede a:

```
https://tudominio.com
```

Deberías ver el **candado verde** en la barra de direcciones.

✅ HTTPS configurado correctamente.

---

### Renovación Automática

Certbot configura renovación automática. Verificar:

```bash
sudo systemctl status certbot.timer
```

Probar renovación:

```bash
sudo certbot renew --dry-run
```

---

## 28. Configurar Firewall

### Habilitar UFW

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

Confirma con `Y`.

---

### Verificar Estado

```bash
sudo ufw status
```

Deberías ver:

```
Status: active

To                         Action      From
--                         ------      ----
OpenSSH                    ALLOW       Anywhere
Nginx Full                 ALLOW       Anywhere
```

---

## 29. Actualizar el Sistema

### Proceso de Actualización

1. **Conectar al servidor**:

```bash
ssh gxapp@IP_DEL_SERVIDOR
```

2. **Ir al proyecto**:

```bash
cd /home/gxapp/gx-object-registry
```

3. **Activar entorno virtual**:

```bash
source venv/bin/activate
```

4. **Descargar cambios**:

```bash
git pull origin main
```

5. **Actualizar dependencias** (si cambiaron):

```bash
pip install -r requirements.txt
```

6. **Ejecutar migraciones** (si hay nuevas):

```bash
alembic upgrade head
```

7. **Reiniciar servicio**:

```bash
sudo systemctl restart gxregistry
```

8. **Verificar logs**:

```bash
sudo journalctl -u gxregistry -f
```

---

## 30. Backups y Recuperación

### Backup de Base de Datos

#### Crear Backup

```bash
pg_dump -U gxregistry -h localhost gxregistry_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

#### Automatizar Backups

Crear script:

```bash
nano /home/gxapp/backup.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/home/gxapp/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
pg_dump -U gxregistry -h localhost gxregistry_db > $BACKUP_DIR/backup_$DATE.sql
# Mantener solo últimos 7 días
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
```

Dar permisos:

```bash
chmod +x /home/gxapp/backup.sh
```

#### Programar con Cron

```bash
crontab -e
```

Agregar:

```cron
0 2 * * * /home/gxapp/backup.sh
```

(Ejecuta diariamente a las 2 AM)

---

### Restaurar Backup

```bash
psql -U gxregistry -d gxregistry_db < backup_20260801_020000.sql
```

---

## 31. Monitoreo y Logs

### Ver Logs de la Aplicación

```bash
# Logs del servicio
sudo journalctl -u gxregistry -f

# Logs de Gunicorn
tail -f /home/gxapp/gx-object-registry/logs/error.log

# Logs de Nginx
sudo tail -f /var/log/nginx/error.log
```

---

### Verificar Estado

```bash
sudo systemctl status gxregistry
sudo systemctl status nginx
sudo systemctl status postgresql
```

---

## 32. Checklist Final

### Instalación Local

```
✅ Git instalado
✅ Python 3.11+ instalado
✅ pip actualizado
✅ PostgreSQL instalado y corriendo
✅ Repositorio clonado
✅ Entorno virtual creado y activado
✅ Dependencias instaladas
✅ Archivo .env configurado
✅ Base de datos creada
✅ Migraciones ejecutadas
✅ Usuario administrador creado
✅ Datos iniciales cargados
✅ Servidor corriendo (uvicorn)
✅ Login funcionando en http://localhost:8000
```

---

### Producción

```
✅ Servidor Linux preparado
✅ Usuario gxapp creado
✅ Herramientas instaladas
✅ PostgreSQL configurado
✅ Proyecto clonado
✅ Variables de entorno configuradas
✅ Migraciones ejecutadas
✅ Usuario admin creado
✅ Gunicorn configurado
✅ systemd configurado y servicio corriendo
✅ Nginx configurado
✅ HTTPS configurado con Let's Encrypt
✅ Firewall configurado
✅ Backups automatizados
✅ Sistema accesible en https://tudominio.com
```

---

✅ **INSTALACIÓN Y DESPLIEGUE COMPLETADOS**

El sistema **GeneXus Object Registry** está ahora:
- ✅ Funcionando localmente para desarrollo
- ✅ Desplegado en producción con HTTPS
- ✅ Con backups automatizados
- ✅ Monitoreado y protegido

**Próximos Pasos**:
- Revisar documentación en `SYSTEM.md` para entender funcionalidades
- Consultar `COMMANDS.md` para comandos útiles
- Leer `TECHNOLOGIES.md` para detalles técnicos


---

# 33. Auditoría técnica del estado actual (sección normativa)

> Auditoría realizada sobre el árbol de trabajo el 1 de agosto de 2026. Si una sección anterior contradice esta, prevalece esta sección.

Se inspeccionaron `requirements.txt`, `.env.example`, Docker, Alembic, modelos, routers, plantillas, scripts y archivos BAT. La arquitectura real es:

```text
Navegador
   ↓ HTTP/HTTPS
Nginx (recomendado en producción; no incluido)
   ↓
Uvicorn + FastAPI :8000
   ├── /web   Jinja2 + HTML + JavaScript + Bootstrap CDN
   ├── /api   API REST + JWT
   ├── /docs  Swagger
   └── /health
   ↓ SQLAlchemy async + asyncpg
PostgreSQL 15 :5432
```

No hay frontend separado, Node.js, npm, build de frontend, `package.json`, Gunicorn instalado, configuración Nginx/systemd, ni CI/CD. API y web se levantan juntas. `requirements.txt` usa mínimos, no versiones exactas; no existe lockfile.

## Versiones verificables

| Requisito | Versión declarada | Obligatorio | Uso |
|---|---:|:---:|---|
| Python | 3.11+; Docker usa 3.11 | Sí fuera de Docker | Runtime |
| pip | No fijada | Sí fuera de Docker | Dependencias |
| PostgreSQL | 15+; Compose usa 15-alpine | Sí | Persistencia |
| Git | No fijada | Sí para clonar | Código |
| Docker/Compose | Sin mínimo fijado | No | Alternativa local |
| Navegador moderno | Sin versión fijada | Sí | Interfaz |
| Node/npm | No usados | No | No corresponde |

Dependencias directas: FastAPI >=0.109.0, Uvicorn >=0.27.0, SQLAlchemy >=2.0.25, asyncpg >=0.29.0, Alembic >=1.13.1, Pydantic >=2.5.3, pydantic-settings >=2.1.0, email-validator >=2.0.0, chardet >=5.2.0, structlog >=24.1.0, python-dotenv >=1.0.0, python-jose >=3.3.0, bcrypt >=4,<5 y las herramientas de prueba/calidad listadas en `requirements.txt`.

El código usa Jinja2, pero `jinja2` no está declarado directamente. Verificar con `python -c "import jinja2; print(jinja2.__version__)"`. Si falla, la corrección mantenible es agregar una versión probada a `requirements.txt`; como desbloqueo local: `python -m pip install jinja2`. No se inventa aquí una versión.

# 34. Instalación limpia resumida y exacta

En Windows instalar Git (git-scm.com), Python 3.11+ (marcar “Add python.exe to PATH”) y PostgreSQL 15+ (postgresql.org). Cerrar y reabrir PowerShell; verificar `git --version`, `py --version`, `py -m pip --version` y `psql --version`. Si `psql` no aparece, agregar `C:\Program Files\PostgreSQL\<versión>\bin` al PATH. Después:

```powershell
git clone https://github.com/HenryG77/gx-object-registry.git
Set-Location gx-object-registry
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Si PowerShell bloquea la activación: `Set-ExecutionPolicy -Scope Process RemoteSigned`. En CMD: `.venv\Scripts\activate.bat`.

Ubuntu/Debian:

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip postgresql postgresql-client
python3 --version # debe ser 3.11+
sudo systemctl enable --now postgresql
git clone https://github.com/HenryG77/gx-object-registry.git
cd gx-object-registry
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
chmod 600 .env
```

macOS con Homebrew:

```bash
xcode-select --install
brew install python@3.11 postgresql@15
brew services start postgresql@15
git clone https://github.com/HenryG77/gx-object-registry.git
cd gx-object-registry
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
chmod 600 .env
```

Nunca usar `sudo pip`. Si no se reconoce un comando, localizar su instalación, corregir PATH, cerrar y abrir terminal y repetir la verificación.

# 35. Variables: inventario completo

| Variable | Obligatoria | Predeterminado | Función |
|---|:---:|---|---|
| `DATABASE_URL` | Sí | ninguno | URL `postgresql+asyncpg://...` |
| `DATABASE_POOL_SIZE` | No | 20 | pool |
| `DATABASE_MAX_OVERFLOW` | No | 10 | conexiones extra |
| `APP_ENV` | No | development | etiqueta |
| `DEBUG` | No | true | debug/SQL/recarga en scripts |
| `LOG_LEVEL` | No | INFO | logs |
| `API_PREFIX` | No | /api | prefijo REST |
| `API_VERSION` | No | v1 | metadato, no URL |
| `API_TITLE`, `API_DESCRIPTION` | No | valores del proyecto | OpenAPI |
| `CORS_ORIGINS` | No | http://localhost:3000 | lista separada por comas |
| `MAX_FILE_SIZE_MB` | No | 50 | límite CSV |
| `MAX_ERRORS_TO_REPORT` | No | 100 | reporte |
| `CSV_BATCH_SIZE` | No | 500 | lote |
| `SECRET_KEY` | Sí en producción | valor inseguro | JWT |
| `ALLOWED_HOSTS` | No | localhost,127.0.0.1 | declarada, pero no aplicada |
| `ALGORITHM` | No | HS256 | JWT |
| `ACCESS_TOKEN_EXPIRE_DAYS` | No | 365 | expiración |

La plantilla omite las dos últimas. Generar SECRET_KEY con `python -c "import secrets; print(secrets.token_urlsafe(48))"`. Reiniciar tras editar. En producción usar DEBUG=false, origen HTTPS exacto, URL a 127.0.0.1 y secreto único. `ALLOWED_HOSTS` no instala middleware. La cookie usa `secure=False` fijo: debe cambiarse a `secure=True` antes de producción HTTPS.

# 36. PostgreSQL, migraciones y seed

En `psql -U postgres`:

```sql
CREATE ROLE gxuser WITH LOGIN PASSWORD ''CONTRASENA_UNICA'';
CREATE DATABASE gx_object_registry OWNER gxuser;
GRANT ALL PRIVILEGES ON DATABASE gx_object_registry TO gxuser;
\q
```

Verificar: `psql -h localhost -p 5432 -U gxuser -d gx_object_registry -c "SELECT current_database(), current_user;"`.

Comandos Alembic válidos:

```bash
alembic current
alembic history --verbose
alembic heads
alembic upgrade head
alembic downgrade -1
alembic revision --autogenerate -m "descripcion"
```

> ⚠️ Hallazgo bloqueante para bases nuevas: `001` crea IDs UUID; los modelos actuales los declaran Integer y `55adc69b9133` intenta alterarlos suponiendo INTEGER. Por ello `alembic upgrade head` no está garantizado desde una base vacía. Hay que reconciliar la cadena en código antes de afirmar que una instalación limpia funciona. En una base existente: backup, `\d object_types`, `\d genexus_objects`, migración explícita y ensayo sobre copia. No marcar `alembic_version` a mano.

Una vez corregido/verificado:

```bash
alembic upgrade head
python scripts/seed_database.py
python scripts/create_admin.py
```

El seeder crea 12 tipos y omite nombres existentes. No hay credenciales iniciales. `reset_password.py` cambia una contraseña. `reset_database.py`, `limpiar_datos.py`, `setup_completo.py` y `permitir_ids_manuales.py` son destructivos o legados y no representan con seguridad el esquema actual; nunca usarlos en producción sin revisión y backup.

# 37. Desarrollo y Docker

```bash
python start_app.py
# alternativa
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Comprobar `curl http://127.0.0.1:8000/health`, luego `http://localhost:8000/web/login`, `/docs` y `/redoc`. `/health` no consulta PostgreSQL. Detener con Ctrl+C. No existe variable PORT: para cambiarlo usar `--port 8001`.

Docker:

```bash
docker --version
docker compose version
docker compose config
docker compose up -d --build
docker compose ps
docker compose logs -f api
docker compose exec api alembic upgrade head
docker compose exec api python scripts/seed_database.py
docker compose exec api python scripts/create_admin.py
docker compose stop
docker compose down
```

> ⚠️ `docker compose down -v` elimina los datos. Compose es solo desarrollo: publica PostgreSQL, usa contraseña literal, monta código, activa reload/debug y no migra automáticamente.

# 38. Producción recomendada

Usar Ubuntu LTS que suministre Python 3.11+, PostgreSQL local, Uvicorn con systemd y Nginx. Gunicorn no está en dependencias; Uvicorn evita inventar una dependencia.

Unidad `/etc/systemd/system/gx-object-registry.service`:

```ini
[Unit]
Description=GeneXus Object Registry
After=network-online.target postgresql.service
Wants=network-online.target
[Service]
Type=simple
User=deploy
Group=deploy
WorkingDirectory=/opt/gx-object-registry
ExecStart=/opt/gx-object-registry/.venv/bin/uvicorn src.main:app --host 127.0.0.1 --port 8000 --workers 2
Restart=on-failure
RestartSec=5
PrivateTmp=true
NoNewPrivileges=true
[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now gx-object-registry
sudo systemctl status gx-object-registry
sudo journalctl -u gx-object-registry -f
```

Nginx:

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name app.ejemplo.com;
    client_max_body_size 50m;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Habilitar con symlink en `sites-enabled`, ejecutar `sudo nginx -t`, recargar y permitir “Nginx Full” en UFW. Crear DNS A hacia el VPS. HTTPS:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d app.ejemplo.com
sudo certbot renew --dry-run
systemctl status certbot.timer
```

No hay build frontend: Nginx proxyfica todo.

# 39. Actualizaciones, backups y recuperación

Antes de actualizar: guardar commit, backup y probar migraciones sobre copia.

```bash
pg_dump -Fc -h 127.0.0.1 -U gxregistry gx_object_registry > gx_object_registry_YYYYMMDD.dump
git status
git rev-parse HEAD
git fetch origin
source .venv/bin/activate
python -m pip install -r requirements.txt
alembic upgrade head
sudo systemctl restart gx-object-registry
curl https://app.ejemplo.com/health
sudo journalctl -u gx-object-registry -n 100 --no-pager
```

Restaurar primero en una base de prueba con `createdb gx_restore_test` y `pg_restore -d gx_restore_test archivo.dump`. Un rollback de código no revierte automáticamente el esquema. Guardar backups cifrados fuera del servidor con retención diaria/semanal/mensual y probar restauraciones. Nunca subir `.env`, dumps, claves, certificados, tokens ni cookies. `cookies.txt` existe y no está ignorado: revisar si contiene sesiones, retirarlo del intercambio y rotarlas.

# 40. Diagnóstico y checklist

| Error | Diagnóstico y solución |
|---|---|
| comando Python/Git/psql no reconocido | verificar instalación/PATH, reabrir terminal |
| pip no reconocido | usar `python -m pip`; `python -m ensurepip --upgrade` si aplica |
| ModuleNotFoundError | comprobar `sys.executable`, activar .venv, reinstalar |
| database_url required | crear .env en la raíz |
| connection refused | servicio, host, puerto, `pg_isready` |
| password authentication failed | probar psql y corregir URL/encoding |
| puerto 8000 ocupado | identificar PID o usar --port 8001 |
| UUID/INTEGER | aplicar advertencia de sección 36; no borrar datos |
| 401/Invalid signature | login, SECRET_KEY estable, usuario activo |
| CORS | origen exacto en CORS_ORIGINS y reinicio |
| 413 Nginx | alinear client_max_body_size |
| 502 Nginx | systemctl, journalctl, curl local, nginx -t |
| HTML sin estilos | comprobar acceso al CDN |
| Docker reinicia | `docker compose logs api` y estado de PostgreSQL |

Checklist final:

- [ ] Git, Python 3.11+, pip y PostgreSQL 15+ verificados.
- [ ] .venv activa y dependencias instaladas.
- [ ] Jinja2 comprobado.
- [ ] .env fuera de Git, DATABASE_URL válida y secreto único.
- [ ] Migraciones UUID/INTEGER reconciliadas y Alembic en head.
- [ ] Seeder y usuario inicial ejecutados; no hay credenciales por defecto.
- [ ] Login, API, páginas e importación probados.
- [ ] Producción con DEBUG=false, cookie Secure, Uvicorn sin reload y PostgreSQL no público.
- [ ] Nginx, DNS, HTTPS, firewall y renovación verificados.
- [ ] Backup/restauración y rollback ensayados.
- [ ] cookies.txt, secretos y dumps fuera del repositorio.

