# ANÁLISIS Y DISEÑO ARQUITECTÓNICO
## Sistema de Administración de Objetos GeneXus

---

## 1. RESUMEN EJECUTIVO

### 1.1 Visión General
Sistema monolítico modular para administrar información básica sobre objetos de GeneXus, permitiendo registro manual e importación masiva desde archivos CSV.

### 1.2 Alcance Confirmado
- ✅ Administración de tipos de objetos (CRUD)
- ✅ Administración de objetos GeneXus (CRUD)
- ✅ Importación CSV con 3 columnas: `name`, `description`, `objectType`
- ✅ Búsqueda y filtrado de objetos
- ✅ Validación de duplicados
- ✅ API REST documentada
- ❌ NO lectura directa de archivos binarios GeneXus
- ❌ NO microservicios
- ❌ NO tablas de auditoría/histórico (versión inicial)
- ❌ NO creación automática de tipos durante importación

### 1.3 Principios de Diseño
- **Simplicidad**: Arquitectura en capas sin sobredimensionamiento
- **Mantenibilidad**: Código limpio, modular y bien documentado
- **Extensibilidad**: Preparado para evolucionar sin refactoring masivo
- **Robustez**: Validaciones exhaustivas y manejo de errores profesional

---

## 2. ARQUITECTURA PROPUESTA

### 2.1 Estilo Arquitectónico
**Monolito Modular con Arquitectura en Capas**

```
┌─────────────────────────────────────────────────────┐
│           PRESENTATION LAYER (API REST)             │
│  Controllers │ DTOs │ OpenAPI/Swagger │ Validation │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│            APPLICATION LAYER (Use Cases)            │
│  CreateObjectType │ ImportCSV │ SearchObjects │...  │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│              DOMAIN LAYER (Business Logic)          │
│  Entities │ Domain Services │ Business Rules │...   │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│         INFRASTRUCTURE LAYER (Data Access)          │
│  Repositories │ Database │ File Processing │ Log    │
└─────────────────────────────────────────────────────┘
```

### 2.2 Módulos Funcionales

```
src/
├── object_types/              # Módulo de Tipos de Objetos
│   ├── domain/
│   │   ├── object_type.py           # Entidad de dominio
│   │   └── object_type_repository.py # Interfaz del repositorio
│   ├── application/
│   │   ├── create_object_type.py
│   │   ├── list_object_types.py
│   │   ├── get_object_type_by_id.py
│   │   ├── update_object_type.py
│   │   └── delete_object_type.py
│   ├── infrastructure/
│   │   └── sqlalchemy_object_type_repository.py
│   └── presentation/
│       ├── dtos.py
│       └── object_type_controller.py
│
├── genexus_objects/           # Módulo de Objetos GeneXus
│   ├── domain/
│   │   ├── genexus_object.py
│   │   └── genexus_object_repository.py
│   ├── application/
│   │   ├── create_genexus_object.py
│   │   ├── list_genexus_objects.py
│   │   ├── get_genexus_object_by_id.py
│   │   ├── update_genexus_object.py
│   │   ├── delete_genexus_object.py
│   │   └── search_genexus_objects.py
│   ├── infrastructure/
│   │   └── sqlalchemy_genexus_object_repository.py
│   └── presentation/
│       ├── dtos.py
│       └── genexus_object_controller.py
│
├── imports/                   # Módulo de Importación
│   ├── application/
│   │   └── import_csv_use_case.py
│   ├── domain/
│   │   ├── csv_parser.py
│   │   ├── import_validator.py
│   │   └── import_result.py
│   └── presentation/
│       ├── dtos.py
│       └── import_controller.py
│
└── shared/                    # Componentes Compartidos
    ├── database/
    │   ├── connection.py
    │   └── migrations/
    ├── errors/
    │   ├── error_codes.py
    │   ├── exceptions.py
    │   └── error_handler.py
    ├── validation/
    │   └── validators.py
    ├── logging/
    │   └── logger.py
    └── config/
        └── settings.py
```

---

## 3. DISEÑO DE BASE DE DATOS

### 3.1 Diagrama Entidad-Relación

```
┌────────────────────────┐
│    object_types        │
├────────────────────────┤
│ id (PK)                │
│ name (UNIQUE)          │
└────────────────────────┘
           │
           │ 1
           │
           │
           │ N
           ▼
┌────────────────────────┐
│  genexus_objects       │
├────────────────────────┤
│ id (PK)                │
│ name                   │
│ description            │
│ object_type_id (FK)    │
│ source_type            │
│ created_at             │
│ updated_at             │
└────────────────────────┘
UNIQUE (name, object_type_id)
```

### 3.2 Tabla `object_types`

#### Definición SQL (PostgreSQL)

```sql
CREATE TABLE object_types (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_object_types_name UNIQUE (name),
    CONSTRAINT ck_object_types_name_not_empty CHECK (TRIM(name) <> '')
);

-- Índice para búsquedas case-insensitive
CREATE UNIQUE INDEX idx_object_types_name_lower ON object_types (LOWER(name));

-- Trigger para actualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_object_types_updated_at BEFORE UPDATE
    ON object_types FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

#### Especificación de Campos

| Campo       | Tipo         | Nulo | Descripción                              | Validaciones                    |
|-------------|--------------|------|------------------------------------------|---------------------------------|
| `id`        | UUID         | NO   | Identificador único                      | PK, auto-generado               |
| `name`      | VARCHAR(100) | NO   | Nombre del tipo de objeto                | UNIQUE (case-insensitive), TRIM |
| `created_at`| TIMESTAMP    | NO   | Fecha de creación                        | DEFAULT CURRENT_TIMESTAMP       |
| `updated_at`| TIMESTAMP    | NO   | Fecha de última modificación             | AUTO-UPDATE via trigger         |

#### Restricciones Clave

1. **Unicidad Case-Insensitive**:
   - No pueden coexistir `PROCEDURE`, `Procedure`, `procedure`
   - Implementado mediante índice en `LOWER(name)`

2. **Integridad Referencial**:
   - No se puede eliminar un tipo con objetos relacionados (`ON DELETE RESTRICT`)

3. **Validación de Datos**:
   - `name` no puede ser cadena vacía después de `TRIM`

#### Datos Iniciales Sugeridos

```sql
INSERT INTO object_types (name) VALUES
    ('TRANSACTION'),
    ('PROCEDURE'),
    ('REPORT'),
    ('MENU'),
    ('WORK_PANEL'),
    ('WEB_PANEL'),
    ('TABLE'),
    ('DATA_VIEW'),
    ('FOLDER'),
    ('PROMPT'),
    ('EXTERNAL_PROGRAM'),
    ('STRUCTURED_DATA_TYPE');
```

**NOTA**: Estos valores NO se insertarán automáticamente. Deben registrarse manualmente vía API.

---

### 3.3 Tabla `genexus_objects`

#### Definición SQL (PostgreSQL)

```sql
CREATE TYPE source_type_enum AS ENUM ('MANUAL', 'CSV');

CREATE TABLE genexus_objects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(128) NOT NULL,
    description TEXT,
    object_type_id UUID NOT NULL,
    source_type source_type_enum NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_genexus_objects_object_type
        FOREIGN KEY (object_type_id)
        REFERENCES object_types(id)
        ON DELETE RESTRICT,

    CONSTRAINT uq_genexus_objects_name_type
        UNIQUE (name, object_type_id),

    CONSTRAINT ck_genexus_objects_name_not_empty
        CHECK (TRIM(name) <> '')
);

-- Índices para optimización de consultas
CREATE INDEX idx_genexus_objects_object_type_id ON genexus_objects(object_type_id);
CREATE INDEX idx_genexus_objects_source_type ON genexus_objects(source_type);
CREATE INDEX idx_genexus_objects_name ON genexus_objects(name);
CREATE INDEX idx_genexus_objects_created_at ON genexus_objects(created_at DESC);

-- Índice para búsqueda full-text (PostgreSQL)
CREATE INDEX idx_genexus_objects_name_trgm ON genexus_objects USING gin (name gin_trgm_ops);
CREATE INDEX idx_genexus_objects_description_trgm ON genexus_objects USING gin (description gin_trgm_ops);

-- Trigger para actualizar updated_at
CREATE TRIGGER update_genexus_objects_updated_at BEFORE UPDATE
    ON genexus_objects FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

#### Especificación de Campos

| Campo            | Tipo              | Nulo | Descripción                          | Validaciones                         |
|------------------|-------------------|------|--------------------------------------|--------------------------------------|
| `id`             | UUID              | NO   | Identificador único                  | PK, auto-generado                    |
| `name`           | VARCHAR(128)      | NO   | Nombre técnico del objeto            | NOT NULL, TRIM, max 128 chars        |
| `description`    | TEXT              | SÍ   | Descripción funcional                | NULL permitido, TRIM                 |
| `object_type_id` | UUID              | NO   | FK a object_types                    | FK, ON DELETE RESTRICT               |
| `source_type`    | ENUM              | NO   | Origen del registro (MANUAL/CSV)     | NOT NULL, valores predefinidos       |
| `created_at`     | TIMESTAMP         | NO   | Fecha de creación                    | DEFAULT CURRENT_TIMESTAMP            |
| `updated_at`     | TIMESTAMP         | NO   | Fecha de última modificación         | AUTO-UPDATE via trigger              |

#### Restricciones Clave

1. **Identidad Funcional**:
   - `UNIQUE (name, object_type_id)` - case sensitive por defecto
   - Permite `AhrTn001` como TRANSACTION y TABLE simultáneamente
   - **DECISIÓN PENDIENTE**: ¿Debe ser case-insensitive?

2. **Integridad Referencial**:
   - FK a `object_types` con `ON DELETE RESTRICT`
   - No se pueden crear objetos con tipos inexistentes

3. **Enumeración `source_type`**:
   - Valores: `MANUAL`, `CSV`
   - Implementado como ENUM nativo (PostgreSQL)
   - Alternativa para otros DB: CHECK constraint

---

## 4. DISEÑO DE ENTIDADES DE DOMINIO

### 4.1 Entidad `ObjectType`

```python
# domain/object_type.py
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class ObjectType:
    """
    Representa un tipo de objeto GeneXus.

    Invariantes:
    - name no puede estar vacío
    - name debe ser único (case-insensitive)
    """
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not self.name or not self.name.strip():
            raise ValueError("El nombre del tipo no puede estar vacío")

        if len(self.name) > 100:
            raise ValueError("El nombre del tipo no puede superar 100 caracteres")

    @staticmethod
    def create(name: str) -> 'ObjectType':
        """Factory method para crear un nuevo tipo de objeto"""
        normalized_name = name.strip()
        return ObjectType(
            id=uuid4(),
            name=normalized_name,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

    def update_name(self, new_name: str):
        """Actualiza el nombre del tipo"""
        self.name = new_name.strip()
        self.updated_at = datetime.utcnow()
        self._validate()
```

### 4.2 Entidad `GeneXusObject`

```python
# domain/genexus_object.py
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

class SourceType(str, Enum):
    MANUAL = "MANUAL"
    CSV = "CSV"

@dataclass
class GeneXusObject:
    """
    Representa un objeto de GeneXus.

    Invariantes:
    - name no puede estar vacío
    - name no puede superar 128 caracteres
    - object_type_id debe existir en object_types
    - La combinación (name, object_type_id) debe ser única
    """
    id: UUID
    name: str
    description: Optional[str]
    object_type_id: UUID
    source_type: SourceType
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not self.name or not self.name.strip():
            raise ValueError("El nombre del objeto no puede estar vacío")

        if len(self.name) > 128:
            raise ValueError("El nombre del objeto no puede superar 128 caracteres")

    @staticmethod
    def create_manual(
        name: str,
        object_type_id: UUID,
        description: Optional[str] = None
    ) -> 'GeneXusObject':
        """Factory method para crear objeto manualmente"""
        normalized_description = description.strip() if description else None

        return GeneXusObject(
            id=uuid4(),
            name=name.strip(),
            description=normalized_description if normalized_description else None,
            object_type_id=object_type_id,
            source_type=SourceType.MANUAL,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

    @staticmethod
    def create_from_csv(
        name: str,
        object_type_id: UUID,
        description: Optional[str] = None
    ) -> 'GeneXusObject':
        """Factory method para crear objeto desde CSV"""
        normalized_description = description.strip() if description else None

        return GeneXusObject(
            id=uuid4(),
            name=name.strip(),
            description=normalized_description if normalized_description else None,
            object_type_id=object_type_id,
            source_type=SourceType.CSV,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

    def update_description(self, new_description: Optional[str]):
        """Actualiza la descripción del objeto"""
        normalized = new_description.strip() if new_description else None
        self.description = normalized if normalized else None
        self.updated_at = datetime.utcnow()

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        object_type_id: Optional[UUID] = None
    ):
        """Actualiza múltiples campos del objeto"""
        if name is not None:
            self.name = name.strip()

        if description is not None:
            normalized = description.strip() if description else None
            self.description = normalized if normalized else None

        if object_type_id is not None:
            self.object_type_id = object_type_id

        self.updated_at = datetime.utcnow()
        self._validate()
```

---

## 5. DISEÑO DE DTOs

### 5.1 DTOs de `ObjectType`

```python
# presentation/object_types/dtos.py
from pydantic import BaseModel, Field, validator
from datetime import datetime
from uuid import UUID
from typing import Optional

class CreateObjectTypeRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip()

class UpdateObjectTypeRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip()

class ObjectTypeResponse(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ObjectTypeListResponse(BaseModel):
    items: list[ObjectTypeResponse]
    total: int
    page: int
    page_size: int
```

### 5.2 DTOs de `GeneXusObject`

```python
# presentation/genexus_objects/dtos.py
from pydantic import BaseModel, Field, validator
from datetime import datetime
from uuid import UUID
from typing import Optional
from enum import Enum

class SourceTypeDTO(str, Enum):
    MANUAL = "MANUAL"
    CSV = "CSV"

class CreateGeneXusObjectRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    description: Optional[str] = None
    object_type_id: UUID

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip()

    @validator('description')
    def normalize_description(cls, v):
        if v is None or not v.strip():
            return None
        return v.strip()

class UpdateGeneXusObjectRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=128)
    description: Optional[str] = None
    object_type_id: Optional[UUID] = None

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip() if v else None

    @validator('description')
    def normalize_description(cls, v):
        if v is None or not v.strip():
            return None
        return v.strip()

class GeneXusObjectResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    object_type_id: UUID
    object_type_name: str  # Denormalizado para conveniencia
    source_type: SourceTypeDTO
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SearchGeneXusObjectsRequest(BaseModel):
    search: Optional[str] = None
    name: Optional[str] = None
    object_type_id: Optional[UUID] = None
    source_type: Optional[SourceTypeDTO] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=50, ge=1, le=1000)
    sort_by: str = Field(default="name")
    sort_order: str = Field(default="asc", pattern="^(asc|desc)$")

class GeneXusObjectListResponse(BaseModel):
    items: list[GeneXusObjectResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
```

### 5.3 DTOs de Importación

```python
# presentation/imports/dtos.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class ImportStatus(str, Enum):
    COMPLETED = "COMPLETED"
    COMPLETED_WITH_ERRORS = "COMPLETED_WITH_ERRORS"
    FAILED = "FAILED"

class ErrorCode(str, Enum):
    OBJECT_TYPE_NOT_FOUND = "OBJECT_TYPE_NOT_FOUND"
    MISSING_NAME = "MISSING_NAME"
    MISSING_OBJECT_TYPE = "MISSING_OBJECT_TYPE"
    INVALID_NAME_LENGTH = "INVALID_NAME_LENGTH"
    DUPLICATE_IN_FILE = "DUPLICATE_IN_FILE"
    INVALID_ROW = "INVALID_ROW"
    DATABASE_ERROR = "DATABASE_ERROR"

class ImportError(BaseModel):
    row_number: int
    field: Optional[str]
    value: Optional[str]
    code: ErrorCode
    message: str

class ImportSummary(BaseModel):
    total_rows: int
    valid_rows: int
    created: int
    updated: int
    unchanged: int
    duplicates: int
    rejected: int

class ImportCSVResponse(BaseModel):
    file_name: str
    status: ImportStatus
    summary: ImportSummary
    errors: list[ImportError]
    processed_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## 6. DISEÑO DE CASOS DE USO

### 6.1 Módulo `ObjectTypes`

#### `CreateObjectType`
```python
Entrada:
  - name: str

Proceso:
  1. Normalizar name (trim)
  2. Validar longitud (max 100)
  3. Verificar que no exista (case-insensitive)
  4. Crear entidad ObjectType
  5. Persistir en repositorio

Salida:
  - ObjectType creado

Errores:
  - OBJECT_TYPE_ALREADY_EXISTS
  - INVALID_NAME_LENGTH
```

#### `ListObjectTypes`
```python
Entrada:
  - page: int (default 1)
  - page_size: int (default 50)

Proceso:
  1. Consultar repositorio con paginación
  2. Ordenar por name ASC

Salida:
  - Lista de ObjectTypes
  - Total de registros
```

#### `GetObjectTypeById`
```python
Entrada:
  - id: UUID

Proceso:
  1. Buscar en repositorio por ID

Salida:
  - ObjectType encontrado

Errores:
  - OBJECT_TYPE_NOT_FOUND
```

#### `UpdateObjectType`
```python
Entrada:
  - id: UUID
  - name: str

Proceso:
  1. Buscar ObjectType por ID
  2. Verificar que nuevo nombre no exista (case-insensitive)
  3. Actualizar entidad
  4. Persistir cambios

Salida:
  - ObjectType actualizado

Errores:
  - OBJECT_TYPE_NOT_FOUND
  - OBJECT_TYPE_ALREADY_EXISTS
```

#### `DeleteObjectType`
```python
Entrada:
  - id: UUID

Proceso:
  1. Buscar ObjectType por ID
  2. Verificar que no tenga objetos relacionados
  3. Eliminar del repositorio

Salida:
  - Confirmación de eliminación

Errores:
  - OBJECT_TYPE_NOT_FOUND
  - OBJECT_TYPE_IN_USE (si tiene objetos relacionados)
```

---

### 6.2 Módulo `GeneXusObjects`

#### `CreateGeneXusObject`
```python
Entrada:
  - name: str
  - description: Optional[str]
  - object_type_id: UUID

Proceso:
  1. Verificar que object_type_id existe
  2. Normalizar name y description
  3. Verificar duplicado (name + object_type_id)
  4. Crear entidad GeneXusObject con source_type=MANUAL
  5. Persistir en repositorio

Salida:
  - GeneXusObject creado

Errores:
  - OBJECT_TYPE_NOT_FOUND
  - OBJECT_ALREADY_EXISTS
  - INVALID_NAME_LENGTH
```

#### `SearchGeneXusObjects`
```python
Entrada:
  - search: Optional[str]
  - name: Optional[str]
  - object_type_id: Optional[UUID]
  - source_type: Optional[SourceType]
  - page: int
  - page_size: int
  - sort_by: str
  - sort_order: str

Proceso:
  1. Construir filtros dinámicos:
     - Si search: buscar en name OR description (case-insensitive)
     - Si name: filtrar por name exacto
     - Si object_type_id: filtrar por tipo
     - Si source_type: filtrar por origen
  2. Aplicar paginación
  3. Aplicar ordenamiento
  4. Ejecutar query en repositorio

Salida:
  - Lista de GeneXusObjects
  - Total de registros
  - Total de páginas

Errores:
  - Ninguno (query vacío es válido)
```

#### `UpdateGeneXusObject`
```python
Entrada:
  - id: UUID
  - name: Optional[str]
  - description: Optional[str]
  - object_type_id: Optional[UUID]

Proceso:
  1. Buscar GeneXusObject por ID
  2. Si cambia object_type_id, verificar que existe
  3. Si cambia name o object_type_id, verificar duplicado
  4. Actualizar entidad
  5. Actualizar updated_at
  6. Persistir cambios

Salida:
  - GeneXusObject actualizado

Errores:
  - OBJECT_NOT_FOUND
  - OBJECT_TYPE_NOT_FOUND
  - OBJECT_ALREADY_EXISTS
```

#### `DeleteGeneXusObject`
```python
Entrada:
  - id: UUID

Proceso:
  1. Buscar GeneXusObject por ID
  2. Eliminar del repositorio

Salida:
  - Confirmación de eliminación

Errores:
  - OBJECT_NOT_FOUND
```

---

### 6.3 Módulo `Imports`

#### `ImportCSV`

```python
Entrada:
  - file: UploadFile
  - max_file_size: int (configurable, default 50MB)
  - max_errors_to_report: int (configurable, default 100)

Proceso:
  1. VALIDACIÓN DE ARCHIVO
     - Verificar extensión .csv
     - Verificar tamaño < max_file_size
     - Verificar que no esté vacío
     - Guardar temporalmente (con nombre seguro)

  2. VALIDACIÓN DE ESTRUCTURA
     - Detectar encoding (UTF-8 preferido)
     - Leer encabezado
     - Validar columnas: name, description, objectType

  3. PRECARGA DE TIPOS
     - Cargar todos los object_types en memoria
     - Crear mapa: nombre_normalizado -> ObjectType

  4. PROCESAMIENTO FILA POR FILA
     Para cada fila (row_number, row_data):

       a) Extraer valores
          - name = row['name']
          - description = row['description']
          - object_type = row['objectType']

       b) Validar name
          - Aplicar trim()
          - Validar no vacío
          - Validar longitud <= 128
          - Si falla: agregar a errores y continuar

       c) Validar description
          - Aplicar trim()
          - Si vacío: convertir a None

       d) Buscar object_type
          - Normalizar: trim() + lower()
          - Buscar en mapa de tipos
          - Si no existe: agregar a errores y continuar

       e) Verificar duplicado dentro del CSV
          - Mantener set de (name, object_type_id) procesados
          - Si duplicado: agregar a errores, marcar como DUPLICATE_IN_FILE

       f) Verificar duplicado en BD
          - Buscar objeto existente por (name, object_type_id)

          Si NO EXISTE:
            - Crear nuevo GeneXusObject con source_type=CSV
            - Incrementar contador 'created'

          Si EXISTE:
            - Comparar description
            - Si es igual: incrementar contador 'unchanged'
            - Si es diferente:
                - Actualizar description
                - Incrementar contador 'updated'

  5. PERSISTENCIA
     - Utilizar batch inserts/updates (lotes de 100-500)
     - Commit por lotes
     - Si error crítico de BD: rollback del lote, agregar errores

  6. LIMPIEZA
     - Eliminar archivo temporal

  7. GENERAR REPORTE
     - Calcular summary
     - Limitar errores reportados a max_errors_to_report
     - Determinar status:
         - Si rejected = 0: COMPLETED
         - Si rejected > 0 pero valid_rows > 0: COMPLETED_WITH_ERRORS
         - Si valid_rows = 0: FAILED

Salida:
  - ImportCSVResponse con summary y errores

Errores Críticos (detienen proceso):
  - INVALID_FILE_EXTENSION
  - FILE_TOO_LARGE
  - INVALID_HEADER
  - INVALID_ENCODING

Errores por Fila (se reportan, proceso continúa):
  - MISSING_NAME
  - MISSING_OBJECT_TYPE
  - OBJECT_TYPE_NOT_FOUND
  - INVALID_NAME_LENGTH
  - DUPLICATE_IN_FILE
```

---

## 7. DISEÑO DE ENDPOINTS REST

### 7.1 Object Types

```
POST   /api/object-types
GET    /api/object-types
GET    /api/object-types/{id}
PATCH  /api/object-types/{id}
DELETE /api/object-types/{id}
```

#### `POST /api/object-types`
**Crear tipo de objeto**

Request:
```json
{
  "name": "PROCEDURE"
}
```

Response (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "PROCEDURE",
  "created_at": "2026-07-29T10:30:00Z",
  "updated_at": "2026-07-29T10:30:00Z"
}
```

Errores:
- 400 Bad Request: Validación fallida
- 409 Conflict: OBJECT_TYPE_ALREADY_EXISTS

---

#### `GET /api/object-types`
**Listar tipos de objetos**

Query params:
- `page` (int, default=1)
- `page_size` (int, default=50, max=1000)

Response (200 OK):
```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "PROCEDURE",
      "created_at": "2026-07-29T10:30:00Z",
      "updated_at": "2026-07-29T10:30:00Z"
    }
  ],
  "total": 12,
  "page": 1,
  "page_size": 50
}
```

---

#### `GET /api/object-types/{id}`
**Obtener tipo de objeto por ID**

Response (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "PROCEDURE",
  "created_at": "2026-07-29T10:30:00Z",
  "updated_at": "2026-07-29T10:30:00Z"
}
```

Errores:
- 404 Not Found: OBJECT_TYPE_NOT_FOUND

---

#### `PATCH /api/object-types/{id}`
**Actualizar tipo de objeto**

Request:
```json
{
  "name": "STORED_PROCEDURE"
}
```

Response (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "STORED_PROCEDURE",
  "created_at": "2026-07-29T10:30:00Z",
  "updated_at": "2026-07-29T14:45:00Z"
}
```

Errores:
- 404 Not Found: OBJECT_TYPE_NOT_FOUND
- 409 Conflict: OBJECT_TYPE_ALREADY_EXISTS

---

#### `DELETE /api/object-types/{id}`
**Eliminar tipo de objeto**

Response (204 No Content)

Errores:
- 404 Not Found: OBJECT_TYPE_NOT_FOUND
- 409 Conflict: OBJECT_TYPE_IN_USE

---

### 7.2 GeneXus Objects

```
POST   /api/objects
GET    /api/objects
GET    /api/objects/{id}
PATCH  /api/objects/{id}
DELETE /api/objects/{id}
```

#### `POST /api/objects`
**Crear objeto GeneXus manualmente**

Request:
```json
{
  "name": "AhrPr001",
  "description": "Recupera Tasa de Interés",
  "object_type_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

Response (201 Created):
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "name": "AhrPr001",
  "description": "Recupera Tasa de Interés",
  "object_type_id": "550e8400-e29b-41d4-a716-446655440000",
  "object_type_name": "PROCEDURE",
  "source_type": "MANUAL",
  "created_at": "2026-07-29T10:30:00Z",
  "updated_at": "2026-07-29T10:30:00Z"
}
```

Errores:
- 400 Bad Request: Validación fallida
- 404 Not Found: OBJECT_TYPE_NOT_FOUND
- 409 Conflict: OBJECT_ALREADY_EXISTS

---

#### `GET /api/objects`
**Buscar y filtrar objetos**

Query params:
- `search` (str): Busca en name y description (case-insensitive)
- `name` (str): Filtro exacto por nombre
- `object_type_id` (UUID): Filtro por tipo
- `source_type` (MANUAL|CSV): Filtro por origen
- `page` (int, default=1)
- `page_size` (int, default=50, max=1000)
- `sort_by` (str, default="name"): name|created_at|updated_at
- `sort_order` (asc|desc, default="asc")

Ejemplos:
```
GET /api/objects?search=interes
GET /api/objects?object_type_id=550e8400-e29b-41d4-a716-446655440000
GET /api/objects?source_type=CSV&page=2&page_size=100
GET /api/objects?sort_by=created_at&sort_order=desc
```

Response (200 OK):
```json
{
  "items": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "name": "AhrPr001",
      "description": "Recupera Tasa de Interés",
      "object_type_id": "550e8400-e29b-41d4-a716-446655440000",
      "object_type_name": "PROCEDURE",
      "source_type": "CSV",
      "created_at": "2026-07-29T10:30:00Z",
      "updated_at": "2026-07-29T10:30:00Z"
    }
  ],
  "total": 8470,
  "page": 1,
  "page_size": 50,
  "total_pages": 170
}
```

---

#### `GET /api/objects/{id}`
**Obtener objeto por ID**

Response (200 OK):
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "name": "AhrPr001",
  "description": "Recupera Tasa de Interés",
  "object_type_id": "550e8400-e29b-41d4-a716-446655440000",
  "object_type_name": "PROCEDURE",
  "source_type": "MANUAL",
  "created_at": "2026-07-29T10:30:00Z",
  "updated_at": "2026-07-29T10:30:00Z"
}
```

Errores:
- 404 Not Found: OBJECT_NOT_FOUND

---

#### `PATCH /api/objects/{id}`
**Actualizar objeto GeneXus**

Request (todos los campos son opcionales):
```json
{
  "name": "AhrPr002",
  "description": "Nueva descripción",
  "object_type_id": "770e8400-e29b-41d4-a716-446655440002"
}
```

Response (200 OK):
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "name": "AhrPr002",
  "description": "Nueva descripción",
  "object_type_id": "770e8400-e29b-41d4-a716-446655440002",
  "object_type_name": "TABLE",
  "source_type": "MANUAL",
  "created_at": "2026-07-29T10:30:00Z",
  "updated_at": "2026-07-29T15:20:00Z"
}
```

Errores:
- 404 Not Found: OBJECT_NOT_FOUND, OBJECT_TYPE_NOT_FOUND
- 409 Conflict: OBJECT_ALREADY_EXISTS

---

#### `DELETE /api/objects/{id}`
**Eliminar objeto GeneXus**

Response (204 No Content)

Errores:
- 404 Not Found: OBJECT_NOT_FOUND

---

### 7.3 Import

```
POST /api/objects/import/csv
```

#### `POST /api/objects/import/csv`
**Importar objetos desde archivo CSV**

Request:
```
Content-Type: multipart/form-data

file: objetos.csv
```

Configuración (vía headers o config):
- `X-Max-File-Size`: 52428800 (50MB default)
- `X-Max-Errors-To-Report`: 100 (default)

Response (200 OK - importación completada):
```json
{
  "file_name": "objetos.csv",
  "status": "COMPLETED",
  "summary": {
    "total_rows": 8500,
    "valid_rows": 8500,
    "created": 8200,
    "updated": 150,
    "unchanged": 150,
    "duplicates": 0,
    "rejected": 0
  },
  "errors": [],
  "processed_at": "2026-07-29T10:30:00Z"
}
```

Response (200 OK - importación con errores parciales):
```json
{
  "file_name": "objetos.csv",
  "status": "COMPLETED_WITH_ERRORS",
  "summary": {
    "total_rows": 8500,
    "valid_rows": 8470,
    "created": 8200,
    "updated": 100,
    "unchanged": 150,
    "duplicates": 10,
    "rejected": 30
  },
  "errors": [
    {
      "row_number": 125,
      "field": "objectType",
      "value": "PROCEDUR",
      "code": "OBJECT_TYPE_NOT_FOUND",
      "message": "El tipo de objeto 'PROCEDUR' no está registrado en el sistema."
    },
    {
      "row_number": 230,
      "field": "name",
      "value": "",
      "code": "MISSING_NAME",
      "message": "El nombre del objeto es obligatorio."
    },
    {
      "row_number": 455,
      "field": null,
      "value": "AhrPr001",
      "code": "DUPLICATE_IN_FILE",
      "message": "El objeto 'AhrPr001' con tipo 'PROCEDURE' aparece duplicado en el archivo."
    }
  ],
  "processed_at": "2026-07-29T10:30:00Z"
}
```

Errores críticos (detienen proceso):
- 400 Bad Request:
  - INVALID_FILE_EXTENSION
  - INVALID_HEADER
  - FILE_TOO_LARGE
  - INVALID_CSV
- 500 Internal Server Error: DATABASE_ERROR (crítico)

---

## 8. MANEJO DE ERRORES

### 8.1 Códigos de Error Estandarizados

```python
class ErrorCode(str, Enum):
    # Object Types
    OBJECT_TYPE_NOT_FOUND = "OBJECT_TYPE_NOT_FOUND"
    OBJECT_TYPE_ALREADY_EXISTS = "OBJECT_TYPE_ALREADY_EXISTS"
    OBJECT_TYPE_IN_USE = "OBJECT_TYPE_IN_USE"
    INVALID_OBJECT_TYPE_NAME = "INVALID_OBJECT_TYPE_NAME"

    # GeneXus Objects
    OBJECT_NOT_FOUND = "OBJECT_NOT_FOUND"
    OBJECT_ALREADY_EXISTS = "OBJECT_ALREADY_EXISTS"
    INVALID_OBJECT_NAME = "INVALID_OBJECT_NAME"
    INVALID_NAME_LENGTH = "INVALID_NAME_LENGTH"

    # Import
    INVALID_FILE = "INVALID_FILE"
    INVALID_FILE_EXTENSION = "INVALID_FILE_EXTENSION"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    INVALID_HEADER = "INVALID_HEADER"
    INVALID_ENCODING = "INVALID_ENCODING"
    INVALID_CSV = "INVALID_CSV"
    MISSING_NAME = "MISSING_NAME"
    MISSING_OBJECT_TYPE = "MISSING_OBJECT_TYPE"
    DUPLICATE_IN_FILE = "DUPLICATE_IN_FILE"
    INVALID_ROW = "INVALID_ROW"

    # System
    DATABASE_ERROR = "DATABASE_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"
```

### 8.2 Estructura de Respuesta de Error

```json
{
  "code": "OBJECT_TYPE_NOT_FOUND",
  "message": "El tipo de objeto no fue encontrado.",
  "details": {
    "object_type_id": "550e8400-e29b-41d4-a716-446655440000"
  },
  "timestamp": "2026-07-29T10:30:00Z",
  "path": "/api/object-types/550e8400-e29b-41d4-a716-446655440000"
}
```

### 8.3 Mapeo HTTP Status Codes

| Error Code                     | HTTP Status | Descripción                          |
|--------------------------------|-------------|--------------------------------------|
| *_NOT_FOUND                    | 404         | Recurso no existe                    |
| *_ALREADY_EXISTS               | 409         | Conflicto de unicidad                |
| *_IN_USE                       | 409         | No se puede eliminar (tiene refs)    |
| VALIDATION_ERROR               | 400         | Datos inválidos                      |
| INVALID_*                      | 400         | Validación de formato/estructura     |
| FILE_TOO_LARGE                 | 413         | Archivo excede límite                |
| DATABASE_ERROR                 | 500         | Error interno de BD                  |
| INTERNAL_ERROR                 | 500         | Error no categorizado                |

---

## 9. VALIDACIONES Y REGLAS DE NEGOCIO

### 9.1 Validaciones de `ObjectType`

| Campo  | Validación                                   | Mensaje de Error                                      |
|--------|----------------------------------------------|-------------------------------------------------------|
| `name` | Obligatorio                                  | "El nombre del tipo es obligatorio."                  |
| `name` | Después de `trim()` no puede estar vacío     | "El nombre del tipo no puede estar vacío."            |
| `name` | Longitud máxima: 100 caracteres              | "El nombre no puede superar 100 caracteres."          |
| `name` | Único (case-insensitive)                     | "Ya existe un tipo de objeto con ese nombre."         |

**Regla de Negocio**: No se puede eliminar un `ObjectType` que tiene `GeneXusObjects` relacionados.

---

### 9.2 Validaciones de `GeneXusObject`

| Campo            | Validación                               | Mensaje de Error                                      |
|------------------|------------------------------------------|-------------------------------------------------------|
| `name`           | Obligatorio                              | "El nombre del objeto es obligatorio."                |
| `name`           | Después de `trim()` no vacío             | "El nombre del objeto no puede estar vacío."          |
| `name`           | Longitud máxima: 128 caracteres          | "El nombre no puede superar 128 caracteres."          |
| `description`    | Opcional                                 | -                                                     |
| `description`    | Si vacío, convertir a `NULL`             | -                                                     |
| `object_type_id` | Obligatorio                              | "El tipo de objeto es obligatorio."                   |
| `object_type_id` | Debe existir en `object_types`           | "El tipo de objeto seleccionado no existe."           |
| Unicidad         | `(name, object_type_id)` único           | "Ya existe un objeto con ese nombre y tipo."          |

**Regla de Negocio**: El mismo `name` puede existir múltiples veces si pertenece a diferentes tipos.

Ejemplo válido:
```
AhrTn001 - TRANSACTION ✓
AhrTn001 - TABLE        ✓
```

---

### 9.3 Validaciones de Importación CSV

#### Validaciones de Archivo

| Aspecto       | Validación                           | Error                         |
|---------------|--------------------------------------|-------------------------------|
| Extensión     | Debe ser `.csv`                      | INVALID_FILE_EXTENSION        |
| Tamaño        | Máximo configurable (50MB default)   | FILE_TOO_LARGE                |
| Contenido     | No puede estar vacío                 | INVALID_FILE                  |
| Encoding      | UTF-8 preferido, detectar otros      | INVALID_ENCODING              |

#### Validaciones de Estructura

| Aspecto       | Validación                           | Error                         |
|---------------|--------------------------------------|-------------------------------|
| Encabezado    | Debe contener: name, description, objectType | INVALID_HEADER        |
| Delimitador   | Punto y coma `;`                     | INVALID_CSV                   |

#### Validaciones por Fila

| Campo         | Validación                           | Error Code                    |
|---------------|--------------------------------------|-------------------------------|
| `name`        | Obligatorio                          | MISSING_NAME                  |
| `name`        | Después de `trim()` no vacío         | MISSING_NAME                  |
| `name`        | Longitud <= 128                      | INVALID_NAME_LENGTH           |
| `objectType`  | Obligatorio                          | MISSING_OBJECT_TYPE           |
| `objectType`  | Debe existir en BD (case-insensitive)| OBJECT_TYPE_NOT_FOUND         |
| Duplicado     | No repetir (name + objectType) en CSV| DUPLICATE_IN_FILE             |

---

### 9.4 Estrategia de Duplicados en Importación

```
Para cada fila válida del CSV:

1. Extraer: name, description, object_type_id

2. Buscar objeto existente:
   WHERE name = :name AND object_type_id = :object_type_id

3. Evaluar:

   CASO A: NO EXISTE
     → Crear nuevo objeto
     → source_type = CSV
     → Incrementar contador 'created'

   CASO B: EXISTE CON MISMA DESCRIPCIÓN
     → No modificar
     → Incrementar contador 'unchanged'

   CASO C: EXISTE CON DESCRIPCIÓN DIFERENTE
     → Actualizar description
     → Actualizar updated_at
     → Incrementar contador 'updated'
```

**Justificación**: Esta estrategia permite reimportar el CSV de forma idempotente, actualizando solo descripciones modificadas.

---

## 10. DISEÑO DE REPOSITORIOS

### 10.1 Interfaz `ObjectTypeRepository`

```python
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

class ObjectTypeRepository(ABC):

    @abstractmethod
    async def create(self, object_type: ObjectType) -> ObjectType:
        """Crea un nuevo tipo de objeto"""
        pass

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[ObjectType]:
        """Busca un tipo por ID"""
        pass

    @abstractmethod
    async def find_by_name(self, name: str) -> Optional[ObjectType]:
        """Busca un tipo por nombre (case-insensitive)"""
        pass

    @abstractmethod
    async def exists_by_name(self, name: str) -> bool:
        """Verifica si existe un tipo con ese nombre"""
        pass

    @abstractmethod
    async def list_all(self, page: int, page_size: int) -> tuple[List[ObjectType], int]:
        """Lista tipos con paginación. Retorna (items, total)"""
        pass

    @abstractmethod
    async def update(self, object_type: ObjectType) -> ObjectType:
        """Actualiza un tipo de objeto"""
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> None:
        """
        Elimina un tipo de objeto.
        Lanza ObjectTypeInUseError si tiene objetos relacionados.
        """
        pass

    @abstractmethod
    async def has_related_objects(self, id: UUID) -> bool:
        """Verifica si el tipo tiene objetos relacionados"""
        pass
```

---

### 10.2 Interfaz `GeneXusObjectRepository`

```python
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

class GeneXusObjectRepository(ABC):

    @abstractmethod
    async def create(self, obj: GeneXusObject) -> GeneXusObject:
        """Crea un nuevo objeto"""
        pass

    @abstractmethod
    async def bulk_create(self, objects: List[GeneXusObject]) -> List[GeneXusObject]:
        """Crea múltiples objetos en lote"""
        pass

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[GeneXusObject]:
        """Busca un objeto por ID"""
        pass

    @abstractmethod
    async def find_by_name_and_type(
        self,
        name: str,
        object_type_id: UUID
    ) -> Optional[GeneXusObject]:
        """Busca objeto por nombre y tipo"""
        pass

    @abstractmethod
    async def exists_by_name_and_type(
        self,
        name: str,
        object_type_id: UUID
    ) -> bool:
        """Verifica si existe un objeto con ese nombre y tipo"""
        pass

    @abstractmethod
    async def search(
        self,
        search: Optional[str] = None,
        name: Optional[str] = None,
        object_type_id: Optional[UUID] = None,
        source_type: Optional[SourceType] = None,
        page: int = 1,
        page_size: int = 50,
        sort_by: str = "name",
        sort_order: str = "asc"
    ) -> tuple[List[GeneXusObject], int]:
        """
        Búsqueda avanzada con filtros.
        Retorna (items, total)
        """
        pass

    @abstractmethod
    async def update(self, obj: GeneXusObject) -> GeneXusObject:
        """Actualiza un objeto"""
        pass

    @abstractmethod
    async def bulk_update(self, objects: List[GeneXusObject]) -> List[GeneXusObject]:
        """Actualiza múltiples objetos en lote"""
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> None:
        """Elimina un objeto"""
        pass
```

---

## 11. PLAN DE PRUEBAS

### 11.1 Pruebas Unitarias

#### `ObjectType` Domain Tests
- ✅ Crear ObjectType válido
- ✅ Rechazar nombre vacío
- ✅ Rechazar nombre > 100 caracteres
- ✅ Normalizar espacios en nombre
- ✅ Actualizar nombre correctamente

#### `GeneXusObject` Domain Tests
- ✅ Crear objeto manual válido
- ✅ Crear objeto desde CSV válido
- ✅ Rechazar nombre vacío
- ✅ Rechazar nombre > 128 caracteres
- ✅ Normalizar description (trim, null si vacío)
- ✅ Actualizar campos correctamente

#### Use Cases Tests
- ✅ `CreateObjectType`: creación exitosa, duplicado
- ✅ `DeleteObjectType`: sin relaciones, con relaciones (debe fallar)
- ✅ `CreateGeneXusObject`: exitoso, tipo inexistente, duplicado
- ✅ `SearchGeneXusObjects`: filtros diversos, paginación

---

### 11.2 Pruebas de Integración

#### API Object Types
- ✅ POST /api/object-types - creación exitosa
- ✅ POST /api/object-types - duplicado (409)
- ✅ GET /api/object-types - paginación
- ✅ DELETE /api/object-types/{id} - con objetos relacionados (409)

#### API GeneXus Objects
- ✅ POST /api/objects - creación manual exitosa
- ✅ POST /api/objects - tipo inexistente (404)
- ✅ GET /api/objects?search=tasa - búsqueda por texto
- ✅ GET /api/objects?object_type_id={id} - filtro por tipo
- ✅ PATCH /api/objects/{id} - actualización parcial

#### API Import
- ✅ POST /api/objects/import/csv - archivo válido completo
- ✅ POST /api/objects/import/csv - archivo con errores parciales
- ✅ POST /api/objects/import/csv - encabezado inválido (400)
- ✅ POST /api/objects/import/csv - extensión incorrecta (400)
- ✅ POST /api/objects/import/csv - archivo demasiado grande (413)

---

### 11.3 Casos de Prueba CSV

#### CSV Válido Básico
```csv
name;description;objectType
AhrPr001;Recupera Tasa Interés;PROCEDURE
AhrTn001;Tipos de Cuentas;TRANSACTION
AhrTr001;Apertura de Cuenta;WORK_PANEL
```
**Esperado**: 3 creados, 0 errores

---

#### CSV con Descripciones Vacías
```csv
name;description;objectType
AhrPr002;;PROCEDURE
AhrPr003;Descripción válida;PROCEDURE
```
**Esperado**: 2 creados, description de AhrPr002 = NULL

---

#### CSV con Tipo Inexistente
```csv
name;description;objectType
AhrPr004;Test;PROCEDURE
AhrPr005;Test;INVALID_TYPE
```
**Esperado**: 1 creado, 1 rechazado (OBJECT_TYPE_NOT_FOUND)

---

#### CSV con Nombre Vacío
```csv
name;description;objectType
;Descripción sin nombre;PROCEDURE
AhrPr006;Válido;PROCEDURE
```
**Esperado**: 1 creado, 1 rechazado (MISSING_NAME)

---

#### CSV con Duplicados Internos
```csv
name;description;objectType
AhrPr007;Primera aparición;PROCEDURE
AhrPr007;Segunda aparición;PROCEDURE
```
**Esperado**: 1 creado, 1 rechazado (DUPLICATE_IN_FILE)

---

#### CSV con Objeto Existente (sin cambios)
```
Precondición: AhrPr008 ya existe con descripción "Original"

CSV:
name;description;objectType
AhrPr008;Original;PROCEDURE
```
**Esperado**: 0 creados, 1 unchanged

---

#### CSV con Objeto Existente (descripción modificada)
```
Precondición: AhrPr009 ya existe con descripción "Original"

CSV:
name;description;objectType
AhrPr009;Nueva descripción;PROCEDURE
```
**Esperado**: 0 creados, 1 updated

---

#### CSV con Acentos y Caracteres Especiales
```csv
name;description;objectType
AñoPr001;Gestión de año fiscal;PROCEDURE
CálculoIVA;Cálculo de impuestos (IVA 21%);TABLE
```
**Esperado**: 2 creados correctamente con encoding UTF-8

---

#### CSV con Punto y Coma en Descripción
```csv
name;description;objectType
AhrPr010;"Procesa cuentas; movimientos y saldos";PROCEDURE
```
**Esperado**: 1 creado, description = "Procesa cuentas; movimientos y saldos"

---

#### CSV con Nombre Demasiado Largo
```csv
name;description;objectType
EstoEsUnNombreDeObjetoExcesivamenteLargoQueExcedeElLimiteDe128CaracteresPermitidosPorLaValidacionDelSistemaYDeberiaSerRechazadoAutomaticamente;Descripción;PROCEDURE
```
**Esperado**: 0 creados, 1 rechazado (INVALID_NAME_LENGTH)

---

#### CSV Grande (Performance)
```
8500 filas válidas
```
**Esperado**: Procesamiento en < 30 segundos, batch inserts, memoria controlada

---

### 11.4 Pruebas de Seguridad

- ✅ SQL Injection en búsquedas
- ✅ Path Traversal en nombres de archivo
- ✅ CSV Injection (fórmulas maliciosas en descripción)
- ✅ Tamaño de archivo excesivo
- ✅ Encoding malicioso

---

## 12. RIESGOS TÉCNICOS IDENTIFICADOS

### 12.1 Riesgo: Unicidad Case-Insensitive de `name` en `genexus_objects`

**Descripción**: La especificación indica que la unicidad de `(name, object_type_id)` debe ser case-insensitive para evitar duplicados como `AhrPr001` y `ahrpr001`.

**Problema**: PostgreSQL por defecto hace comparaciones case-sensitive en restricciones UNIQUE.

**Soluciones**:

1. **Índice en `LOWER(name)` + `object_type_id`**:
   ```sql
   CREATE UNIQUE INDEX idx_genexus_objects_name_type_lower
   ON genexus_objects (LOWER(name), object_type_id);
   ```
   ⚠️ No reemplaza la restricción UNIQUE, solo previene duplicados.

2. **Columna computada normalizada**:
   ```sql
   ALTER TABLE genexus_objects ADD COLUMN name_normalized VARCHAR(128)
   GENERATED ALWAYS AS (LOWER(name)) STORED;

   CREATE UNIQUE INDEX idx_genexus_objects_name_normalized_type
   ON genexus_objects (name_normalized, object_type_id);
   ```
   ✅ Más robusto, garantiza unicidad case-insensitive.

**Decisión Pendiente**: ¿Debe `name` ser case-insensitive? Si no, eliminar este requerimiento.

---

### 12.2 Riesgo: Búsqueda Insensible a Acentos

**Descripción**: La especificación menciona "Analiza si también conviene hacerla insensible a acentos".

**Problema**: PostgreSQL requiere configuración adicional (collations o extensión `unaccent`).

**Solución**:
```sql
CREATE EXTENSION IF NOT EXISTS unaccent;

-- Búsqueda sin acentos
SELECT * FROM genexus_objects
WHERE unaccent(name) ILIKE unaccent('%interes%');
```

**Impacto en Performance**: Las funciones `unaccent()` impiden uso de índices normales. Requiere índices funcionales.

**Decisión Pendiente**: ¿Es necesario búsqueda insensible a acentos? Si sí, implementar índices GIN con pg_trgm.

---

### 12.3 Riesgo: Importación de Archivos CSV Muy Grandes

**Descripción**: CSV con 50,000+ filas puede causar:
- Alto consumo de memoria
- Timeout de conexión HTTP
- Transacciones largas que bloquean tablas

**Mitigación**:
1. **Procesamiento por lotes (batches)**:
   - Leer 500-1000 filas a la vez
   - Commit por lote
   - Liberar memoria entre lotes

2. **Streaming de archivo**:
   - No cargar todo el archivo en memoria
   - Usar generadores/iteradores

3. **Timeout configurable**:
   - Permitir hasta 5-10 minutos para importaciones grandes

4. **Procesamiento asíncrono (futuro)**:
   - Para CSV > 10MB, usar job queue (Celery, RQ)
   - Notificar al usuario cuando termine

**Decisión**: Para MVP, procesamiento sincrónico con batches. Evaluar async en v2 si se requiere.

---

### 12.4 Riesgo: Codificación de Archivos CSV

**Descripción**: CSV puede venir en UTF-8, ISO-8859-1, Windows-1252, etc.

**Mitigación**:
1. Detectar automáticamente encoding con biblioteca `chardet`
2. Intentar UTF-8 primero, fallback a ISO-8859-1
3. Reportar error si no se puede decodificar

**Código de ejemplo**:
```python
import chardet

def detect_encoding(file_bytes: bytes) -> str:
    result = chardet.detect(file_bytes)
    return result['encoding']
```

---

### 12.5 Riesgo: Concurrencia en Importación

**Descripción**: Dos usuarios importan simultáneamente el mismo objeto.

**Escenario**:
```
Usuario A importa: AhrPr001 - PROCEDURE
Usuario B importa: AhrPr001 - PROCEDURE (mismo tiempo)

Ambos verifican que no existe → race condition → ambos intentan insertar
```

**Mitigación**:
1. **Nivel de Aislamiento**: Usar `SERIALIZABLE` o `REPEATABLE READ`
2. **Manejo de Excepciones**: Capturar `IntegrityError` de violación de UNIQUE
3. **Retry Logic**: Si falla por duplicado, reintentar con SELECT primero

**Decisión**: Para MVP, capturar `IntegrityError` y reportar como error de importación.

---

## 13. RECOMENDACIÓN DE STACK TECNOLÓGICO

Dado que mencionaste **Python**, estas son mis recomendaciones profesionales:

### 13.1 Stack Recomendado

```
Backend Framework: FastAPI
ORM:               SQLAlchemy 2.0 (async)
Database:          PostgreSQL 15+
Migration:         Alembic
Validation:        Pydantic V2
CSV Parser:        pandas / csv (stdlib)
Testing:           pytest + pytest-asyncio
API Docs:          OpenAPI (built-in FastAPI)
Logging:           structlog
Config:            pydantic-settings
Containerization:  Docker + docker-compose
```

### 13.2 Justificación

#### ✅ **FastAPI** (Framework)
- **Pro**: Documentación automática OpenAPI/Swagger
- **Pro**: Validación automática con Pydantic
- **Pro**: Async nativo para mejor performance
- **Pro**: Excelente para APIs REST empresariales
- **Pro**: Typing completo, menos errores
- **Contra**: Curva de aprendizaje moderada si no conoces async

#### ✅ **SQLAlchemy 2.0** (ORM)
- **Pro**: ORM más maduro de Python
- **Pro**: Soporte async completo
- **Pro**: Relaciones complejas bien manejadas
- **Pro**: Migraciones estables con Alembic
- **Contra**: Sintaxis más verbosa que ORMs simples

#### ✅ **PostgreSQL** (Database)
- **Pro**: ENUM nativo para `source_type`
- **Pro**: UUID nativo
- **Pro**: Índices GIN para búsqueda full-text
- **Pro**: Extensión `unaccent` para búsquedas sin acentos
- **Pro**: `ON DELETE RESTRICT` robusto
- **Pro**: Case-insensitive con collations/índices funcionales
- **Contra**: Requiere instalación/servicio (mitigado con Docker)

#### ✅ **Pydantic** (Validation)
- **Pro**: Integrado con FastAPI
- **Pro**: Validación declarativa de DTOs
- **Pro**: Serialización automática
- **Pro**: Error messages claros

#### ✅ **pytest** (Testing)
- **Pro**: Estándar de facto en Python
- **Pro**: Fixtures poderosos
- **Pro**: Plugins para async, coverage, etc.
- **Pro**: Sintaxis simple y clara

---

### 13.3 Alternativas Consideradas

#### Django REST Framework
❌ **Descartado**:
- Demasiado monolítico para este caso
- Admin no es necesario
- ORM menos flexible que SQLAlchemy
- Más overhead innecesario

#### Flask
❌ **Descartado**:
- Requiere más configuración manual
- No tiene validación automática
- No genera OpenAPI automáticamente
- Menos moderno que FastAPI

#### MySQL / MariaDB
❌ **Descartado**:
- ENUM menos robusto
- UUID no nativo (requiere CHAR(36))
- Búsqueda full-text menos potente
- Collations case-insensitive más complejas

---

### 13.4 Estructura de Proyecto Propuesta

```
gx-object-registry/
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml           # Poetry o setuptools
├── requirements.txt         # Dependencias
├── .env.example
├── .gitignore
├── README.md
│
├── alembic/                 # Migraciones
│   ├── versions/
│   └── env.py
│
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point FastAPI
│   │
│   ├── shared/
│   │   ├── database/
│   │   │   ├── connection.py
│   │   │   └── base.py
│   │   ├── errors/
│   │   │   ├── error_codes.py
│   │   │   ├── exceptions.py
│   │   │   └── handlers.py
│   │   ├── config/
│   │   │   └── settings.py
│   │   └── logging/
│   │       └── logger.py
│   │
│   ├── object_types/
│   │   ├── domain/
│   │   │   ├── object_type.py
│   │   │   └── object_type_repository.py
│   │   ├── application/
│   │   │   ├── create_object_type.py
│   │   │   ├── list_object_types.py
│   │   │   ├── get_object_type_by_id.py
│   │   │   ├── update_object_type.py
│   │   │   └── delete_object_type.py
│   │   ├── infrastructure/
│   │   │   ├── models.py
│   │   │   └── sqlalchemy_object_type_repository.py
│   │   └── presentation/
│   │       ├── dtos.py
│   │       └── router.py
│   │
│   ├── genexus_objects/
│   │   ├── domain/
│   │   │   ├── genexus_object.py
│   │   │   └── genexus_object_repository.py
│   │   ├── application/
│   │   │   ├── create_genexus_object.py
│   │   │   ├── list_genexus_objects.py
│   │   │   ├── get_genexus_object_by_id.py
│   │   │   ├── update_genexus_object.py
│   │   │   ├── delete_genexus_object.py
│   │   │   └── search_genexus_objects.py
│   │   ├── infrastructure/
│   │   │   ├── models.py
│   │   │   └── sqlalchemy_genexus_object_repository.py
│   │   └── presentation/
│   │       ├── dtos.py
│   │       └── router.py
│   │
│   └── imports/
│       ├── application/
│       │   └── import_csv_use_case.py
│       ├── domain/
│       │   ├── csv_parser.py
│       │   ├── import_validator.py
│       │   └── import_result.py
│       └── presentation/
│           ├── dtos.py
│           └── router.py
│
└── tests/
    ├── unit/
    │   ├── object_types/
    │   ├── genexus_objects/
    │   └── imports/
    ├── integration/
    │   ├── test_object_types_api.py
    │   ├── test_genexus_objects_api.py
    │   └── test_import_api.py
    └── fixtures/
        ├── valid.csv
        ├── invalid_header.csv
        └── duplicate.csv
```

---

## 14. DEPENDENCIAS PRINCIPALES

```toml
# pyproject.toml (usando Poetry)

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.109.0"
uvicorn = {extras = ["standard"], version = "^0.27.0"}
sqlalchemy = {extras = ["asyncio"], version = "^2.0.25"}
asyncpg = "^0.29.0"              # Driver async PostgreSQL
alembic = "^1.13.1"
pydantic = "^2.5.3"
pydantic-settings = "^2.1.0"
python-multipart = "^0.0.6"      # Para upload de archivos
pandas = "^2.2.0"                # Parser CSV robusto
chardet = "^5.2.0"               # Detección de encoding
structlog = "^24.1.0"            # Logging estructurado
python-dotenv = "^1.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.4"
pytest-asyncio = "^0.23.3"
pytest-cov = "^4.1.0"
httpx = "^0.26.0"                # Cliente HTTP async para tests
faker = "^22.2.0"                # Datos de prueba
black = "^24.1.1"                # Formatter
ruff = "^0.1.14"                 # Linter
mypy = "^1.8.0"                  # Type checker
```

---

## 15. VARIABLES DE ENTORNO

```bash
# .env.example

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/gx_object_registry
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# Application
APP_ENV=development  # development | staging | production
DEBUG=true
LOG_LEVEL=INFO

# API
API_PREFIX=/api
API_VERSION=v1
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# Import Settings
MAX_FILE_SIZE_MB=50
MAX_ERRORS_TO_REPORT=100
CSV_BATCH_SIZE=500

# Security (futuro)
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## 16. DOCKER SETUP

```yaml
# docker-compose.yml

version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: gx_object_registry
      POSTGRES_USER: gxuser
      POSTGRES_PASSWORD: gxpassword
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U gxuser"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build: .
    command: uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://gxuser:gxpassword@postgres:5432/gx_object_registry
      APP_ENV: development
      DEBUG: "true"
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  postgres_data:
```

```dockerfile
# Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando por defecto
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 17. PLAN DE IMPLEMENTACIÓN POR ETAPAS

### **Etapa 1: Setup Inicial** (Día 1)
- [ ] Inicializar proyecto Python con Poetry/pip
- [ ] Configurar estructura de carpetas
- [ ] Configurar FastAPI básico
- [ ] Configurar SQLAlchemy + PostgreSQL
- [ ] Configurar Alembic para migraciones
- [ ] Configurar Docker Compose
- [ ] Configurar variables de entorno
- [ ] Configurar logging con structlog
- [ ] Configurar pytest

**Entregable**: Proyecto base ejecutable con `/health` endpoint

---

### **Etapa 2: Migraciones de Base de Datos** (Día 2)
- [ ] Crear migración para tabla `object_types`
  - Campos: id, name, created_at, updated_at
  - Restricciones: PK, UNIQUE(name), índice case-insensitive
  - Trigger para updated_at
- [ ] Crear migración para tabla `genexus_objects`
  - Campos: id, name, description, object_type_id, source_type, created_at, updated_at
  - Restricciones: FK, UNIQUE(name, object_type_id)
  - Índices para búsqueda y performance
- [ ] Seed inicial (opcional) con tipos básicos

**Entregable**: Base de datos completamente estructurada

---

### **Etapa 3: Módulo ObjectTypes - Backend** (Día 3-4)
- [ ] Implementar entidad de dominio `ObjectType`
- [ ] Implementar repositorio SQLAlchemy
- [ ] Implementar casos de uso:
  - CreateObjectType
  - ListObjectTypes
  - GetObjectTypeById
  - UpdateObjectType
  - DeleteObjectType
- [ ] Implementar DTOs con Pydantic
- [ ] Implementar router FastAPI
- [ ] Escribir pruebas unitarias
- [ ] Escribir pruebas de integración

**Entregable**: CRUD completo de object_types funcionando

---

### **Etapa 4: Módulo GeneXusObjects - Backend** (Día 5-6)
- [ ] Implementar entidad de dominio `GeneXusObject`
- [ ] Implementar repositorio SQLAlchemy con búsquedas
- [ ] Implementar casos de uso:
  - CreateGeneXusObject
  - ListGeneXusObjects
  - GetGeneXusObjectById
  - UpdateGeneXusObject
  - DeleteGeneXusObject
  - SearchGeneXusObjects (con filtros avanzados)
- [ ] Implementar DTOs con Pydantic
- [ ] Implementar router FastAPI
- [ ] Escribir pruebas unitarias
- [ ] Escribir pruebas de integración

**Entregable**: CRUD completo de objetos + búsqueda funcionando

---

### **Etapa 5: Módulo Import CSV** (Día 7-9)
- [ ] Implementar parser CSV con pandas
- [ ] Implementar validador de estructura CSV
- [ ] Implementar detección de encoding
- [ ] Implementar lógica de importación:
  - Validación de filas
  - Detección de duplicados
  - Creación/actualización de objetos
  - Procesamiento por lotes
  - Manejo de errores por fila
- [ ] Implementar ImportCSVResponse
- [ ] Implementar router con upload de archivo
- [ ] Escribir pruebas con CSVs de prueba:
  - CSV válido
  - CSV con errores
  - CSV con duplicados
  - CSV con encoding no-UTF8
  - CSV con caracteres especiales

**Entregable**: Importación CSV funcionando completamente

---

### **Etapa 6: Refinamiento y Optimización** (Día 10)
- [ ] Optimizar queries de búsqueda
- [ ] Implementar índices adicionales si es necesario
- [ ] Configurar CORS
- [ ] Configurar límites de request size
- [ ] Implementar rate limiting (opcional)
- [ ] Revisar manejo de errores global
- [ ] Completar documentación OpenAPI

**Entregable**: Sistema optimizado y robusto

---

### **Etapa 7: Testing Completo** (Día 11)
- [ ] Ejecutar suite completa de tests
- [ ] Alcanzar > 80% code coverage
- [ ] Pruebas de carga con CSV grande (10k+ filas)
- [ ] Pruebas de concurrencia
- [ ] Pruebas de seguridad básicas

**Entregable**: Sistema testeado exhaustivamente

---

### **Etapa 8: Documentación y Deploy** (Día 12)
- [ ] Documentar README completo
- [ ] Documentar endpoints en Swagger
- [ ] Crear guía de instalación
- [ ] Crear guía de uso
- [ ] Preparar scripts de deployment
- [ ] Configurar health checks
- [ ] Deploy en ambiente de staging

**Entregable**: Sistema documentado y deployable

---

## 18. DECISIONES PENDIENTES CRÍTICAS

Antes de comenzar la implementación, necesito tu confirmación sobre:

### ❓ **Decisión 1: Unicidad de `name` en `genexus_objects`**

¿Debe ser case-insensitive?

**Opción A**: Case-insensitive (recomendado)
- `AhrPr001`, `ahrpr001`, `AHRPR001` se consideran duplicados
- Requiere índice funcional en `LOWER(name)`

**Opción B**: Case-sensitive
- `AhrPr001` y `ahrpr001` pueden coexistir
- Implementación más simple

**Tu decisión**: _____

---

### ❓ **Decisión 2: Búsqueda insensible a acentos**

¿La búsqueda debe ignorar acentos?

**Opción A**: Sí, insensible a acentos
- Buscar "tasa" encuentra "Tasa" y "Tása"
- Requiere extensión `unaccent` + índices GIN

**Opción B**: No, sensible a acentos
- Búsqueda más simple y rápida
- Implementación más directa

**Tu decisión**: _____

---

### ❓ **Decisión 3: Datos iniciales en `object_types`**

¿Quieres que el sistema inserte automáticamente los tipos básicos (TRANSACTION, PROCEDURE, etc.) al crear la BD?

**Opción A**: Sí, seed automático
- Más conveniente para desarrollo
- Requiere migración de datos

**Opción B**: No, insertar manualmente vía API
- Más control
- Requiere paso manual inicial

**Tu decisión**: _____

---

### ❓ **Decisión 4: Procesamiento de importación**

Para CSV muy grandes (>10,000 filas):

**Opción A**: Procesamiento sincrónico con timeout largo
- Más simple para MVP
- Usuario espera durante importación
- Puede timeout en archivos muy grandes

**Opción B**: Procesamiento asíncrono con job queue
- Más complejo (requiere Celery/RQ + Redis)
- Usuario recibe respuesta inmediata
- Sistema notifica cuando termina

**Tu decisión para MVP**: _____

---

## 19. PRÓXIMOS PASOS

Una vez que confirmes:

1. ✅ El stack tecnológico propuesto (FastAPI + PostgreSQL + SQLAlchemy)
2. ✅ Las decisiones pendientes arriba
3. ✅ Cualquier ajuste al diseño

Procederé con la **implementación por etapas**, comenzando por:

```
Etapa 1: Setup Inicial
- Crear estructura de proyecto
- Configurar dependencias
- Configurar Docker
- Configurar FastAPI básico
```

**Estaré guiándote paso a paso** en cada etapa, revisando código juntos y asegurándome de que entiendas cada decisión arquitectónica.

---

## 20. RESUMEN EJECUTIVO FINAL

### ✅ Arquitectura Definida
- Monolito modular en capas (Presentation → Application → Domain → Infrastructure)
- 3 módulos funcionales: ObjectTypes, GeneXusObjects, Imports
- Sin sobredimensionamiento arquitectónico

### ✅ Base de Datos Diseñada
- 2 tablas: `object_types`, `genexus_objects`
- Relación 1:N con `ON DELETE RESTRICT`
- Índices para performance de búsqueda
- Restricciones de integridad robustas

### ✅ API REST Completa
- 13 endpoints bien definidos
- Búsqueda avanzada con filtros
- Importación CSV con validación exhaustiva
- Manejo de errores profesional

### ✅ Flujos de Negocio Claros
- Registro manual de tipos y objetos
- Importación CSV con detección de duplicados
- Estrategia de actualización idempotente

### ✅ Validaciones Exhaustivas
- Validación de archivo CSV
- Validación por fila
- Detección de duplicados internos y en BD
- Reportes de error detallados

### ✅ Plan de Implementación
- 8 etapas claramente definidas
- Estimación: 12 días desarrollo
- Enfoque incremental y testeable

### ✅ Stack Tecnológico Profesional
- FastAPI + SQLAlchemy + PostgreSQL
- Testing con pytest
- Docker para deployment
- Documentación automática OpenAPI
