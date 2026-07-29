# GUÍA PASO A PASO - ESTRUCTURA DEL PROYECTO

## 📁 ESTRUCTURA COMPLETA (Vista General)

```
gx-object-registry/                    ← Raíz del proyecto (ya existe)
│
├── 📄 documentation.md                 ← Ya existe (documentación del diseño)
├── 📄 guia.md                          ← Esta guía
│
├── 📄 .env.example                     ← Ejemplo de variables de entorno
├── 📄 .env                             ← Variables de entorno reales (NO subir a git)
├── 📄 .gitignore                       ← Archivos que Git debe ignorar
├── 📄 requirements.txt                 ← Dependencias de Python
├── 📄 README.md                        ← Documentación del proyecto
├── 📄 docker-compose.yml               ← Configuración de Docker
├── 📄 Dockerfile                       ← Imagen Docker de la aplicación
│
├── 📁 alembic/                         ← Migraciones de base de datos
│   ├── 📄 alembic.ini                  ← Configuración de Alembic
│   ├── 📄 env.py                       ← Script de entorno de Alembic
│   └── 📁 versions/                    ← Carpeta para las migraciones
│       └── (archivos de migración se generan automáticamente)
│
├── 📁 src/                             ← CÓDIGO FUENTE (toda la aplicación)
│   ├── 📄 __init__.py                  ← Hace que src sea un paquete Python
│   ├── 📄 main.py                      ← PUNTO DE ENTRADA de FastAPI
│   │
│   ├── 📁 shared/                      ← Componentes compartidos por todos los módulos
│   │   ├── 📄 __init__.py
│   │   │
│   │   ├── 📁 database/                ← Conexión a la base de datos
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 connection.py        ← Configuración de SQLAlchemy
│   │   │   └── 📄 base.py              ← Clase base para modelos
│   │   │
│   │   ├── 📁 config/                  ← Configuración de la aplicación
│   │   │   ├── 📄 __init__.py
│   │   │   └── 📄 settings.py          ← Variables de entorno y configuración
│   │   │
│   │   ├── 📁 errors/                  ← Manejo de errores
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 error_codes.py       ← Códigos de error estandarizados
│   │   │   ├── 📄 exceptions.py        ← Excepciones personalizadas
│   │   │   └── 📄 handlers.py          ← Manejadores de excepciones
│   │   │
│   │   └── 📁 logging/                 ← Sistema de logs
│   │       ├── 📄 __init__.py
│   │       └── 📄 logger.py            ← Configuración de logging
│   │
│   ├── 📁 object_types/                ← MÓDULO: Tipos de objetos GeneXus
│   │   ├── 📄 __init__.py
│   │   │
│   │   ├── 📁 domain/                  ← Lógica de negocio pura
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 object_type.py       ← Entidad ObjectType (clase de dominio)
│   │   │   └── 📄 object_type_repository.py ← Interfaz del repositorio (contrato)
│   │   │
│   │   ├── 📁 application/             ← Casos de uso (orquestación)
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 create_object_type.py     ← Caso de uso: Crear tipo
│   │   │   ├── 📄 list_object_types.py      ← Caso de uso: Listar tipos
│   │   │   ├── 📄 get_object_type_by_id.py  ← Caso de uso: Obtener por ID
│   │   │   ├── 📄 update_object_type.py     ← Caso de uso: Actualizar tipo
│   │   │   └── 📄 delete_object_type.py     ← Caso de uso: Eliminar tipo
│   │   │
│   │   ├── 📁 infrastructure/          ← Implementación técnica (BD, APIs externas)
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 models.py            ← Modelo SQLAlchemy (tabla en BD)
│   │   │   └── 📄 sqlalchemy_object_type_repository.py ← Implementación del repositorio
│   │   │
│   │   └── 📁 presentation/            ← Capa de presentación (API REST)
│   │       ├── 📄 __init__.py
│   │       ├── �� dtos.py              ← DTOs (Request/Response con Pydantic)
│   │       └── 📄 router.py            ← Endpoints REST (rutas FastAPI)
│   │
│   ├── 📁 genexus_objects/             ← MÓDULO: Objetos GeneXus
│   │   ├── 📄 __init__.py
│   │   │
│   │   ├── 📁 domain/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 genexus_object.py         ← Entidad GeneXusObject
│   │   │   └── 📄 genexus_object_repository.py ← Interfaz del repositorio
│   │   │
│   │   ├── 📁 application/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 create_genexus_object.py
│   │   │   ├── 📄 list_genexus_objects.py
│   │   │   ├── 📄 get_genexus_object_by_id.py
│   │   │   ├── 📄 update_genexus_object.py
│   │   │   ├── 📄 delete_genexus_object.py
│   │   │   └── 📄 search_genexus_objects.py
│   │   │
│   │   ├── 📁 infrastructure/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 models.py
│   │   │   └── 📄 sqlalchemy_genexus_object_repository.py
│   │   │
│   │   └── 📁 presentation/
│   │       ├── 📄 __init__.py
│   │       ├── 📄 dtos.py
│   │       └── 📄 router.py
│   │
│   └── 📁 imports/                     ← MÓDULO: Importación CSV
│       ├── 📄 __init__.py
│       │
│       ├── 📁 domain/
│       │   ├── 📄 __init__.py
│       │   ├── 📄 csv_parser.py        ← Parser de archivos CSV
│       │   ├── 📄 import_validator.py  ← Validaciones de importación
│       │   └── 📄 import_result.py     ← Resultado de la importación
│       │
│       ├── 📁 application/
│       │   ├── 📄 __init__.py
│       │   └── 📄 import_csv_use_case.py ← Caso de uso: Importar CSV
│       │
│       └── 📁 presentation/
│           ├── 📄 __init__.py
│           ├── 📄 dtos.py
│           └── 📄 router.py
│
└── 📁 tests/                           ← PRUEBAS
    ├── 📄 __init__.py
    │
    ├── 📁 unit/                        ← Pruebas unitarias (lógica aislada)
    │   ├── 📄 __init__.py
    │   ├── 📁 object_types/
    │   ├── 📁 genexus_objects/
    │   └── 📁 imports/
    │
    ├── 📁 integration/                 ← Pruebas de integración (con BD real)
    │   ├── 📄 __init__.py
    │   ├── 📄 test_object_types_api.py
    │   ├── 📄 test_genexus_objects_api.py
    │   └── 📄 test_import_api.py
    │
    └── 📁 fixtures/                    ← Archivos de prueba (CSVs de ejemplo)
        ├── 📄 valid.csv
        ├── 📄 invalid_header.csv
        ├── 📄 duplicate.csv
        └── 📄 large.csv
```

---

## 📚 EXPLICACIÓN POR CARPETA

### 🔵 **Nivel Raíz** (configuración del proyecto)

| Archivo/Carpeta | Para qué sirve |
|----------------|----------------|
| `documentation.md` | Toda la documentación de diseño y arquitectura (YA EXISTE) |
| `guia.md` | Esta guía paso a paso |
| `.env.example` | Plantilla de variables de entorno (para otros desarrolladores) |
| `.env` | Variables de entorno reales (contraseñas, URLs) - NO subir a Git |
| `.gitignore` | Lista de archivos que Git debe ignorar (node_modules, .env, etc.) |
| `requirements.txt` | Lista de dependencias de Python (FastAPI, SQLAlchemy, etc.) |
| `README.md` | Documentación para usar el proyecto (cómo instalarlo, ejecutarlo) |
| `docker-compose.yml` | Configuración para levantar PostgreSQL + API con Docker |
| `Dockerfile` | Instrucciones para crear la imagen Docker de la aplicación |

---

### 🔵 **`alembic/`** (migraciones de base de datos)

| Archivo/Carpeta | Para qué sirve |
|----------------|----------------|
| `alembic.ini` | Configuración de Alembic (herramienta de migraciones) |
| `env.py` | Script que Alembic usa para conectarse a la BD |
| `versions/` | Aquí se guardan los archivos de migración (crear tablas, índices, etc.) |

**¿Qué hace?** Alembic es como "Git para la base de datos". Te permite crear versiones de tu esquema de BD y aplicar cambios de forma controlada.

---

### 🔵 **`src/`** (código fuente - TODO EL CÓDIGO VIVE AQUÍ)

---

#### 🟢 **`src/main.py`** (punto de entrada)

**¿Qué es?** El archivo principal que inicia FastAPI. Aquí se configuran:
- Los routers (endpoints)
- Middleware
- CORS
- Manejo de errores global

**Ejemplo conceptual:**
```python
from fastapi import FastAPI
from src.object_types.presentation import router as object_types_router
from src.genexus_objects.presentation import router as genexus_objects_router

app = FastAPI(title="GeneXus Object Registry")

app.include_router(object_types_router)
app.include_router(genexus_objects_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

---

#### 🟢 **`src/shared/`** (componentes compartidos)

**¿Qué es?** Todo lo que usan TODOS los módulos (database, errores, configuración).

##### `shared/database/`
- **`connection.py`**: Configuración de SQLAlchemy (conexión a PostgreSQL)
- **`base.py`**: Clase base para todos los modelos de BD

##### `shared/config/`
- **`settings.py`**: Lee las variables de `.env` (DATABASE_URL, MAX_FILE_SIZE, etc.)

##### `shared/errors/`
- **`error_codes.py`**: Enum con todos los códigos de error (`OBJECT_TYPE_NOT_FOUND`, etc.)
- **`exceptions.py`**: Clases de excepciones personalizadas
- **`handlers.py`**: Convierte excepciones en respuestas HTTP

##### `shared/logging/`
- **`logger.py`**: Configuración de logs estructurados

---

#### 🟢 **`src/object_types/`** (módulo de tipos)

**¿Qué hace este módulo?** Administra el catálogo de tipos de objetos GeneXus (PROCEDURE, TRANSACTION, etc.)

**Organización por capas:**

##### `domain/` (lógica de negocio pura)
- **`object_type.py`**: Entidad de dominio (clase Python con validaciones)
  ```python
  class ObjectType:
      id: UUID
      name: str

      def validate(self):
          if len(self.name) > 100:
              raise ValueError("Nombre muy largo")
  ```
- **`object_type_repository.py`**: Interfaz (contrato) que dice qué métodos debe tener el repositorio
  ```python
  class ObjectTypeRepository(ABC):
      @abstractmethod
      async def create(self, obj: ObjectType) -> ObjectType:
          pass
  ```

##### `application/` (casos de uso)
- **`create_object_type.py`**: Orquesta la creación (valida, verifica duplicados, guarda)
- **`list_object_types.py`**: Obtiene lista paginada
- **`get_object_type_by_id.py`**: Busca uno por ID
- **`update_object_type.py`**: Actualiza un tipo
- **`delete_object_type.py`**: Elimina un tipo (verifica que no tenga objetos relacionados)

##### `infrastructure/` (implementación técnica)
- **`models.py`**: Modelo SQLAlchemy (mapea la tabla `object_types` en PostgreSQL)
  ```python
  class ObjectTypeModel(Base):
      __tablename__ = "object_types"
      id = Column(UUID, primary_key=True)
      name = Column(String(100), unique=True)
  ```
- **`sqlalchemy_object_type_repository.py`**: Implementación real del repositorio usando SQLAlchemy

##### `presentation/` (API REST)
- **`dtos.py`**: Request/Response models con Pydantic
  ```python
  class CreateObjectTypeRequest(BaseModel):
      name: str = Field(max_length=100)
  ```
- **`router.py`**: Endpoints de FastAPI
  ```python
  @router.post("/api/object-types")
  async def create_object_type(request: CreateObjectTypeRequest):
      ...
  ```

---

#### 🟢 **`src/genexus_objects/`** (módulo de objetos)

**¿Qué hace?** Administra los objetos GeneXus (AhrPr001, AhrTn001, etc.)

**Estructura igual que `object_types/`:**
- `domain/`: Entidad `GeneXusObject` + interfaz del repositorio
- `application/`: Casos de uso (crear, listar, buscar, actualizar, eliminar)
- `infrastructure/`: Modelo SQLAlchemy + repositorio real
- `presentation/`: DTOs + router con endpoints

---

#### 🟢 **`src/imports/`** (módulo de importación)

**¿Qué hace?** Importa objetos desde archivos CSV

**Estructura:**
- `domain/`:
  - `csv_parser.py`: Lee y parsea archivos CSV
  - `import_validator.py`: Valida estructura del CSV y filas
  - `import_result.py`: Modela el resultado (created, updated, errors)
- `application/`:
  - `import_csv_use_case.py`: Orquesta TODO el proceso de importación
- `presentation/`:
  - `dtos.py`: DTOs para request/response
  - `router.py`: Endpoint `POST /api/objects/import/csv`

---

### 🔵 **`tests/`** (pruebas automatizadas)

| Carpeta | Para qué sirve |
|---------|----------------|
| `unit/` | Pruebas de lógica aislada (sin BD, sin red) |
| `integration/` | Pruebas con BD real (PostgreSQL en Docker) |
| `fixtures/` | Archivos de ejemplo para probar (CSVs válidos/inválidos) |

---

## 🎯 ORDEN DE CREACIÓN RECOMENDADO

### **FASE 1: Configuración base** (archivos raíz)
1. `.gitignore`
2. `requirements.txt`
3. `.env.example`
4. `.env`
5. `README.md`

### **FASE 2: Estructura de carpetas**
6. Crear toda la estructura de carpetas vacías (con `__init__.py`)

### **FASE 3: Shared (componentes compartidos)**
7. `shared/config/settings.py`
8. `shared/database/connection.py`
9. `shared/errors/` (todo)

### **FASE 4: Main**
10. `main.py` (básico con `/health`)

### **FASE 5: Primer módulo (ObjectTypes)**
11. `object_types/domain/`
12. `object_types/infrastructure/`
13. `object_types/application/`
14. `object_types/presentation/`

### **FASE 6: Docker y BD**
15. `docker-compose.yml`
16. `Dockerfile`
17. `alembic/` (configuración + primera migración)

### **FASE 7: Segundo módulo (GeneXusObjects)**
18. Igual que ObjectTypes

### **FASE 8: Tercer módulo (Imports)**
19. Igual que anteriores

### **FASE 9: Tests**
20. `tests/` (todos)

---

## 🚀 ARQUITECTURA EN CAPAS - EXPLICACIÓN

### ¿Por qué 4 capas?

```
PRESENTATION (API)
    ↓
APPLICATION (Casos de Uso)
    ↓
DOMAIN (Lógica de Negocio)
    ↓
INFRASTRUCTURE (Base de Datos)
```

#### **1. PRESENTATION** (Capa de Presentación)
- **Responsabilidad**: Comunicación con el mundo exterior (HTTP, APIs)
- **Contiene**: Routers de FastAPI, DTOs con Pydantic
- **Ejemplo**: Recibe `POST /api/object-types` con JSON, valida formato

#### **2. APPLICATION** (Capa de Aplicación)
- **Responsabilidad**: Orquestar casos de uso (coordinar)
- **Contiene**: Clases de casos de uso
- **Ejemplo**: "Para crear un tipo, primero valido, luego verifico duplicados, luego guardo"

#### **3. DOMAIN** (Capa de Dominio)
- **Responsabilidad**: Lógica de negocio pura (reglas del negocio)
- **Contiene**: Entidades (ObjectType, GeneXusObject), interfaces de repositorios
- **Ejemplo**: "El nombre no puede superar 100 caracteres"

#### **4. INFRASTRUCTURE** (Capa de Infraestructura)
- **Responsabilidad**: Detalles técnicos (BD, APIs externas)
- **Contiene**: Modelos SQLAlchemy, implementación de repositorios
- **Ejemplo**: "Ejecuto INSERT INTO object_types..."

---

## 📌 CONCEPTOS CLAVE

### ¿Qué es un DTO (Data Transfer Object)?
- Objeto que se usa para transferir datos entre capas
- En nuestro caso: Request/Response de la API
- Usa Pydantic para validación automática

### ¿Qué es una Entidad de Dominio?
- Representa un concepto del negocio
- Contiene lógica y validaciones del negocio
- NO depende de la base de datos

### ¿Qué es un Repositorio?
- Patrón que abstrae el acceso a datos
- Interfaz: define QUÉ operaciones hay (create, find, delete)
- Implementación: define CÓMO se hacen (con SQLAlchemy)

### ¿Qué es un Caso de Uso?
- Representa una acción que puede hacer el usuario
- Orquesta múltiples operaciones
- Ejemplo: "Crear un tipo de objeto" implica validar, verificar duplicados y guardar

---

## 🎨 VENTAJAS DE ESTA ARQUITECTURA

✅ **Separación de responsabilidades**: Cada capa tiene un propósito claro
✅ **Testeable**: Puedes probar lógica sin BD, sin API
✅ **Mantenible**: Cambios en BD no afectan lógica de negocio
✅ **Escalable**: Fácil agregar nuevos módulos
✅ **Profesional**: Estructura usada en empresas reales

---

## 💡 PRÓXIMOS PASOS

Cuando estés listo, empezamos paso a paso creando:
1. Archivos de configuración
2. Estructura de carpetas
3. Código básico
4. Docker
5. Base de datos
6. Primer módulo funcional

**Avísame cuando quieras empezar y vamos paso a paso** 🚀
