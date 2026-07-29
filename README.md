# GeneXus Object Registry

Sistema para administrar información básica sobre objetos de GeneXus.

## Características

- ✅ Administración de tipos de objetos GeneXus (CRUD)
- ✅ Administración de objetos GeneXus (CRUD)
- ✅ Importación masiva desde archivos CSV
- ✅ Búsqueda y filtrado avanzado
- ✅ API REST documentada con OpenAPI/Swagger
- ✅ Validación automática de datos
- ✅ Detección de duplicados

## Stack Tecnológico

- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0 (async)
- **Migrations**: Alembic
- **Validation**: Pydantic V2
- **Testing**: pytest
- **Containerization**: Docker + docker-compose

## Requisitos Previos

- Python 3.11 o superior
- PostgreSQL 15 o superior (o Docker)
- Git

## Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd gx-object-registry
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

### 3. Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus configuraciones.

### 6. Iniciar base de datos (con Docker)

```bash
docker-compose up -d postgres
```

### 7. Ejecutar migraciones

```bash
alembic upgrade head
```

### 8. Iniciar servidor

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Uso

### Acceder a la documentación de la API

Una vez iniciado el servidor, accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints principales

#### Object Types

```
POST   /api/object-types       # Crear tipo
GET    /api/object-types       # Listar tipos
GET    /api/object-types/{id}  # Obtener por ID
PATCH  /api/object-types/{id}  # Actualizar
DELETE /api/object-types/{id}  # Eliminar
```

#### GeneXus Objects

```
POST   /api/objects            # Crear objeto
GET    /api/objects            # Listar/buscar objetos
GET    /api/objects/{id}       # Obtener por ID
PATCH  /api/objects/{id}       # Actualizar
DELETE /api/objects/{id}       # Eliminar
```

#### Import

```
POST   /api/objects/import/csv # Importar desde CSV
```

## Formato del CSV

El archivo CSV debe tener 3 columnas separadas por punto y coma (`;`):

```csv
name;description;objectType
AhrPr001;Recupera Tasa Interés;PROCEDURE
AhrTn001;Tipos de Cuentas;TRANSACTION
AhrTr001;Apertura de Cuenta;WORK_PANEL
```

### Reglas:

- **name**: Obligatorio, máximo 128 caracteres
- **description**: Opcional
- **objectType**: Debe ser un tipo existente en la base de datos

## Desarrollo

### Ejecutar tests

```bash
pytest
```

### Con cobertura

```bash
pytest --cov=src --cov-report=html
```

### Formatear código

```bash
black src/
```

### Linter

```bash
ruff check src/
```

### Type checking

```bash
mypy src/
```

## Docker

### Levantar todo el stack

```bash
docker-compose up
```

### Solo base de datos

```bash
docker-compose up -d postgres
```

### Reconstruir imágenes

```bash
docker-compose up --build
```

## Estructura del Proyecto

```
gx-object-registry/
├── src/                    # Código fuente
│   ├── main.py            # Punto de entrada
│   ├── shared/            # Componentes compartidos
│   ├── object_types/      # Módulo de tipos
│   ├── genexus_objects/   # Módulo de objetos
│   └── imports/           # Módulo de importación
├── tests/                 # Pruebas
├── alembic/              # Migraciones
├── documentation.md      # Documentación de diseño
├── guia.md              # Guía de estructura
└── requirements.txt     # Dependencias
```

## Documentación Adicional

- [documentation.md](documentation.md) - Diseño arquitectónico completo
- [guia.md](guia.md) - Guía de estructura del proyecto

## Licencia

[Definir licencia]

## Autor

[Tu nombre]
