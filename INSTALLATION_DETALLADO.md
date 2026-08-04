# Guía de Instalación Detallada - GeneXus Object Registry

**Versión del documento**: 1.0
**Fecha**: Agosto 2026
**Audiencia**: Desarrolladores principiantes e intermedios

---

## Tabla de Contenidos

### PARTE 1: INSTALACIÓN LOCAL (DESARROLLO)

1. [Introducción](#1-introducción)
2. [Requisitos del Sistema](#2-requisitos-del-sistema)
3. [Preparación del Sistema Operativo](#3-preparación-del-sistema-operativo)
4. [Instalación de Git](#4-instalación-de-git)
5. [Instalación de Python](#5-instalación-de-python)
6. [Instalación de PostgreSQL](#6-instalación-de-postgresql)
7. [Clonar el Repositorio](#7-clonar-el-repositorio)
8. [Crear Entorno Virtual](#8-crear-entorno-virtual)
9. [Configurar Variables de Entorno](#9-configurar-variables-de-entorno)
10. [Instalar Dependencias](#10-instalar-dependencias)
11. [Configurar Base de Datos](#11-configurar-base-de-datos)
12. [Ejecutar Migraciones](#12-ejecutar-migraciones)
13. [Cargar Datos Iniciales](#13-cargar-datos-iniciales)
14. [Crear Usuario Administrador](#14-crear-usuario-administrador)
15. [Iniciar el Servidor](#15-iniciar-el-servidor)
16. [Verificar Instalación](#16-verificar-instalación)
17. [Instalación con Docker (Alternativa)](#17-instalación-con-docker-alternativa)
18. [Solución de Problemas Comunes](#18-solución-de-problemas-comunes)

### PARTE 2: DESPLIEGUE EN PRODUCCIÓN

19. [Preparación del Servidor](#19-preparación-del-servidor)
20. [Configuración de PostgreSQL en Producción](#20-configuración-de-postgresql-en-producción)
21. [Instalación del Proyecto en Producción](#21-instalación-del-proyecto-en-producción)
22. [Configuración de Gunicorn](#22-configuración-de-gunicorn)
23. [Configuración de Systemd](#23-configuración-de-systemd)
24. [Instalación de Nginx](#24-instalación-de-nginx)
25. [Configuración de HTTPS](#25-configuración-de-https)
26. [Configuración de Firewall](#26-configuración-de-firewall)
27. [Backups Automáticos](#27-backups-automáticos)
28. [Monitoreo y Logs](#28-monitoreo-y-logs)
29. [Actualizaciones del Sistema](#29-actualizaciones-del-sistema)
30. [Checklist Final](#30-checklist-final)

---

# PARTE 1: INSTALACIÓN LOCAL (DESARROLLO)

---

## 1. Introducción

### ¿Qué es GeneXus Object Registry?

**GeneXus Object Registry** es un sistema web diseñado para administrar información básica sobre objetos de GeneXus. Permite registrar, buscar, actualizar y eliminar objetos de un proyecto GeneXus, así como importar grandes cantidades de objetos desde archivos CSV.

### Componentes del Sistema

El proyecto está compuesto por los siguientes componentes principales:

```
┌─────────────────────────────────────────────┐
│         NAVEGADOR WEB (Cliente)             │
│  - Interfaz web HTML/CSS/JavaScript         │
│  - Bootstrap 5 para estilos                 │
└─────────────────┬───────────────────────────┘
                  │
                  │ HTTP/HTTPS
                  │
┌─────────────────▼───────────────────────────┐
│         BACKEND (FastAPI + Python)          │
│  - API REST (FastAPI)                       │
│  - Lógica de negocio (casos de uso)         │
│  - Autenticación JWT                        │
│  - Validación con Pydantic                  │
└─────────────────┬───────────────────────────┘
                  │
                  │ SQLAlchemy (async)
                  │
┌─────────────────▼───────────────────────────┐
│       BASE DE DATOS (PostgreSQL)            │
│  - Almacenamiento persistente               │
│  - Tablas: users, object_types,             │
│    genexus_objects                          │
└─────────────────────────────────────────────┘
```

### Tecnologías Utilizadas

| Tecnología | Versión Requerida | Propósito |
|------------|-------------------|-----------|
| **Python** | 3.11 o superior | Lenguaje de programación backend |
| **FastAPI** | 0.109.0+ | Framework web para crear la API REST |
| **PostgreSQL** | 15 o superior | Base de datos relacional |
| **SQLAlchemy** | 2.0.25+ | ORM asíncrono para acceso a datos |
| **Alembic** | 1.13.1+ | Sistema de migraciones de base de datos |
| **Pydantic** | 2.5.3+ | Validación de datos y DTOs |
| **Uvicorn** | 0.27.0+ | Servidor ASGI para FastAPI |
| **bcrypt** | 4.0.0 - 4.9.9 | Hash de contraseñas |
| **python-jose** | 3.3.0+ | Generación y verificación de tokens JWT |

### Arquitectura del Proyecto

El proyecto sigue los principios de **Clean Architecture** (Arquitectura Limpia):

```
src/
├── auth/                      # Módulo de autenticación
│   ├── domain/               # Entidades y reglas de negocio
│   ├── application/          # Casos de uso
│   ├── infrastructure/       # Implementaciones (BD, JWT)
│   └── presentation/         # API REST (routers, DTOs)
│
├── object_types/             # Módulo de tipos de objetos
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── presentation/
│
├── genexus_objects/          # Módulo de objetos GeneXus
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── presentation/
│
├── imports/                  # Módulo de importación CSV
│   ├── domain/
│   ├── application/
│   └── presentation/
│
├── web/                      # Interfaz web (templates HTML)
│   ├── templates/
│   └── router.py
│
└── shared/                   # Componentes compartidos
    ├── config/              # Configuración
    ├── database/            # Conexión a BD
    ├── errors/              # Manejo de errores
    └── logging/             # Sistema de logs
```

### Sistemas Operativos Compatibles

Este proyecto puede ejecutarse en:

- ✅ **Windows** 10/11 (64-bit)
- ✅ **Ubuntu** 20.04 LTS / 22.04 LTS / 24.04 LTS
- ✅ **Debian** 11 / 12
- ✅ **macOS** 12 (Monterey) o superior
- ✅ **Otras distribuciones Linux** (con adaptaciones menores)

### ¿Qué se Instalará Durante el Proceso?

Durante la instalación local, instalarás:

1. **Git** - Sistema de control de versiones
2. **Python 3.11+** - Runtime del lenguaje
3. **pip** - Gestor de paquetes de Python
4. **PostgreSQL 15+** - Sistema de base de datos
5. **Entorno virtual Python** - Aislamiento de dependencias
6. **22 paquetes Python** - Definidos en [requirements.txt](requirements.txt)

### ¿Qué se Configurará?

1. Variables de entorno (archivo `.env`)
2. Conexión a base de datos PostgreSQL
3. Usuario y base de datos en PostgreSQL
4. Migraciones de esquema de base de datos
5. Datos iniciales (tipos de objetos GeneXus)
6. Usuario administrador inicial

### ¿Qué Servicios se Levantarán?

En **desarrollo**:
- PostgreSQL (puerto 5432)
- Uvicorn (servidor ASGI en puerto 8000)

En **producción**:
- PostgreSQL (puerto 5432)
- Gunicorn + Uvicorn workers (puerto 8000)
- Nginx (puerto 80/443 como proxy inverso)
- Systemd (gestión del proceso)

### Flujo General de Instalación

```
1. Sistema Operativo
        ↓
2. Instalar Git
        ↓
3. Instalar Python 3.11+
        ↓
4. Instalar PostgreSQL 15+
        ↓
5. Clonar repositorio
        ↓
6. Crear entorno virtual
        ↓
7. Activar entorno virtual
        ↓
8. Instalar dependencias (pip)
        ↓
9. Configurar .env
        ↓
10. Crear base de datos PostgreSQL
        ↓
11. Ejecutar migraciones (Alembic)
        ↓
12. Cargar datos iniciales (seed)
        ↓
13. Crear usuario administrador
        ↓
14. Iniciar servidor (Uvicorn)
        ↓
15. Acceder desde navegador
```

### Tiempo Estimado de Instalación

- **Primera instalación completa**: No aplica (depende del usuario)
- **Reinstalación con herramientas ya instaladas**: No aplica (depende del usuario)

---

## 2. Requisitos del Sistema

### Tabla de Requisitos Completa

| Requisito | Versión Mínima | Versión Recomendada | Obligatorio | Uso |
|-----------|----------------|---------------------|-------------|-----|
| **Sistema Operativo** | Windows 10, Ubuntu 20.04, macOS 12 | Windows 11, Ubuntu 22.04 LTS, macOS 14 | ✅ Sí | Sistema base |
| **Python** | 3.11.0 | 3.11.x o 3.12.x | ✅ Sí | Runtime de la aplicación |
| **pip** | 23.0 | Última versión | ✅ Sí | Gestor de paquetes Python |
| **PostgreSQL** | 15.0 | 15.x o 16.x | ✅ Sí | Base de datos |
| **Git** | 2.30 | Última versión | ✅ Sí | Control de versiones |
| **Docker** | 20.10 | Última versión | ❌ No (opcional) | Contenedorización |
| **Docker Compose** | 2.0 | Última versión | ❌ No (opcional) | Orquestación de contenedores |
| **RAM** | 2 GB | 4 GB o más | ✅ Sí | Memoria del sistema |
| **Espacio en disco** | 1 GB | 5 GB o más | ✅ Sí | Almacenamiento |
| **Navegador web** | Chrome 90+, Firefox 88+, Edge 90+ | Última versión | ✅ Sí | Interfaz de usuario |

### Notas Importantes

**Sobre Python**:
- **NO** usar Python 3.9 o inferior (incompatible con algunas dependencias)
- **NO** usar Python 3.13+ aún (puede tener incompatibilidades con bcrypt)
- ✅ **RECOMENDADO**: Python 3.11.x (versión probada)

**Sobre PostgreSQL**:
- **NO** usar MySQL, MariaDB, SQLite u otras bases de datos
- El proyecto utiliza características específicas de PostgreSQL
- Se requiere soporte para async con `asyncpg`

**Sobre el Sistema Operativo**:
- Windows requiere versión de 64 bits
- En Linux se recomienda Ubuntu por facilidad de instalación
- macOS requiere Homebrew para instalar PostgreSQL fácilmente

---

## 3. Preparación del Sistema Operativo

Antes de instalar cualquier herramienta, verificaremos el estado actual del sistema.

### Windows 10/11

#### Verificar Versión de Windows

1. Presiona `Windows + R`
2. Escribe `winver` y presiona Enter
3. Verifica que sea Windows 10 (build 19041+) o Windows 11

#### Actualizar Windows

1. Abre **Configuración** (`Windows + I`)
2. Ve a **Windows Update**
3. Haz clic en **Buscar actualizaciones**
4. Instala todas las actualizaciones pendientes
5. Reinicia si es necesario

#### Habilitar Ejecución de Scripts (PowerShell)

Algunos comandos requieren PowerShell. Para verificar:

1. Abre **PowerShell** como administrador:
   - Presiona `Windows + X`
   - Selecciona **Windows PowerShell (Administrador)** o **Terminal (Administrador)**

2. Ejecuta:
   ```powershell
   Get-ExecutionPolicy
   ```

3. Si muestra `Restricted`, ejecuta:
   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   - Confirma con `Y` (Yes)

#### Instalar Windows Terminal (Opcional pero Recomendado)

Windows Terminal ofrece una mejor experiencia de línea de comandos:

1. Abre **Microsoft Store**
2. Busca **Windows Terminal**
3. Haz clic en **Obtener** / **Instalar**
4. Una vez instalado, úsalo en lugar de CMD

### Ubuntu / Debian

#### Verificar Versión de Ubuntu

```bash
lsb_release -a
```

**Salida esperada**:
```
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 22.04.3 LTS
Release:        22.04
Codename:       jammy
```

#### Actualizar Sistema

```bash
sudo apt update
sudo apt upgrade -y
```

**Qué hace cada comando**:
- `apt update`: Actualiza la lista de paquetes disponibles
- `apt upgrade`: Instala las versiones más recientes de los paquetes

**Si aparece un error de permisos**:
```
E: Could not open lock file /var/lib/dpkg/lock-frontend
```

**Solución**:
1. Asegúrate de usar `sudo`
2. Si el problema persiste, otro proceso está usando apt. Espera o reinicia

#### Instalar Herramientas Básicas

```bash
sudo apt install -y curl wget software-properties-common build-essential
```

**Qué instala**:
- `curl`: Herramienta para transferir datos
- `wget`: Descarga de archivos
- `software-properties-common`: Gestión de repositorios
- `build-essential`: Compiladores C/C++ (necesarios para algunas dependencias Python)

### macOS

#### Verificar Versión de macOS

1. Haz clic en el menú Apple (esquina superior izquierda)
2. Selecciona **Acerca de este Mac**
3. Verifica que sea macOS 12 (Monterey) o superior

#### Instalar Homebrew

Homebrew es el gestor de paquetes para macOS. Es **esencial** para instalar Python y PostgreSQL.

**Verificar si ya está instalado**:
```bash
brew --version
```

**Si muestra la versión**, ya está instalado. Pasa a la siguiente sección.

**Si NO está instalado**:

1. Abre **Terminal** (Aplicaciones → Utilidades → Terminal)

2. Ejecuta:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. El script pedirá tu contraseña de macOS
4. Confirma la instalación presionando Enter
5. Espera a que termine (puede tardar varios minutos)

6. **IMPORTANTE**: Al finalizar, Homebrew mostrará comandos que debes ejecutar. Ejemplo:
   ```bash
   echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
   eval "$(/opt/homebrew/bin/brew shellenv)"
   ```

   **Copia y ejecuta esos comandos exactamente como aparecen**

7. Cierra y vuelve a abrir Terminal

8. Verifica:
   ```bash
   brew --version
   ```

   **Salida esperada**:
   ```
   Homebrew 4.x.x
   ```

#### Actualizar Homebrew

```bash
brew update
brew upgrade
```

---

## 4. Instalación de Git

Git es necesario para clonar el repositorio del proyecto.

### Windows

#### Verificar si Git está instalado

Abre **PowerShell** o **CMD** y ejecuta:

```cmd
git --version
```

**Si muestra la versión** (ejemplo: `git version 2.41.0`), Git ya está instalado. Pasa a la [sección 5](#5-instalación-de-python).

**Si aparece**: `'git' is not recognized as an internal or external command`

Git **NO** está instalado. Continúa con la instalación.

#### Descargar Git

1. Ve a: https://git-scm.com/download/win
2. La descarga debería iniciar automáticamente
3. Si no, haz clic en **Click here to download manually**
4. Descarga el instalador de 64 bits

#### Instalar Git

1. Ejecuta el archivo descargado (`Git-2.x.x-64-bit.exe`)
2. En la pantalla de instalación, usa estas configuraciones:

   - **Select Components**: Deja las opciones por defecto
   - **Default editor**: Selecciona tu editor preferido (puedes dejar Vim)
   - **Adjusting your PATH environment**: Selecciona **Git from the command line and also from 3rd-party software** (opción recomendada)
   - **Choosing HTTPS transport backend**: Usa **Use the OpenSSL library**
   - **Configuring the line ending conversions**: Usa **Checkout Windows-style, commit Unix-style line endings**
   - **Configuring the terminal emulator**: Usa **Use MinTTY**
   - Resto de opciones: Deja valores por defecto

3. Haz clic en **Install**
4. Espera a que termine
5. Haz clic en **Finish**

#### Verificar Instalación

1. **CIERRA** PowerShell o CMD completamente
2. **ABRE** PowerShell o CMD nuevamente
3. Ejecuta:
   ```cmd
   git --version
   ```

**Salida esperada**:
```
git version 2.41.0.windows.1
```

**Si aún aparece el error** `'git' is not recognized`:
- Reinicia tu computadora
- Abre PowerShell nuevamente
- Intenta de nuevo

#### Configurar Git (Primera vez)

```cmd
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

**Reemplaza**:
- `"Tu Nombre"` con tu nombre real
- `"tu@email.com"` con tu email

**Verificar configuración**:
```cmd
git config --global --list
```

**Salida esperada**:
```
user.name=Tu Nombre
user.email=tu@email.com
```

### Ubuntu / Debian

#### Verificar si Git está instalado

```bash
git --version
```

**Si muestra la versión**, Git ya está instalado. Pasa a la [sección 5](#5-instalación-de-python).

**Si aparece**: `command not found`

Git **NO** está instalado. Continúa con la instalación.

#### Instalar Git

```bash
sudo apt update
sudo apt install -y git
```

#### Verificar Instalación

```bash
git --version
```

**Salida esperada**:
```
git version 2.34.1
```

#### Configurar Git

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

**Verificar**:
```bash
git config --global --list
```

### macOS

#### Verificar si Git está instalado

```bash
git --version
```

**Si muestra la versión**, Git ya está instalado. Pasa a la [sección 5](#5-instalación-de-python).

**Si aparece un diálogo pidiendo instalar Command Line Tools**:
- Haz clic en **Instalar**
- Acepta los términos
- Espera a que termine
- Ejecuta `git --version` nuevamente

**Si aparece**: `command not found`

Instala Git con Homebrew.

#### Instalar Git con Homebrew

```bash
brew install git
```

#### Verificar Instalación

```bash
git --version
```

**Salida esperada**:
```
git version 2.41.0
```

#### Configurar Git

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

**Verificar**:
```bash
git config --global --list
```

---

## 5. Instalación de Python

El proyecto requiere **Python 3.11 o superior**.

### Windows

#### Verificar si Python está instalado

Abre PowerShell y ejecuta:

```cmd
python --version
```

**También prueba**:
```cmd
python3 --version
py --version
py -3 --version
```

**Si muestra** `Python 3.11.x` o `Python 3.12.x`, Python ya está instalado correctamente.

**Verifica que pip esté disponible**:
```cmd
python -m pip --version
```

**Si ambos funcionan**, pasa a la [sección 6](#6-instalación-de-postgresql).

**Si NO está instalado o la versión es menor a 3.11**, continúa con la instalación.

#### Descargar Python

1. Ve a: https://www.python.org/downloads/
2. Haz clic en **Download Python 3.11.x** (o la versión 3.11 más reciente)
3. Descarga el instalador para Windows (64-bit)

**IMPORTANTE**: No descargues Python 3.13 aún (puede tener incompatibilidades).

#### Instalar Python

1. Ejecuta el instalador descargado
2. **MUY IMPORTANTE**: ✅ **Marca la casilla** `Add Python 3.11 to PATH` (abajo del todo)
3. Haz clic en **Install Now**
4. Espera a que termine
5. Haz clic en **Close**

#### Verificar Instalación

1. **CIERRA** PowerShell completamente
2. **ABRE** PowerShell nuevamente
3. Ejecuta:
   ```cmd
   python --version
   ```

**Salida esperada**:
```
Python 3.11.7
```

**Si aún no funciona**, prueba:
```cmd
py --version
```

**En Windows, puedes usar** `py` en lugar de `python` para todos los comandos.

#### Verificar pip

```cmd
python -m pip --version
```

**Salida esperada**:
```
pip 23.x.x from ... (python 3.11)
```

**Si pip NO está instalado**:
```cmd
python -m ensurepip --upgrade
```

#### Actualizar pip

```cmd
python -m pip install --upgrade pip
```

### Ubuntu / Debian

#### Verificar versión de Python

```bash
python3 --version
```

**Si muestra** `Python 3.11.x` o superior, Python ya está instalado. Pasa a verificar pip.

**Si muestra** `Python 3.10.x` o inferior, necesitas instalar Python 3.11.

#### Instalar Python 3.11 en Ubuntu 22.04

```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev
```

**Verificar**:
```bash
python3.11 --version
```

**Salida esperada**:
```
Python 3.11.4
```

**Crear alias (opcional)**:

Para usar `python3` en lugar de `python3.11`:

```bash
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
```

#### Verificar pip

```bash
python3.11 -m pip --version
```

**Si pip NO está instalado**:
```bash
sudo apt install -y python3-pip
```

**O instala pip para Python 3.11 específicamente**:
```bash
python3.11 -m ensurepip --upgrade
```

#### Actualizar pip

```bash
python3.11 -m pip install --upgrade pip
```

### macOS

#### Verificar versión de Python

```bash
python3 --version
```

**Si muestra** `Python 3.11.x` o `Python 3.12.x`, Python ya está instalado. Pasa a verificar pip.

**Si NO está instalado o es una versión antigua**, instala Python con Homebrew.

#### Instalar Python con Homebrew

```bash
brew install python@3.11
```

**Nota**: Homebrew puede instalar la versión más reciente (3.12). Eso está bien.

#### Verificar Instalación

```bash
python3 --version
```

**Salida esperada**:
```
Python 3.11.7
```

#### Verificar pip

```bash
python3 -m pip --version
```

**Si pip NO está disponible**:
```bash
python3 -m ensurepip --upgrade
```

#### Actualizar pip

```bash
python3 -m pip install --upgrade pip
```

---

## 6. Instalación de PostgreSQL

PostgreSQL es la base de datos utilizada por el proyecto. Requieres **PostgreSQL 15 o superior**.

### Windows

#### Verificar si PostgreSQL está instalado

Abre PowerShell y ejecuta:

```cmd
psql --version
```

**Si muestra la versión** (ejemplo: `psql (PostgreSQL) 15.3`), PostgreSQL ya está instalado. Pasa a [verificar el servicio](#verificar-servicio-postgresql-windows).

**Si aparece**: `'psql' is not recognized`

PostgreSQL **NO** está instalado o no está en el PATH.

#### Descargar PostgreSQL

1. Ve a: https://www.postgresql.org/download/windows/
2. Haz clic en **Download the installer**
3. Esto te redirige a EnterpriseDB
4. Descarga **PostgreSQL 15.x** para Windows x86-64

**Archivo descargado**: `postgresql-15.x-windows-x64.exe`

#### Instalar PostgreSQL

1. Ejecuta el instalador descargado
2. Haz clic en **Next**

**Select Installation Directory**:
- Deja la ruta por defecto: `C:\Program Files\PostgreSQL\15`
- Haz clic en **Next**

**Select Components**:
- ✅ PostgreSQL Server
- ✅ pgAdmin 4 (herramienta gráfica)
- ✅ Stack Builder (opcional)
- ✅ Command Line Tools
- Haz clic en **Next**

**Data Directory**:
- Deja por defecto: `C:\Program Files\PostgreSQL\15\data`
- Haz clic en **Next**

**Password**:
- **MUY IMPORTANTE**: Ingresa una contraseña para el usuario `postgres`
- **Anota esta contraseña** (la necesitarás más adelante)
- Ejemplo: `postgres123` (cámbiala por una más segura)
- Confirma la contraseña
- Haz clic en **Next**

**Port**:
- Deja el puerto por defecto: **5432**
- **Si el puerto está ocupado**, usa **5433** o **5434**
- Haz clic en **Next**

**Locale**:
- Deja por defecto (Default locale)
- Haz clic en **Next**

**Pre Installation Summary**:
- Revisa la configuración
- Haz clic en **Next**

3. Espera a que termine la instalación
4. **Desmarca** "Launch Stack Builder at exit" (no es necesario)
5. Haz clic en **Finish**

#### Verificar Instalación

1. **CIERRA** PowerShell completamente
2. **ABRE** PowerShell nuevamente
3. Ejecuta:
   ```cmd
   psql --version
   ```

**Salida esperada**:
```
psql (PostgreSQL) 15.3
```

**Si aún aparece** `'psql' is not recognized`:

**Agregar PostgreSQL al PATH manualmente**:

1. Presiona `Windows + R`
2. Escribe `sysdm.cpl` y presiona Enter
3. Ve a la pestaña **Opciones avanzadas**
4. Haz clic en **Variables de entorno**
5. En **Variables del sistema**, busca `Path` y haz doble clic
6. Haz clic en **Nuevo**
7. Agrega: `C:\Program Files\PostgreSQL\15\bin`
8. Haz clic en **Aceptar** en todas las ventanas
9. **REINICIA** PowerShell
10. Intenta de nuevo: `psql --version`

#### Verificar Servicio PostgreSQL (Windows)

PostgreSQL debe estar corriendo como servicio.

**Verificar estado**:

1. Presiona `Windows + R`
2. Escribe `services.msc` y presiona Enter
3. Busca **postgresql-x64-15**
4. El estado debe ser **En ejecución (Running)**

**Si NO está en ejecución**:
- Haz clic derecho sobre el servicio
- Selecciona **Iniciar**

**Iniciar/Detener PostgreSQL desde CMD**:

```cmd
# Iniciar
net start postgresql-x64-15

# Detener
net stop postgresql-x64-15

# Ver estado
sc query postgresql-x64-15
```

#### Conectar a PostgreSQL

```cmd
psql -U postgres
```

**Te pedirá la contraseña** que configuraste durante la instalación.

**Salida esperada**:
```
psql (15.3)
Type "help" for help.

postgres=#
```

**Comandos básicos de psql**:
- `\l` - Listar bases de datos
- `\du` - Listar usuarios
- `\q` - Salir de psql

**Sal de psql**:
```sql
\q
```

### Ubuntu / Debian

#### Verificar si PostgreSQL está instalado

```bash
psql --version
```

**Si muestra la versión** (ejemplo: `psql (PostgreSQL) 15.4`), PostgreSQL está instalado. Pasa a [verificar el servicio](#verificar-servicio-postgresql-ubuntu).

**Si aparece**: `command not found`

PostgreSQL **NO** está instalado.

#### Instalar PostgreSQL 15

**En Ubuntu 22.04 o superior**:

```bash
sudo apt update
sudo apt install -y postgresql-15 postgresql-contrib-15
```

**En Ubuntu 20.04 (requiere repositorio adicional)**:

```bash
# Agregar repositorio oficial de PostgreSQL
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

# Importar clave GPG
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# Actualizar e instalar
sudo apt update
sudo apt install -y postgresql-15 postgresql-contrib-15
```

#### Verificar Instalación

```bash
psql --version
```

**Salida esperada**:
```
psql (PostgreSQL) 15.4 (Ubuntu 15.4-1.pgdg22.04+1)
```

#### Verificar Servicio PostgreSQL (Ubuntu)

```bash
sudo systemctl status postgresql
```

**Salida esperada**:
```
● postgresql.service - PostgreSQL RDBMS
     Loaded: loaded
     Active: active (exited) since ...
```

**Si el servicio NO está activo**:

```bash
# Iniciar PostgreSQL
sudo systemctl start postgresql

# Habilitar inicio automático
sudo systemctl enable postgresql

# Verificar estado nuevamente
sudo systemctl status postgresql
```

**Comandos útiles**:

```bash
# Iniciar
sudo systemctl start postgresql

# Detener
sudo systemctl stop postgresql

# Reiniciar
sudo systemctl restart postgresql

# Ver logs
sudo journalctl -u postgresql -f
```

#### Conectar a PostgreSQL

En Ubuntu, el usuario `postgres` se crea automáticamente sin contraseña inicial.

**Conectar como usuario postgres**:

```bash
sudo -u postgres psql
```

**Salida esperada**:
```
psql (15.4)
Type "help" for help.

postgres=#
```

**Sal de psql**:
```sql
\q
```

#### Configurar Contraseña para postgres (Opcional)

Si quieres configurar una contraseña para el usuario `postgres`:

```bash
sudo -u postgres psql
```

Dentro de psql:
```sql
ALTER USER postgres WITH PASSWORD 'tu_contraseña_segura';
\q
```

### macOS

#### Verificar si PostgreSQL está instalado

```bash
psql --version
```

**Si muestra la versión**, PostgreSQL está instalado. Pasa a [verificar el servicio](#verificar-servicio-postgresql-macos).

**Si aparece**: `command not found`

PostgreSQL **NO** está instalado.

#### Instalar PostgreSQL con Homebrew

```bash
brew install postgresql@15
```

**Espera a que termine la instalación** (puede tardar varios minutos).

#### Agregar PostgreSQL al PATH

Homebrew muestra instrucciones al finalizar. Generalmente son:

```bash
echo 'export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Si usas bash en lugar de zsh**:
```bash
echo 'export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

#### Verificar Instalación

```bash
psql --version
```

**Salida esperada**:
```
psql (PostgreSQL) 15.4
```

#### Verificar Servicio PostgreSQL (macOS)

**Iniciar PostgreSQL**:

```bash
brew services start postgresql@15
```

**Verificar estado**:

```bash
brew services list
```

**Salida esperada**:
```
Name          Status  User    File
postgresql@15 started tu_user ~/Library/LaunchAgents/homebrew...
```

**Comandos útiles**:

```bash
# Iniciar
brew services start postgresql@15

# Detener
brew services stop postgresql@15

# Reiniciar
brew services restart postgresql@15
```

#### Conectar a PostgreSQL

```bash
psql postgres
```

**Salida esperada**:
```
psql (15.4)
Type "help" for help.

postgres=#
```

**Sal de psql**:
```sql
\q
```

---

## 7. Clonar el Repositorio

Ahora descargaremos el código fuente del proyecto desde el repositorio Git.

### Elegir Ubicación para el Proyecto

**Recomendaciones por sistema operativo**:

**Windows**:
- `C:\Users\TuUsuario\Proyectos\`
- `C:\dev\`
- `D:\Proyectos\` (si tienes otro disco)

**Ubuntu/Linux**:
- `~/proyectos/`
- `~/dev/`
- `/opt/` (requiere permisos)

**macOS**:
- `~/proyectos/`
- `~/dev/`
- `~/Documents/proyectos/`

### Crear Carpeta de Proyectos

**Windows** (PowerShell):
```cmd
mkdir C:\Users\TuUsuario\Proyectos
cd C:\Users\TuUsuario\Proyectos
```

**Reemplaza** `TuUsuario` con tu nombre de usuario real.

**Linux/macOS**:
```bash
mkdir -p ~/proyectos
cd ~/proyectos
```

### Clonar el Repositorio

**IMPORTANTE**: Necesitas la URL del repositorio. Puede ser:
- HTTPS: `https://github.com/usuario/gx-object-registry.git`
- SSH: `git@github.com:usuario/gx-object-registry.git`

**Para este ejemplo**, asumimos que tienes el repositorio localmente o una URL válida.

**Clonar con HTTPS**:

```bash
git clone https://github.com/USUARIO/gx-object-registry.git
```

**Reemplaza** `USUARIO` con el usuario/organización real del repositorio.

**Si el repositorio es privado**, Git pedirá tus credenciales:
- **Username**: Tu usuario de GitHub
- **Password**: Tu token de acceso personal (NO tu contraseña de GitHub)

**Cómo obtener un token**:
1. Ve a GitHub → Settings → Developer settings → Personal access tokens
2. Genera un nuevo token con permisos `repo`
3. Copia el token y úsalo como contraseña

**Salida esperada durante la clonación**:
```
Cloning into 'gx-object-registry'...
remote: Enumerating objects: 500, done.
remote: Counting objects: 100% (500/500), done.
remote: Compressing objects: 100% (300/300), done.
Receiving objects: 100% (500/500), 1.5 MiB | 2.00 MiB/s, done.
Resolving deltas: 100% (200/200), done.
```

### Entrar al Proyecto

```bash
cd gx-object-registry
```

### Verificar Contenido del Proyecto

**Windows**:
```cmd
dir
```

**Linux/macOS**:
```bash
ls -la
```

**Deberías ver estos archivos/carpetas**:
```
.env.example
.git/
.gitignore
alembic/
alembic.ini
docker-compose.yml
Dockerfile
README.md
requirements.txt
scripts/
src/
tests/
```

**Si NO ves estos archivos**:
- Verifica que estés en la carpeta correcta: `cd gx-object-registry`
- Verifica que la clonación fue exitosa

---

## 8. Crear Entorno Virtual

Un **entorno virtual** (virtual environment) aísla las dependencias de Python de este proyecto de otros proyectos en tu sistema.

**Ventajas**:
- Evita conflictos entre versiones de paquetes
- Puedes tener diferentes proyectos con diferentes versiones de dependencias
- No contaminas la instalación global de Python

### ¿Qué es un entorno virtual?

Es una carpeta que contiene:
- Una copia de Python
- pip (gestor de paquetes)
- Todas las dependencias instaladas para este proyecto

### Verificar que estás en la carpeta del proyecto

**Antes de crear el entorno virtual**, asegúrate de estar dentro de `gx-object-registry`:

**Windows**:
```cmd
cd
```

**Linux/macOS**:
```bash
pwd
```

**Deberías ver algo como**:
- Windows: `C:\Users\TuUsuario\Proyectos\gx-object-registry`
- Linux/macOS: `/home/usuario/proyectos/gx-object-registry`

### Crear Entorno Virtual

#### Windows

```cmd
python -m venv venv
```

**O si usas** `py`:
```cmd
py -m venv venv
```

**Qué hace este comando**:
- `python -m venv`: Ejecuta el módulo `venv` de Python
- `venv`: Nombre de la carpeta del entorno virtual (puedes usar otro nombre, pero `venv` es el estándar)

**Salida esperada**:
- No muestra nada, pero crea una carpeta `venv/`

**Verificar que se creó**:
```cmd
dir venv
```

Deberías ver carpetas como: `Include`, `Lib`, `Scripts`

#### Linux/macOS

```bash
python3 -m venv venv
```

**O con Python 3.11 específicamente**:
```bash
python3.11 -m venv venv
```

**Verificar que se creó**:
```bash
ls venv/
```

Deberías ver carpetas como: `bin`, `include`, `lib`

### Activar Entorno Virtual

**IMPORTANTE**: Debes activar el entorno virtual CADA VEZ que abras una nueva terminal para trabajar en este proyecto.

#### Windows (PowerShell)

```cmd
venv\Scripts\activate
```

**Si aparece un error de permisos**:
```
cannot be loaded because running scripts is disabled on this system
```

**Solución**:
1. Abre PowerShell como **Administrador**
2. Ejecuta:
   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. Confirma con `Y`
4. Cierra PowerShell de administrador
5. Vuelve a tu PowerShell normal
6. Intenta activar nuevamente: `venv\Scripts\activate`

**Salida esperada**:
```
(venv) C:\Users\TuUsuario\Proyectos\gx-object-registry>
```

Nota el `(venv)` al inicio del prompt. **Esto indica que el entorno virtual está activo**.

#### Windows (CMD)

```cmd
venv\Scripts\activate.bat
```

#### Linux/macOS

```bash
source venv/bin/activate
```

**Salida esperada**:
```
(venv) usuario@pc:~/proyectos/gx-object-registry$
```

Nota el `(venv)` al inicio del prompt.

### Verificar que el Entorno Virtual está Activo

**Todos los sistemas**:

```bash
which python
```

**Windows (PowerShell)**:
```cmd
where python
```

**Salida esperada (Windows)**:
```
C:\Users\TuUsuario\Proyectos\gx-object-registry\venv\Scripts\python.exe
```

**Salida esperada (Linux/macOS)**:
```
/home/usuario/proyectos/gx-object-registry/venv/bin/python
```

**Si NO muestra la ruta con `venv`**, el entorno virtual NO está activo. Intenta activarlo nuevamente.

### Desactivar Entorno Virtual (cuando termines de trabajar)

Simplemente ejecuta:

```bash
deactivate
```

El `(venv)` desaparecerá del prompt.

**Para volver a trabajar**, debes activarlo nuevamente con `source venv/bin/activate` (Linux/macOS) o `venv\Scripts\activate` (Windows).

---

## 9. Configurar Variables de Entorno

Las variables de entorno contienen configuraciones sensibles del proyecto (contraseñas, claves secretas, URLs de conexión).

### ¿Qué es el archivo `.env`?

- Es un archivo de texto plano
- Contiene pares `CLAVE=valor`
- NO debe subirse a Git (está en `.gitignore`)
- Cada desarrollador tiene su propio `.env` con sus configuraciones locales

### Copiar el Archivo de Ejemplo

El proyecto incluye un archivo `.env.example` con todas las variables necesarias.

**Windows**:
```cmd
copy .env.example .env
```

**Linux/macOS**:
```bash
cp .env.example .env
```

**Verificar que se creó**:

**Windows**:
```cmd
dir .env
```

**Linux/macOS**:
```bash
ls -la .env
```

### Editar el Archivo `.env`

Abre el archivo `.env` con tu editor de texto preferido:

**Visual Studio Code**:
```bash
code .env
```

**Notepad (Windows)**:
```cmd
notepad .env
```

**nano (Linux/macOS)**:
```bash
nano .env
```

### Configuración de Variables

A continuación, las variables que **DEBES** configurar:

#### 1. DATABASE_URL

**Formato**:
```
DATABASE_URL=postgresql+asyncpg://USUARIO:CONTRASEÑA@HOST:PUERTO/NOMBRE_BD
```

**Valores por defecto** (cámbialos según tu instalación):

**Si instalaste PostgreSQL localmente con las configuraciones recomendadas**:

```env
DATABASE_URL=postgresql+asyncpg://gxuser:gxpassword@localhost:5432/gx_object_registry
```

**Componentes**:
- `gxuser`: Usuario de PostgreSQL (lo crearemos en la siguiente sección)
- `gxpassword`: Contraseña del usuario (cámbiala por una segura)
- `localhost`: Servidor (local)
- `5432`: Puerto de PostgreSQL (usa el que configuraste)
- `gx_object_registry`: Nombre de la base de datos (lo crearemos después)

**IMPORTANTE**: No uses el usuario `postgres` directamente. Crearemos un usuario específico para la aplicación.

#### 2. DATABASE_POOL_SIZE y DATABASE_MAX_OVERFLOW

```env
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10
```

**Puedes dejar estos valores por defecto** para desarrollo.

#### 3. APP_ENV

```env
APP_ENV=development
```

**Valores posibles**:
- `development`: Modo desarrollo (logs detallados, debug activo)
- `production`: Modo producción (logs mínimos, debug desactivado)

**Para desarrollo local, usa** `development`.

#### 4. DEBUG

```env
DEBUG=true
```

**Valores posibles**:
- `true`: Habilita modo debug (errores detallados)
- `false`: Deshabilita debug

**Para desarrollo, usa** `true`.

#### 5. LOG_LEVEL

```env
LOG_LEVEL=INFO
```

**Valores posibles**:
- `DEBUG`: Muestra todos los logs (muy detallado)
- `INFO`: Logs informativos (recomendado para desarrollo)
- `WARNING`: Solo advertencias y errores
- `ERROR`: Solo errores

#### 6. SECRET_KEY

**MUY IMPORTANTE**: Esta clave se usa para firmar tokens JWT.

**Generar una clave segura**:

**Desde Python** (recomendado):
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Salida ejemplo**:
```
Kx8vN3pQ2mL9wR5tY7uI1oP4aS6dF8gH2jK5lZ9xC3vB6nM0
```

**Copia ese valor** y pégalo en `.env`:

```env
SECRET_KEY=Kx8vN3pQ2mL9wR5tY7uI1oP4aS6dF8gH2jK5lZ9xC3vB6nM0
```

**NO uses** `change-this-secret-key-in-production`.

#### 7. API_PREFIX y API_VERSION

```env
API_PREFIX=/api
API_VERSION=v1
```

**Puedes dejar estos valores por defecto**.

#### 8. CORS_ORIGINS

```env
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

**Para desarrollo local**, usa:
```env
CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

**Separa múltiples orígenes con comas** (sin espacios).

#### 9. MAX_FILE_SIZE_MB

```env
MAX_FILE_SIZE_MB=50
```

Tamaño máximo de archivos CSV para importación.

#### 10. ALLOWED_HOSTS

```env
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Archivo `.env` Completo para Desarrollo

**Ejemplo completo**:

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://gxuser:gxpassword@localhost:5432/gx_object_registry
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# Application Settings
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO

# API Configuration
API_PREFIX=/api
API_VERSION=v1
API_TITLE=GeneXus Object Registry
API_DESCRIPTION=API para administrar objetos de GeneXus

# CORS (separate multiple origins with commas)
CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# Import Settings
MAX_FILE_SIZE_MB=50
MAX_ERRORS_TO_REPORT=100
CSV_BATCH_SIZE=500

# Security (IMPORTANT: Change SECRET_KEY!)
SECRET_KEY=TU_CLAVE_GENERADA_CON_SECRETS
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Reemplaza**:
- `TU_CLAVE_GENERADA_CON_SECRETS` con una clave real generada con `secrets`

### Guardar el Archivo

**Visual Studio Code**: `Ctrl+S` (Windows/Linux) o `Cmd+S` (macOS)
**nano**: `Ctrl+X`, luego `Y`, luego `Enter`
**Notepad**: Archivo → Guardar

---

## 10. Instalar Dependencias

Ahora instalaremos todas las bibliotecas Python que el proyecto necesita.

### Verificar Entorno Virtual Activo

**IMPORTANTE**: Asegúrate de que el entorno virtual esté activo.

**Verifica que veas** `(venv)` al inicio del prompt:

```
(venv) C:\Users\...\gx-object-registry>
```

**Si NO está activo**, actívalo:

**Windows**:
```cmd
venv\Scripts\activate
```

**Linux/macOS**:
```bash
source venv/bin/activate
```

### Actualizar pip

Antes de instalar dependencias, actualiza pip a la última versión:

```bash
python -m pip install --upgrade pip
```

**Salida esperada**:
```
Successfully installed pip-24.0
```

### Instalar Todas las Dependencias

```bash
pip install -r requirements.txt
```

**Qué hace este comando**:
- Lee el archivo [requirements.txt](requirements.txt)
- Descarga e instala cada paquete listado
- Instala también las dependencias de esas dependencias

**Salida esperada**:
```
Collecting fastapi>=0.109.0 (from -r requirements.txt (line 2))
  Downloading fastapi-0.109.2-py3-none-any.whl (92 kB)
Collecting uvicorn[standard]>=0.27.0 (from -r requirements.txt (line 3))
  Downloading uvicorn-0.27.1-py3-none-any.whl (60 kB)
...
Installing collected packages: ...
Successfully installed alembic-1.13.1 asyncpg-0.29.0 bcrypt-4.1.2 ...
```

**El proceso puede tardar 2-5 minutos** dependiendo de tu conexión a internet.

### Dependencias Instaladas

El archivo `requirements.txt` incluye **22 paquetes principales**:

| Categoría | Paquetes |
|-----------|----------|
| **FastAPI y Servidor** | fastapi, uvicorn, python-multipart |
| **Base de Datos** | sqlalchemy[asyncio], asyncpg, alembic |
| **Validación** | pydantic, pydantic-settings, email-validator |
| **Seguridad** | python-jose[cryptography], bcrypt |
| **CSV Processing** | chardet |
| **Logging** | structlog |
| **Environment** | python-dotenv |
| **Testing** | pytest, pytest-asyncio, pytest-cov, httpx, faker |
| **Code Quality** | black, ruff, mypy |

### Verificar Instalación

**Listar paquetes instalados**:
```bash
pip list
```

**Salida esperada** (parcial):
```
Package            Version
------------------ -------
alembic            1.13.1
asyncpg            0.29.0
bcrypt             4.1.2
fastapi            0.109.2
pydantic           2.5.3
sqlalchemy         2.0.25
uvicorn            0.27.1
...
```

**Verificar paquetes específicos**:
```bash
pip show fastapi
pip show sqlalchemy
pip show alembic
```

### Solución de Problemas Durante la Instalación

#### Error: "Microsoft Visual C++ 14.0 is required" (Windows)

**Causa**: Algunos paquetes necesitan compilación en Windows.

**Solución**:
1. Descarga **Microsoft C++ Build Tools**: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Ejecuta el instalador
3. Selecciona **Herramientas de compilación de C++**
4. Instala
5. Reinicia la terminal
6. Intenta `pip install -r requirements.txt` nuevamente

#### Error: "No module named '_ctypes'" (Linux)

**Causa**: Falta libffi-dev.

**Solución**:
```bash
sudo apt install -y libffi-dev python3-dev
pip install -r requirements.txt
```

#### Error: Timeout durante descarga

**Causa**: Conexión lenta o inestable.

**Solución**:
```bash
pip install -r requirements.txt --timeout=120
```

O instala paquetes uno por uno:
```bash
pip install fastapi
pip install uvicorn[standard]
# ... etc
```

---

## 11. Configurar Base de Datos

Ahora crearemos el usuario y la base de datos en PostgreSQL para la aplicación.

### Conceptos Importantes

**Usuario de aplicación vs Usuario postgres**:
- `postgres`: Usuario administrador de PostgreSQL (super usuario)
- `gxuser` (o el nombre que elijas): Usuario específico para la aplicación (menos privilegios)

**Base de datos**:
- `gx_object_registry`: Base de datos donde se almacenarán las tablas

### Windows

#### Conectar a PostgreSQL como postgres

Abre PowerShell y ejecuta:

```cmd
psql -U postgres
```

**Te pedirá la contraseña** que configuraste durante la instalación de PostgreSQL.

**Salida esperada**:
```
psql (15.3)
Type "help" for help.

postgres=#
```

Ahora estás dentro del shell de PostgreSQL.

#### Crear Usuario para la Aplicación

Dentro del shell de PostgreSQL (`postgres=#`), ejecuta:

```sql
CREATE USER gxuser WITH PASSWORD 'gxpassword';
```

**IMPORTANTE**: Cambia `gxpassword` por una contraseña segura.

**Salida esperada**:
```
CREATE ROLE
```

#### Crear Base de Datos

```sql
CREATE DATABASE gx_object_registry OWNER gxuser;
```

**Salida esperada**:
```
CREATE DATABASE
```

#### Otorgar Privilegios

```sql
GRANT ALL PRIVILEGES ON DATABASE gx_object_registry TO gxuser;
```

**Salida esperada**:
```
GRANT
```

#### Conectar a la Nueva Base de Datos

```sql
\c gx_object_registry
```

**Salida esperada**:
```
You are now connected to database "gx_object_registry" as user "postgres".
```

#### Otorgar Privilegios en el Esquema Public

```sql
GRANT ALL ON SCHEMA public TO gxuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO gxuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO gxuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO gxuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO gxuser;
```

**Salida esperada**:
```
GRANT
GRANT
GRANT
ALTER DEFAULT PRIVILEGES
ALTER DEFAULT PRIVILEGES
```

#### Verificar Usuario y Base de Datos

```sql
\l
```

Deberías ver `gx_object_registry` en la lista.

```sql
\du
```

Deberías ver `gxuser` en la lista de roles.

#### Salir de psql

```sql
\q
```

#### Probar Conexión con el Nuevo Usuario

```cmd
psql -U gxuser -d gx_object_registry -h localhost
```

**Te pedirá la contraseña de gxuser**.

**Si la conexión es exitosa**:
```
psql (15.3)
Type "help" for help.

gx_object_registry=>
```

**Sal de psql**:
```sql
\q
```

### Ubuntu / Debian

#### Conectar a PostgreSQL como postgres

```bash
sudo -u postgres psql
```

**Salida esperada**:
```
psql (15.4)
Type "help" for help.

postgres=#
```

#### Crear Usuario para la Aplicación

```sql
CREATE USER gxuser WITH PASSWORD 'gxpassword';
```

**IMPORTANTE**: Cambia `gxpassword` por una contraseña segura.

**Salida esperada**:
```
CREATE ROLE
```

#### Crear Base de Datos

```sql
CREATE DATABASE gx_object_registry OWNER gxuser;
```

**Salida esperada**:
```
CREATE DATABASE
```

#### Otorgar Privilegios

```sql
GRANT ALL PRIVILEGES ON DATABASE gx_object_registry TO gxuser;
```

```sql
\c gx_object_registry
```

```sql
GRANT ALL ON SCHEMA public TO gxuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO gxuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO gxuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO gxuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO gxuser;
```

#### Salir de psql

```sql
\q
```

#### Probar Conexión

```bash
psql -U gxuser -d gx_object_registry -h localhost
```

**Salida esperada**:
```
psql (15.4)
gx_object_registry=>
```

```sql
\q
```

### macOS

#### Conectar a PostgreSQL

```bash
psql postgres
```

**Salida esperada**:
```
psql (15.4)
postgres=#
```

Sigue los mismos pasos que Ubuntu (crear usuario, crear BD, otorgar privilegios).

### Verificar DATABASE_URL en .env

Asegúrate de que el archivo `.env` tenga la configuración correcta:

```env
DATABASE_URL=postgresql+asyncpg://gxuser:gxpassword@localhost:5432/gx_object_registry
```

**Componentes**:
- `gxuser`: El usuario que creaste
- `gxpassword`: La contraseña que configuraste
- `localhost`: Servidor local
- `5432`: Puerto de PostgreSQL (o el que configuraste)
- `gx_object_registry`: Nombre de la base de datos

**Si usaste valores diferentes**, actualiza el `.env` en consecuencia.

---

## 12. Ejecutar Migraciones

Las **migraciones** son scripts que crean y modifican la estructura de la base de datos (tablas, columnas, índices).

### ¿Qué son las Migraciones?

- Son archivos Python en la carpeta `alembic/versions/`
- Cada migración tiene un método `upgrade()` (aplicar cambios) y `downgrade()` (revertir cambios)
- Se ejecutan en orden cronológico
- Alembic lleva control de qué migraciones ya se aplicaron

### Migraciones Existentes en el Proyecto

El proyecto tiene estas migraciones:

1. `001_create_object_types_and_genexus_objects.py` - Crea tablas iniciales
2. `20260731_1438_55adc69b9133_add_auth_system_and_created_by_fields.py` - Sistema de autenticación
3. `20260801_1120_add_last_login_to_users.py` - Campo last_login
4. `20260801_1200_add_must_change_password.py` - Campo must_change_password

### Verificar Entorno Virtual Activo

**Asegúrate de que el entorno virtual esté activo**:

```
(venv) C:\...\gx-object-registry>
```

**Si NO está activo**, actívalo:

**Windows**:
```cmd
venv\Scripts\activate
```

**Linux/macOS**:
```bash
source venv/bin/activate
```

### Ver Estado Actual de Migraciones

```bash
alembic current
```

**Salida esperada** (si es primera instalación):
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
```

**No muestra ninguna revisión** porque aún no se ha aplicado ninguna migración.

### Ver Historial de Migraciones Disponibles

```bash
alembic history
```

**Salida esperada**:
```
Rev: 20260801_1200 (head)
Parent: 20260801_1120
Path: alembic/versions/20260801_1200_add_must_change_password.py

    add must change password

Rev: 20260801_1120
Parent: 20260731_1438_55adc69b9133
Path: alembic/versions/20260801_1120_add_last_login_to_users.py

    add last login to users

...
```

### Ejecutar Todas las Migraciones

```bash
alembic upgrade head
```

**Qué hace**:
- `upgrade`: Aplicar migraciones
- `head`: Hasta la última migración disponible

**Salida esperada**:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 001, create object types and genexus objects
INFO  [alembic.runtime.migration] Running upgrade 001 -> 20260731_1438_55adc69b9133, add auth system and created by fields
INFO  [alembic.runtime.migration] Running upgrade 20260731_1438_55adc69b9133 -> 20260801_1120, add last login to users
INFO  [alembic.runtime.migration] Running upgrade 20260801_1120 -> 20260801_1200, add must change password
```

**Esto significa que se crearon todas las tablas**.

### Verificar que las Migraciones se Aplicaron

```bash
alembic current
```

**Salida esperada**:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
20260801_1200 (head)
```

**Muestra la última migración aplicada**.

### Verificar Tablas en PostgreSQL

**Conectar a la base de datos**:

**Windows**:
```cmd
psql -U gxuser -d gx_object_registry -h localhost
```

**Linux**:
```bash
psql -U gxuser -d gx_object_registry -h localhost
```

**Listar tablas**:
```sql
\dt
```

**Salida esperada**:
```
                List of relations
 Schema |        Name         | Type  | Owner
--------+---------------------+-------+--------
 public | alembic_version     | table | gxuser
 public | genexus_objects     | table | gxuser
 public | object_types        | table | gxuser
 public | users               | table | gxuser
(4 rows)
```

**Describir tabla users**:
```sql
\d users
```

**Salida esperada** (columnas de la tabla):
```
                          Table "public.users"
       Column        |            Type             | Nullable | Default
---------------------+-----------------------------+----------+---------
 id                  | integer                     | not null |
 username            | character varying(50)       | not null |
 email               | character varying(255)      | not null |
 full_name           | character varying(255)      |          |
 hashed_password     | character varying(255)      | not null |
 is_active           | boolean                     | not null |
 created_at          | timestamp without time zone | not null |
 updated_at          | timestamp without time zone | not null |
 last_login          | timestamp without time zone |          |
 must_change_password| boolean                     | not null |
```

**Salir de psql**:
```sql
\q
```

### Solución de Problemas

#### Error: "Can't locate revision identified by..."

**Causa**: La base de datos tiene migraciones aplicadas que no coinciden con los archivos.

**Solución**:
```bash
alembic stamp head
```

#### Error: "Target database is not up to date"

**Causa**: Hay migraciones pendientes.

**Solución**: Ejecuta `alembic upgrade head`

#### Error: "FATAL: password authentication failed"

**Causa**: La contraseña en `.env` no coincide con la configurada en PostgreSQL.

**Solución**: Verifica `DATABASE_URL` en `.env`

---

## 13. Cargar Datos Iniciales

Los **datos iniciales** (seeds) son registros básicos necesarios para que la aplicación funcione.

### ¿Qué Datos Iniciales Cargará el Script?

El script `scripts/seed_database.py` carga **tipos de objetos GeneXus**:

- PROCEDURE
- TRANSACTION
- DATA_PROVIDER
- WEB_PANEL
- WORK_WITH
- DASHBOARD
- SD_PANEL
- MASTER_PAGE
- THEME
- DOMAIN
- IMAGE
- STYLE

### Verificar Entorno Virtual Activo

```
(venv) C:\...\gx-object-registry>
```

### Ejecutar el Script de Seed

```bash
python scripts/seed_database.py
```

**Salida esperada**:
```
🌱 Iniciando seed de tipos de objeto...
📊 Base de datos: localhost:5432/gx_object_registry

✅ Creado: PROCEDURE (ID: 1)
✅ Creado: TRANSACTION (ID: 2)
✅ Creado: DATA_PROVIDER (ID: 3)
✅ Creado: WEB_PANEL (ID: 4)
✅ Creado: WORK_WITH (ID: 5)
✅ Creado: DASHBOARD (ID: 6)
✅ Creado: SD_PANEL (ID: 7)
✅ Creado: MASTER_PAGE (ID: 8)
✅ Creado: THEME (ID: 9)
✅ Creado: DOMAIN (ID: 10)
✅ Creado: IMAGE (ID: 11)
✅ Creado: STYLE (ID: 12)

✨ Seed completado:
   • Creados: 12
   • Ya existían: 0
   • Total: 12
```

### Si Ejecutas el Script Nuevamente

```bash
python scripts/seed_database.py
```

**Salida esperada**:
```
🌱 Iniciando seed de tipos de objeto...
📊 Base de datos: localhost:5432/gx_object_registry

⏭️  Ya existe: PROCEDURE
⏭️  Ya existe: TRANSACTION
⏭️  Ya existe: DATA_PROVIDER
...

✨ Seed completado:
   • Creados: 0
   • Ya existían: 12
   • Total: 12
```

**El script es idempotente**: Puede ejecutarse varias veces sin duplicar datos.

### Verificar Datos en PostgreSQL

```bash
psql -U gxuser -d gx_object_registry -h localhost
```

```sql
SELECT * FROM object_types;
```

**Salida esperada**:
```
 id |     name      |         created_at         |         updated_at
----+---------------+----------------------------+----------------------------
  1 | PROCEDURE     | 2026-08-03 10:30:00.123456 | 2026-08-03 10:30:00.123456
  2 | TRANSACTION   | 2026-08-03 10:30:00.234567 | 2026-08-03 10:30:00.234567
...
(12 rows)
```

```sql
\q
```

---

## 14. Crear Usuario Administrador

Ahora crearemos el primer usuario para poder acceder al sistema.

### Ejecutar Script de Creación de Usuario

```bash
python scripts/create_admin.py
```

### Proceso Interactivo

El script te pedirá la siguiente información:

**Salida esperada**:
```
============================================================
  CREAR USUARIO ADMINISTRADOR
============================================================

Ingresa los datos del nuevo usuario:
------------------------------------------------------------
Username (3-50 caracteres):
```

**Ingresa un username**. Ejemplo: `admin`

```
Email:
```

**Ingresa un email válido**. Ejemplo: `admin@example.com`

```
Nombre completo (opcional):
```

**Ingresa tu nombre** o presiona Enter para omitir. Ejemplo: `Administrador`

```
Contraseña (mínimo 6 caracteres):
```

**Ingresa una contraseña segura**. Ejemplo: `Admin123!`

**Nota**: Los caracteres NO se mostrarán mientras escribes (es normal).

```
Confirmar contraseña:
```

**Ingresa la misma contraseña nuevamente**.

### Confirmación

```
------------------------------------------------------------
Datos del usuario:
  Username:  admin
  Email:     admin@example.com
  Nombre:    Administrador
------------------------------------------------------------

¿Crear este usuario? (S/n):
```

**Presiona Enter** (o escribe `S`) para confirmar.

### Usuario Creado

```
Creando usuario...

✅ Usuario creado exitosamente!

============================================================
  CREDENCIALES DE ACCESO
============================================================
  Username:  admin
  Email:     admin@example.com
  Nombre:    Administrador
  ID:        1
============================================================

Puedes iniciar sesión en: http://localhost:8000/web/login
```

**IMPORTANTE**: Guarda estas credenciales en un lugar seguro.

### Si Ya Existen Usuarios

Si ejecutas el script nuevamente:

```
⚠️  Ya existen 1 usuario(s) en el sistema.

¿Deseas crear un usuario adicional de todos modos? (s/N):
```

**Puedes crear más usuarios** respondiendo `s`.

### Verificar Usuario en PostgreSQL

```bash
psql -U gxuser -d gx_object_registry -h localhost
```

```sql
SELECT id, username, email, is_active FROM users;
```

**Salida esperada**:
```
 id | username |       email       | is_active
----+----------+-------------------+-----------
  1 | admin    | admin@example.com | t
(1 row)
```

```sql
\q
```

---

## 15. Iniciar el Servidor

Finalmente, iniciaremos el servidor web para acceder a la aplicación.

### Verificar Entorno Virtual Activo

```
(venv) C:\...\gx-object-registry>
```

### Iniciar con Uvicorn

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Parámetros**:
- `src.main:app`: Módulo y variable de la aplicación FastAPI
- `--reload`: Reinicia automáticamente al detectar cambios en el código
- `--host 0.0.0.0`: Permite conexiones desde cualquier IP (incluida la red local)
- `--port 8000`: Puerto donde correrá el servidor

**Salida esperada**:
```
INFO:     Will watch for changes in these directories: ['C:\\...\\gx-object-registry']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [67890]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**El servidor está corriendo** cuando ves "Application startup complete".

### Alternativa: Iniciar Solo en Localhost

Si NO necesitas acceso desde la red local:

```bash
uvicorn src.main:app --reload
```

Esto inicia el servidor solo en `http://127.0.0.1:8000`

### Alternativa: Usar el Script Main

```bash
python src/main.py
```

**Salida similar** a uvicorn.

### Detener el Servidor

**Presiona** `Ctrl+C` en la terminal donde está corriendo.

**Salida esperada**:
```
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [67890]
```

---

## 16. Verificar Instalación

Ahora verificaremos que todo funciona correctamente.

### 1. Verificar Health Check (API)

**Opción 1: Navegador**

Abre tu navegador y ve a:

```
http://localhost:8000/health
```

**Salida esperada**:
```json
{
  "status": "ok",
  "app": "GeneXus Object Registry",
  "version": "v1",
  "environment": "development"
}
```

**Opción 2: curl (desde otra terminal)**

```bash
curl http://localhost:8000/health
```

**Salida esperada**:
```json
{"status":"ok","app":"GeneXus Object Registry","version":"v1","environment":"development"}
```

### 2. Acceder a la Documentación de la API

Abre tu navegador y ve a:

```
http://localhost:8000/docs
```

**Deberías ver**: Swagger UI con todos los endpoints documentados.

**Endpoints disponibles**:
- `/api/auth/*` - Autenticación
- `/api/users/*` - Gestión de usuarios
- `/api/object-types/*` - Tipos de objetos
- `/api/objects/*` - Objetos GeneXus
- `/api/objects/import/csv` - Importación CSV

### 3. Acceder a la Interfaz Web

Abre tu navegador y ve a:

```
http://localhost:8000/web/login
```

**Deberías ver**: Página de inicio de sesión.

### 4. Iniciar Sesión

**Ingresa las credenciales** que creaste:

- **Username**: `admin` (o el que creaste)
- **Password**: `Admin123!` (o la que creaste)

**Haz clic en** "Iniciar Sesión"

**Deberías ser redirigido a**: `http://localhost:8000/web`

**Deberías ver**: Panel principal con:
- Tipos de Objetos
- Objetos GeneXus
- Importar CSV
- Usuarios (solo administradores)

### 5. Verificar Tipos de Objetos

En la interfaz web:

1. Haz clic en **"Tipos de Objetos"**
2. **Deberías ver** los 12 tipos cargados por el seed:
   - PROCEDURE
   - TRANSACTION
   - DATA_PROVIDER
   - etc.

### 6. Crear un Objeto de Prueba

1. Haz clic en **"Objetos GeneXus"**
2. Haz clic en **"Nuevo Objeto"**
3. Completa el formulario:
   - **Nombre**: `TestProcedure`
   - **Descripción**: `Procedimiento de prueba`
   - **Tipo**: Selecciona `PROCEDURE`
4. Haz clic en **"Guardar"**

**El objeto debería aparecer** en la lista.

### 7. Verificar Logs en la Terminal

En la terminal donde corre Uvicorn, deberías ver logs como:

```
INFO:     127.0.0.1:54321 - "GET /web/login HTTP/1.1" 200 OK
INFO:     127.0.0.1:54321 - "POST /api/auth/login HTTP/1.1" 200 OK
INFO:     127.0.0.1:54321 - "GET /web HTTP/1.1" 200 OK
INFO:     127.0.0.1:54321 - "GET /api/object-types HTTP/1.1" 200 OK
```

### Checklist de Verificación

```
✅ PostgreSQL está corriendo
✅ Migraciones aplicadas correctamente
✅ Datos iniciales cargados (12 tipos de objetos)
✅ Usuario administrador creado
✅ Servidor FastAPI corriendo en puerto 8000
✅ Health check responde correctamente
✅ Documentación Swagger accesible
✅ Interfaz web cargando
✅ Login funciona correctamente
✅ Puedo ver tipos de objetos
✅ Puedo crear objetos GeneXus
```

**Si todos los items están marcados**: ✨ **¡Instalación exitosa!**

---

## 17. Instalación con Docker (Alternativa)

Docker permite ejecutar la aplicación en contenedores aislados, sin necesidad de instalar Python, PostgreSQL u otras dependencias directamente en tu sistema.

### Prerrequisitos

- **Docker Desktop** instalado (Windows/macOS)
- **Docker y Docker Compose** instalados (Linux)

### Verificar Docker Instalado

```bash
docker --version
docker-compose --version
```

**Salida esperada**:
```
Docker version 24.0.5
Docker Compose version v2.20.2
```

**Si NO está instalado**:

**Windows/macOS**: Descarga Docker Desktop desde <https://www.docker.com/products/docker-desktop>

**Ubuntu**:
```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

**Reinicia tu sesión** después de agregar tu usuario al grupo docker.

### Arquitectura Docker del Proyecto

El proyecto incluye:

- `Dockerfile`: Imagen para el backend (FastAPI)
- `docker-compose.yml`: Orquestación de servicios (API + PostgreSQL)

**Servicios definidos**:

1. **postgres**: PostgreSQL 15 con datos persistentes
2. **api**: Aplicación FastAPI con auto-reload

### Configuración en docker-compose.yml

```yaml
services:
  postgres:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: gx_object_registry
      POSTGRES_USER: gxuser
      POSTGRES_PASSWORD: gxpassword

  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgresql+asyncpg://gxuser:gxpassword@postgres:5432/gx_object_registry
```

### Levantar Todo el Stack

**Desde la carpeta del proyecto**:

```bash
docker-compose up
```

**Qué hace**:
- Descarga las imágenes necesarias (primera vez)
- Construye la imagen de la API
- Inicia PostgreSQL
- Inicia FastAPI
- Muestra logs en tiempo real

**Salida esperada** (parcial):
```
[+] Running 2/2
 ✔ Container gx_postgres  Started
 ✔ Container gx_api       Started

gx_postgres  | PostgreSQL init process complete; ready for start up.
gx_postgres  | LOG:  database system is ready to accept connections
gx_api       | INFO:     Application startup complete.
gx_api       | INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Para ejecutar en segundo plano** (detached):

```bash
docker-compose up -d
```

### Ejecutar Migraciones en Docker

```bash
docker-compose exec api alembic upgrade head
```

### Cargar Datos Iniciales en Docker

```bash
docker-compose exec api python scripts/seed_database.py
```

### Crear Usuario Administrador en Docker

```bash
docker-compose exec api python scripts/create_admin.py
```

**Sigue el proceso interactivo** normalmente.

### Acceder a la Aplicación

Abre tu navegador:

```
http://localhost:8000/web/login
```

### Ver Logs en Tiempo Real

```bash
docker-compose logs -f
```

**Solo logs de la API**:
```bash
docker-compose logs -f api
```

**Solo logs de PostgreSQL**:
```bash
docker-compose logs -f postgres
```

### Entrar a un Contenedor

**Entrar al contenedor de la API**:

```bash
docker-compose exec api bash
```

Ahora estás dentro del contenedor y puedes ejecutar comandos Python.

**Salir**:
```bash
exit
```

**Entrar a PostgreSQL**:

```bash
docker-compose exec postgres psql -U gxuser -d gx_object_registry
```

### Detener los Servicios

**Detener sin eliminar contenedores**:
```bash
docker-compose stop
```

**Detener y eliminar contenedores**:
```bash
docker-compose down
```

**Detener y eliminar volúmenes (⚠️ ELIMINA DATOS)**:
```bash
docker-compose down -v
```

### Reconstruir Imágenes

Si modificaste el `Dockerfile` o dependencias:

```bash
docker-compose build
docker-compose up
```

**O en un solo comando**:
```bash
docker-compose up --build
```

### Ventajas de Docker

✅ No necesitas instalar Python, PostgreSQL, ni dependencias
✅ Mismo entorno en desarrollo y producción
✅ Fácil de compartir con el equipo
✅ Aislamiento completo del sistema

### Desventajas de Docker

❌ Mayor consumo de recursos (RAM, disco)
❌ Curva de aprendizaje para principiantes
❌ Reinicio más lento al modificar código (aunque --reload ayuda)

---

## 18. Solución de Problemas Comunes

Esta sección cubre los errores más frecuentes durante la instalación y su solución.

### Problemas con Python

#### Error: `'python' is not recognized as an internal or external command`

**Causa**: Python no está instalado o no está en el PATH.

**Solución Windows**:

1. Verifica instalación:
   ```cmd
   py --version
   ```

2. Si `py` funciona, úsalo en lugar de `python`:
   ```cmd
   py -m venv venv
   py -m pip install -r requirements.txt
   ```

3. Si tampoco funciona, reinstala Python marcando **"Add Python to PATH"**

**Solución Linux/macOS**:

```bash
python3 --version
```

Usa `python3` en lugar de `python`.

#### Error: `No module named 'venv'`

**Causa**: El módulo venv no está instalado.

**Solución Ubuntu**:
```bash
sudo apt install python3.11-venv
```

#### Error: `externally-managed-environment`

**Causa**: Python está gestionado por el sistema (Ubuntu 23.04+).

**Solución**:

**Opción 1 (Recomendada)**: Usa entornos virtuales:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Opción 2**: Usa pipx para herramientas globales:
```bash
sudo apt install pipx
```

### Problemas con PostgreSQL

#### Error: `psql: error: connection to server on socket failed`

**Causa**: PostgreSQL no está corriendo.

**Solución Windows**:
```cmd
net start postgresql-x64-15
```

**Solución Linux**:
```bash
sudo systemctl start postgresql
sudo systemctl status postgresql
```

**Solución macOS**:
```bash
brew services start postgresql@15
```

#### Error: `FATAL: password authentication failed for user "gxuser"`

**Causa**: Contraseña incorrecta en `.env` o usuario no existe.

**Solución**:

1. Verifica que el usuario existe:
   ```bash
   psql -U postgres
   \du
   ```

2. Si no existe, créalo:
   ```sql
   CREATE USER gxuser WITH PASSWORD 'gxpassword';
   ```

3. Verifica `DATABASE_URL` en `.env`:
   ```env
   DATABASE_URL=postgresql+asyncpg://gxuser:gxpassword@localhost:5432/gx_object_registry
   ```

4. Si la contraseña tiene caracteres especiales, escápala en la URL.

#### Error: `database "gx_object_registry" does not exist`

**Causa**: La base de datos no fue creada.

**Solución**:

```bash
psql -U postgres
```

```sql
CREATE DATABASE gx_object_registry OWNER gxuser;
\q
```

#### Error: `connection to server at "localhost" (::1), port 5432 failed`

**Causa**: PostgreSQL está en un puerto diferente.

**Solución**:

1. Verifica el puerto:
   ```bash
   psql -U postgres
   SHOW port;
   ```

2. Actualiza `.env`:
   ```env
   DATABASE_URL=postgresql+asyncpg://gxuser:gxpassword@localhost:PUERTO/gx_object_registry
   ```

### Problemas con Migraciones

#### Error: `Target database is not up to date`

**Causa**: Hay cambios en los modelos que no están reflejados en migraciones.

**Solución**:

```bash
alembic upgrade head
```

#### Error: `Can't locate revision identified by 'xxxx'`

**Causa**: Desincronización entre base de datos y archivos de migración.

**Solución**:

**Opción 1**: Forzar el stamp:
```bash
alembic stamp head
```

**Opción 2**: Resetear base de datos (⚠️ ELIMINA DATOS):
```bash
alembic downgrade base
alembic upgrade head
```

#### Error: `relation "users" already exists`

**Causa**: Las tablas ya existen en la base de datos.

**Solución**:

**Opción 1**: Marca la base de datos como actualizada:
```bash
alembic stamp head
```

**Opción 2**: Elimina y recrea (⚠️ ELIMINA DATOS):
```bash
psql -U gxuser -d gx_object_registry
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO gxuser;
\q

alembic upgrade head
```

### Problemas con Dependencias

#### Error: `error: Microsoft Visual C++ 14.0 or greater is required` (Windows)

**Causa**: Falta compilador C++ para paquetes con extensiones nativas.

**Solución**:

1. Descarga **Build Tools for Visual Studio**: <https://visualstudio.microsoft.com/visual-cpp-build-tools/>
2. Ejecuta el instalador
3. Selecciona **"Herramientas de compilación de C++"**
4. Instala
5. Reinicia terminal
6. Vuelve a ejecutar `pip install -r requirements.txt`

#### Error: `error: command 'gcc' failed` (Linux)

**Causa**: Faltan herramientas de desarrollo.

**Solución Ubuntu**:
```bash
sudo apt install -y build-essential python3-dev libpq-dev
pip install -r requirements.txt
```

#### Error: `No matching distribution found for bcrypt>=4.0.0,<5.0.0`

**Causa**: Versión de Python incompatible (probablemente 3.13+).

**Solución**:

Usa Python 3.11 o 3.12:

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Problemas con el Servidor

#### Error: `Address already in use: 0.0.0.0:8000`

**Causa**: El puerto 8000 ya está ocupado.

**Solución**:

**Opción 1**: Usa otro puerto:
```bash
uvicorn src.main:app --reload --port 8001
```

**Opción 2**: Encuentra y mata el proceso:

**Windows**:
```cmd
netstat -ano | findstr :8000
taskkill /PID <numero_pid> /F
```

**Linux/macOS**:
```bash
lsof -i :8000
kill -9 <pid>
```

#### Error: `ModuleNotFoundError: No module named 'src'`

**Causa**: No estás ejecutando desde la carpeta raíz del proyecto.

**Solución**:

```bash
cd gx-object-registry
uvicorn src.main:app --reload
```

#### Error: `ModuleNotFoundError: No module named 'fastapi'`

**Causa**: El entorno virtual no está activo o las dependencias no están instaladas.

**Solución**:

1. Activa el entorno virtual:
   ```bash
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

2. Verifica que esté activo (debe aparecer `(venv)`):
   ```bash
   which python
   ```

3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

### Problemas con Docker

#### Error: `Cannot connect to the Docker daemon`

**Causa**: Docker no está corriendo.

**Solución**:

**Windows/macOS**: Inicia Docker Desktop

**Linux**:
```bash
sudo systemctl start docker
```

#### Error: `permission denied while trying to connect to the Docker daemon`

**Causa**: Tu usuario no tiene permisos para Docker.

**Solución Linux**:

```bash
sudo usermod -aG docker $USER
```

**Cierra sesión e inicia sesión nuevamente**, o ejecuta:

```bash
newgrp docker
```

#### Error: `port is already allocated`

**Causa**: El puerto ya está en uso.

**Solución**:

Cambia el puerto en `docker-compose.yml`:

```yaml
services:
  api:
    ports:
      - "8001:8000"  # Cambia 8000 a 8001
```

### Problemas de Rendimiento

#### La aplicación está muy lenta

**Causas posibles**:

1. **Base de datos sin índices**: Ejecuta migraciones completas
2. **Demasiados logs**: Cambia `LOG_LEVEL=WARNING` en `.env`
3. **Recursos del sistema**: Cierra aplicaciones innecesarias

**Solución**:

```env
LOG_LEVEL=WARNING
DEBUG=false
```

Reinicia el servidor.

### Tabla de Referencia Rápida de Errores

| Error | Causa Común | Solución Rápida |
|-------|-------------|-----------------|
| `'python' is not recognized` | Python no en PATH | Usa `py` en Windows |
| `psql: connection failed` | PostgreSQL detenido | `sudo systemctl start postgresql` |
| `password authentication failed` | Contraseña incorrecta | Verifica `.env` |
| `database does not exist` | BD no creada | `CREATE DATABASE ...` |
| `Address already in use` | Puerto ocupado | Usa `--port 8001` |
| `No module named 'src'` | Carpeta incorrecta | `cd gx-object-registry` |
| `No module named 'fastapi'` | Entorno no activo | `source venv/bin/activate` |
| `C++ 14.0 required` | Falta compilador | Instala Build Tools |

### ¿Necesitas Más Ayuda?

Si el problema persiste:

1. **Revisa los logs completos** del error
2. **Busca el error exacto** en Google o StackOverflow
3. **Verifica que seguiste todos los pasos** de instalación
4. **Comprueba las versiones** de Python, PostgreSQL, etc.

---

**FIN DE LA PARTE 1: INSTALACIÓN LOCAL**

---

# PARTE 2: DESPLIEGUE EN PRODUCCIÓN

Esta segunda parte cubre el despliegue del sistema en un servidor de producción Ubuntu 22.04 LTS.

---

## 19. Preparación del Servidor

### Requisitos del Servidor

**Especificaciones mínimas recomendadas**:

- **Sistema Operativo**: Ubuntu 22.04 LTS (64-bit)
- **RAM**: 2 GB mínimo, 4 GB recomendado
- **CPU**: 2 núcleos
- **Disco**: 20 GB SSD
- **Red**: Conexión a Internet estable
- **Acceso**: SSH con clave pública (recomendado)

### Proveedores Recomendados

- **DigitalOcean**: Droplets desde $6/mes
- **AWS**: EC2 t3.micro (capa gratuita disponible)
- **Linode**: Desde $5/mes
- **Vultr**: Desde $5/mes
- **Hetzner**: Desde €4/mes

### Conectarse al Servidor

**Desde tu computadora local**:

```bash
ssh usuario@IP_DEL_SERVIDOR
```

**O con clave SSH**:

```bash
ssh -i ~/.ssh/tu_clave.pem usuario@IP_DEL_SERVIDOR
```

**Ejemplo**:
```bash
ssh root@203.0.113.10
```

### Actualizar Sistema

**Primer paso crítico**:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt autoremove -y
```

### Configurar Zona Horaria

```bash
sudo timedatectl set-timezone America/Mexico_City
```

**Ver zonas disponibles**:
```bash
timedatectl list-timezones
```

### Crear Usuario para la Aplicación

**NO uses root para ejecutar la aplicación**.

```bash
sudo adduser gxapp
```

**Ingresa contraseña** y completa los datos.

**Agregar a sudoers**:

```bash
sudo usermod -aG sudo gxapp
```

**Cambiar a ese usuario**:

```bash
su - gxapp
```

### Instalar Herramientas Esenciales

```bash
sudo apt install -y curl wget git build-essential software-properties-common
```

---

## 20. Configuración de PostgreSQL en Producción

### Instalar PostgreSQL

```bash
sudo apt install -y postgresql-15 postgresql-contrib-15
```

### Iniciar y Habilitar Servicio

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo systemctl status postgresql
```

### Configurar Contraseña para postgres

```bash
sudo -u postgres psql
```

```sql
ALTER USER postgres WITH PASSWORD 'tu_contraseña_segura_postgres';
\q
```

### Crear Usuario y Base de Datos

```bash
sudo -u postgres psql
```

```sql
CREATE USER gxuser WITH PASSWORD 'contraseña_produccion_segura';
CREATE DATABASE gx_object_registry OWNER gxuser;
GRANT ALL PRIVILEGES ON DATABASE gx_object_registry TO gxuser;

\c gx_object_registry

GRANT ALL ON SCHEMA public TO gxuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO gxuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO gxuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO gxuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO gxuser;

\q
```

### Configurar Acceso Remoto (Opcional)

**Solo si necesitas acceso desde otra máquina**.

Edita configuración de PostgreSQL:

```bash
sudo nano /etc/postgresql/15/main/postgresql.conf
```

Busca y modifica:

```
listen_addresses = 'localhost'
```

Cambia a:

```
listen_addresses = '*'
```

Edita pg_hba.conf:

```bash
sudo nano /etc/postgresql/15/main/pg_hba.conf
```

Agrega al final:

```
host    all             all             0.0.0.0/0               scram-sha-256
```

Reinicia PostgreSQL:

```bash
sudo systemctl restart postgresql
```

### Verificar Conexión

```bash
psql -U gxuser -d gx_object_registry -h localhost
```

---

## 21. Instalación del Proyecto en Producción

### Elegir Ubicación

```bash
cd /home/gxapp
mkdir apps
cd apps
```

### Clonar Repositorio

```bash
git clone https://github.com/USUARIO/gx-object-registry.git
cd gx-object-registry
```

### Instalar Python 3.11

```bash
sudo apt install -y python3.11 python3.11-venv python3.11-dev
```

### Crear Entorno Virtual

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

### Configurar Variables de Entorno

```bash
cp .env.example .env
nano .env
```

**Configuración de producción**:

```env
# Database
DATABASE_URL=postgresql+asyncpg://gxuser:contraseña_produccion@localhost:5432/gx_object_registry

# Application
APP_ENV=production
DEBUG=false
LOG_LEVEL=WARNING

# Security - GENERAR NUEVA CLAVE
SECRET_KEY=clave_generada_con_secrets_muy_larga_y_segura
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com

# CORS
CORS_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com

# API
API_PREFIX=/api
API_VERSION=v1
```

**Generar SECRET_KEY**:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

### Ejecutar Migraciones

```bash
source venv/bin/activate
alembic upgrade head
```

### Cargar Datos Iniciales

```bash
python scripts/seed_database.py
```

### Crear Usuario Administrador

```bash
python scripts/create_admin.py
```

### Probar Servidor Manualmente

```bash
source venv/bin/activate
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

Accede desde navegador: `http://IP_SERVIDOR:8000`

**Si funciona**, detén con `Ctrl+C`.

---

## 22. Configuración de Gunicorn

Gunicorn es un servidor WSGI/ASGI robusto para producción.

### Ya está instalado

Lo instalamos en la sección anterior con:

```bash
pip install gunicorn
```

### Probar Gunicorn

```bash
source venv/bin/activate
gunicorn src.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

**Parámetros**:
- `--workers 4`: Número de procesos workers (recomendado: 2 x CPU cores + 1)
- `--worker-class uvicorn.workers.UvicornWorker`: Worker asíncrono
- `--bind 0.0.0.0:8000`: IP y puerto

**Detén con** `Ctrl+C`.

### Calcular Workers Óptimos

```bash
nproc
```

**Si muestra** `2` (2 cores), usa: `--workers 5` (2 x 2 + 1)

---

## 23. Configuración de Systemd

Systemd gestiona la aplicación como servicio del sistema.

### Crear Archivo de Servicio

```bash
sudo nano /etc/systemd/system/gxregistry.service
```

**Contenido**:

```ini
[Unit]
Description=GeneXus Object Registry API
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=notify
User=gxapp
Group=gxapp
WorkingDirectory=/home/gxapp/apps/gx-object-registry
Environment="PATH=/home/gxapp/apps/gx-object-registry/venv/bin"

ExecStart=/home/gxapp/apps/gx-object-registry/venv/bin/gunicorn src.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 127.0.0.1:8000 \
  --access-logfile /var/log/gxregistry/access.log \
  --error-logfile /var/log/gxregistry/error.log \
  --timeout 120

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

**Ajusta**:
- `--workers`: Según tus CPU cores
- `User` y `Group`: Usuario que creaste
- Rutas según tu instalación

### Crear Carpeta de Logs

```bash
sudo mkdir -p /var/log/gxregistry
sudo chown gxapp:gxapp /var/log/gxregistry
```

### Recargar Systemd

```bash
sudo systemctl daemon-reload
```

### Habilitar e Iniciar Servicio

```bash
sudo systemctl enable gxregistry
sudo systemctl start gxregistry
```

### Verificar Estado

```bash
sudo systemctl status gxregistry
```

**Salida esperada**:

```
● gxregistry.service - GeneXus Object Registry API
     Loaded: loaded (/etc/systemd/system/gxregistry.service; enabled)
     Active: active (running) since ...
```

### Ver Logs

```bash
sudo journalctl -u gxregistry -f
```

**Logs de acceso**:

```bash
tail -f /var/log/gxregistry/access.log
```

### Comandos Útiles

```bash
# Reiniciar
sudo systemctl restart gxregistry

# Detener
sudo systemctl stop gxregistry

# Ver logs
sudo journalctl -u gxregistry --since "10 minutes ago"
```

---

## 24. Instalación de Nginx

Nginx actuará como proxy inverso, sirviendo la aplicación en el puerto 80/443.

### Instalar Nginx

```bash
sudo apt install -y nginx
```

### Iniciar y Habilitar

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

### Verificar Instalación

Accede desde navegador: `http://IP_SERVIDOR`

**Deberías ver**: Página de bienvenida de Nginx.

### Configurar Sitio

```bash
sudo nano /etc/nginx/sites-available/gxregistry
```

**Contenido**:

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_redirect off;
        proxy_buffering off;

        proxy_connect_timeout 120;
        proxy_send_timeout 120;
        proxy_read_timeout 120;
    }
}
```

**Reemplaza** `tu-dominio.com` con tu dominio real.

### Habilitar Sitio

```bash
sudo ln -s /etc/nginx/sites-available/gxregistry /etc/nginx/sites-enabled/
```

### Eliminar Sitio Default (Opcional)

```bash
sudo rm /etc/nginx/sites-enabled/default
```

### Probar Configuración

```bash
sudo nginx -t
```

**Salida esperada**:

```
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### Reiniciar Nginx

```bash
sudo systemctl restart nginx
```

### Verificar

Accede desde navegador: `http://tu-dominio.com`

**Deberías ver**: La aplicación funcionando.

---

## 25. Configuración de HTTPS

Usaremos Let's Encrypt (certificado SSL gratuito) con Certbot.

### Instalar Certbot

```bash
sudo apt install -y certbot python3-certbot-nginx
```

### Obtener Certificado

```bash
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

**Proceso interactivo**:

1. **Email**: Ingresa tu email
2. **Términos**: Acepta (`A`)
3. **Newsletter**: Decide (`Y` o `N`)
4. **Redirect**: Selecciona `2` (Redirect HTTP to HTTPS)

**Salida esperada**:

```
Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/tu-dominio.com/fullchain.pem
Key is saved at: /etc/letsencrypt/live/tu-dominio.com/privkey.pem
```

### Verificar Auto-Renovación

```bash
sudo certbot renew --dry-run
```

**Salida esperada**:

```
Congratulations, all simulated renewals succeeded
```

### Verificar HTTPS

Accede: `https://tu-dominio.com`

**Deberías ver**: Candado verde en el navegador.

### Renovación Automática

Certbot configura un cron job automático. Verifica:

```bash
sudo systemctl list-timers | grep certbot
```

---

## 26. Configuración de Firewall

### Instalar UFW

```bash
sudo apt install -y ufw
```

### Configurar Reglas

```bash
# Permitir SSH (IMPORTANTE: hacerlo ANTES de habilitar UFW)
sudo ufw allow 22/tcp

# Permitir HTTP
sudo ufw allow 80/tcp

# Permitir HTTPS
sudo ufw allow 443/tcp

# Denegar todo lo demás
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

### Habilitar Firewall

```bash
sudo ufw enable
```

Confirma con `y`.

### Verificar Estado

```bash
sudo ufw status verbose
```

**Salida esperada**:

```
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
443/tcp                    ALLOW       Anywhere
```

### Permitir PostgreSQL Solo Localmente

PostgreSQL ya escucha solo en localhost. No es necesario abrir puerto 5432.

---

## 27. Backups Automáticos

### Script de Backup

```bash
sudo nano /home/gxapp/backup_database.sh
```

**Contenido**:

```bash
#!/bin/bash

# Configuración
DB_NAME="gx_object_registry"
DB_USER="gxuser"
BACKUP_DIR="/home/gxapp/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/gxregistry_$DATE.sql.gz"

# Crear directorio si no existe
mkdir -p $BACKUP_DIR

# Realizar backup
PGPASSWORD='contraseña_produccion' pg_dump -U $DB_USER -h localhost $DB_NAME | gzip > $BACKUP_FILE

# Eliminar backups antiguos (mantener últimos 7 días)
find $BACKUP_DIR -name "gxregistry_*.sql.gz" -mtime +7 -delete

echo "Backup completado: $BACKUP_FILE"
```

**Reemplaza** `contraseña_produccion` con la contraseña real.

### Dar Permisos

```bash
chmod +x /home/gxapp/backup_database.sh
```

### Probar Backup

```bash
/home/gxapp/backup_database.sh
```

Verifica:

```bash
ls -lh /home/gxapp/backups/
```

### Configurar Cron

```bash
crontab -e
```

Agrega al final:

```cron
# Backup diario a las 3 AM
0 3 * * * /home/gxapp/backup_database.sh >> /var/log/backup.log 2>&1
```

### Restaurar Backup

```bash
gunzip < /home/gxapp/backups/gxregistry_FECHA.sql.gz | psql -U gxuser -d gx_object_registry
```

---

## 28. Monitoreo y Logs

### Logs de la Aplicación

```bash
# Ver logs en tiempo real
sudo journalctl -u gxregistry -f

# Logs de las últimas 24 horas
sudo journalctl -u gxregistry --since "24 hours ago"

# Logs con errores
sudo journalctl -u gxregistry -p err
```

### Logs de Nginx

```bash
# Access logs
sudo tail -f /var/log/nginx/access.log

# Error logs
sudo tail -f /var/log/nginx/error.log
```

### Logs de PostgreSQL

```bash
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

### Monitorear Recursos

**Ver uso de CPU y RAM**:

```bash
htop
```

**Ver uso de disco**:

```bash
df -h
```

**Ver conexiones activas**:

```bash
sudo netstat -tulpn | grep :8000
```

---

## 29. Actualizaciones del Sistema

### Procedimiento Seguro

**1. Hacer Backup**:

```bash
/home/gxapp/backup_database.sh
```

**2. Descargar Cambios**:

```bash
cd /home/gxapp/apps/gx-object-registry
git pull origin main
```

**3. Activar Entorno Virtual**:

```bash
source venv/bin/activate
```

**4. Actualizar Dependencias**:

```bash
pip install -r requirements.txt --upgrade
```

**5. Ejecutar Migraciones**:

```bash
alembic upgrade head
```

**6. Reiniciar Servicio**:

```bash
sudo systemctl restart gxregistry
```

**7. Verificar Logs**:

```bash
sudo journalctl -u gxregistry -f
```

**8. Verificar Aplicación**:

Accede a `https://tu-dominio.com` y prueba funcionalidades.

### Si Algo Sale Mal

**Revertir a backup**:

```bash
gunzip < /home/gxapp/backups/ultimo_backup.sql.gz | psql -U gxuser -d gx_object_registry
```

**Revertir código**:

```bash
git reset --hard HEAD~1
sudo systemctl restart gxregistry
```

---

## 30. Checklist Final

### Checklist de Instalación Local

```
✅ Python 3.11+ instalado
✅ PostgreSQL 15+ instalado
✅ Git instalado
✅ Repositorio clonado
✅ Entorno virtual creado y activado
✅ Dependencias instaladas
✅ Archivo .env configurado
✅ Base de datos creada
✅ Usuario de BD creado
✅ Migraciones ejecutadas
✅ Datos iniciales cargados
✅ Usuario administrador creado
✅ Servidor iniciado exitosamente
✅ Login funciona
✅ Puedo crear objetos
```

### Checklist de Producción

```
✅ Servidor Ubuntu 22.04 configurado
✅ Usuario de aplicación creado
✅ PostgreSQL instalado y configurado
✅ Base de datos y usuario creados
✅ Proyecto clonado en /home/gxapp/apps/
✅ Entorno virtual creado
✅ Dependencias instaladas (incluyendo gunicorn)
✅ .env configurado con valores de producción
✅ SECRET_KEY generada y única
✅ Migraciones ejecutadas
✅ Datos iniciales cargados
✅ Usuario admin creado
✅ Servicio systemd creado y habilitado
✅ Servicio corriendo correctamente
✅ Nginx instalado y configurado
✅ Sitio Nginx habilitado
✅ Aplicación accesible vía HTTP
✅ Certbot instalado
✅ Certificado SSL obtenido
✅ HTTPS funcionando
✅ Redirección HTTP → HTTPS activa
✅ Firewall configurado (UFW)
✅ Puertos 22, 80, 443 abiertos
✅ Script de backup creado
✅ Cron de backup configurado
✅ Logs accesibles y funcionando
✅ Procedimiento de actualización documentado
```

### URLs Importantes

**Desarrollo**:
- Aplicación: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

**Producción**:
- Aplicación: `https://tu-dominio.com`
- API Docs: `https://tu-dominio.com/docs`
- Health Check: `https://tu-dominio.com/health`

### Comandos de Referencia Rápida

**Desarrollo**:
```bash
# Activar entorno
source venv/bin/activate

# Iniciar servidor
uvicorn src.main:app --reload

# Migraciones
alembic upgrade head

# Tests
pytest
```

**Producción**:
```bash
# Ver logs
sudo journalctl -u gxregistry -f

# Reiniciar servicio
sudo systemctl restart gxregistry

# Estado del servicio
sudo systemctl status gxregistry

# Backup manual
/home/gxapp/backup_database.sh

# Actualizar aplicación
cd /home/gxapp/apps/gx-object-registry
git pull
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
sudo systemctl restart gxregistry
```

### Recursos Adicionales

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org)
- [Alembic Documentation](https://alembic.sqlalchemy.org)

---

## Conclusión

Has completado la instalación de **GeneXus Object Registry** tanto en desarrollo como en producción.

### Próximos Pasos

1. **Personaliza la aplicación** según tus necesidades
2. **Importa tus objetos GeneXus** desde CSV
3. **Configura backups adicionales** (offsite)
4. **Implementa monitoreo** (Prometheus, Grafana)
5. **Configura alertas** (email, Slack)
6. **Documenta tu flujo de trabajo** específico

### Soporte

Si encuentras problemas:

1. Revisa los logs de la aplicación
2. Consulta la sección [18. Solución de Problemas](#18-solución-de-problemas-comunes)
3. Verifica que seguiste todos los pasos
4. Busca el error exacto en Google/StackOverflow

---

**¡Felicitaciones por completar la instalación!** 🎉

---

**Documento creado**: Agosto 2026
**Versión**: 1.0
**Última actualización**: 2026-08-03

**FIN DEL DOCUMENTO**
