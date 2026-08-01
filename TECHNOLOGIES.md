# Tecnologías Utilizadas - GeneXus Object Registry

Este documento describe de manera técnica todas las tecnologías, frameworks, librerías y herramientas utilizadas en el proyecto GeneXus Object Registry.

---

## Resumen Tecnológico

**GeneXus Object Registry** es una aplicación web full-stack moderna construida con:

| Categoría | Tecnología Principal |
|-----------|---------------------|
| **Lenguaje** | Python 3.11+ |
| **Framework Backend** | FastAPI 0.109.0+ |
| **Servidor ASGI** | Uvicorn 0.27.0+ |
| **Base de Datos** | PostgreSQL 15+ |
| **ORM** | SQLAlchemy 2.0.25+ (async) |
| **Migraciones** | Alembic 1.13.1+ |
| **Validación** | Pydantic V2 (2.5.3+) |
| **Autenticación** | JWT (python-jose 3.3.0+) |
| **Hash de Contraseñas** | bcrypt 4.0.0+ |
| **Frontend** | HTML5 + Bootstrap 5 + Vanilla JavaScript |
| **Templates** | Jinja2 (integrado con FastAPI) |
| **Logging** | structlog 24.1.0+ |
| **Containerización** | Docker + Docker Compose |

---

## Tecnologías Principales

### 1. Python 3.11+

**Descripción**: Lenguaje de programación interpretado, de alto nivel y multiparadigma.

**Versión requerida**: 3.11 o superior

**Función en el proyecto**:
- Lenguaje principal para todo el backend
- Proporciona características modernas como:
  - Type hints mejorados
  - Mejor rendimiento (20-25% más rápido que Python 3.10)
  - Mensajes de error más claros
  - Soporte nativo para async/await

**Por qué es importante**:
- Ecosistema maduro con excelentes librerías
- Sintaxis clara y legible
- Gran comunidad y soporte
- Ideal para desarrollo rápido de aplicaciones web

---

### 2. FastAPI 0.109.0+

**Descripción**: Framework web moderno y de alto rendimiento para construir APIs REST con Python.

**Versión**: 0.109.0 o superior

**Características utilizadas**:
- Validación automática de datos con Pydantic
- Generación automática de documentación (Swagger/OpenAPI)
- Soporte nativo para async/await
- Dependency Injection
- Type hints para autocompletado en IDEs
- Serialización/deserialización automática de JSON

**Función en el proyecto**:
- Framework principal del backend
- Define todos los endpoints REST (`/api/...`)
- Maneja routing, validación, serialización
- Integra Jinja2 para servir páginas web (`/web/...`)
- Proporciona documentación interactiva en `/docs` y `/redoc`

**Por qué es importante**:
- Uno de los frameworks más rápidos de Python (comparable a Node.js)
- Reduce significativamente el código boilerplate
- Detecta errores en tiempo de desarrollo gracias a type hints
- Documentación automática siempre actualizada

**Ejemplo de uso en el proyecto**:
```python
# src/auth/presentation/router.py
@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    response: Response,
    repository: SQLAlchemyUserRepository = Depends(get_repository),
):
    """Inicia sesión y devuelve un token JWT."""
    use_case = AuthenticateUser(repository)
    user, access_token = await use_case.execute(
        username=request.username,
        password=request.password,
    )
    # ... lógica adicional
```

---

### 3. Uvicorn 0.27.0+

**Descripción**: Servidor ASGI (Asynchronous Server Gateway Interface) ligero y rápido.

**Versión**: 0.27.0 o superior

**Función en el proyecto**:
- Servidor HTTP que ejecuta la aplicación FastAPI
- Maneja conexiones asíncronas de manera eficiente
- Proporciona hot-reload en desarrollo (`--reload`)
- Soporta WebSockets (aunque no usado actualmente)

**Por qué es importante**:
- Permite a FastAPI aprovechar completamente async/await
- Alto rendimiento y baja latencia
- Fácil de configurar y ejecutar

**Comando usado**:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

---

### 4. PostgreSQL 15+

**Descripción**: Sistema de gestión de bases de datos relacional de código abierto.

**Versión**: 15 o superior

**Función en el proyecto**:
- Almacena toda la información persistente:
  - Usuarios y credenciales
  - Tipos de objetos GeneXus
  - Objetos GeneXus
  - Auditoría (quién creó qué y cuándo)

**Características utilizadas**:
- Índices únicos (para validar duplicados)
- Índices case-insensitive (`LOWER(name)`)
- Foreign keys con `ON DELETE RESTRICT` y `ON DELETE SET NULL`
- Constraints únicos compuestos
- Transacciones ACID

**Por qué es importante**:
- Robustez y confiabilidad en producción
- Excelente rendimiento para consultas complejas
- Soporte completo para integridad referencial
- Ampliamente adoptado en la industria

**Conexión**:
- Driver: **asyncpg** (driver asíncrono nativo para PostgreSQL)
- Formato de URL: `postgresql+asyncpg://user:password@host:port/database`

---

### 5. SQLAlchemy 2.0.25+ (Async)

**Descripción**: ORM (Object-Relational Mapping) de Python para interactuar con bases de datos.

**Versión**: 2.0.25 o superior (versión async)

**Función en el proyecto**:
- Mapea modelos Python a tablas de PostgreSQL
- Permite escribir consultas en Python en lugar de SQL crudo
- Maneja conexiones, transacciones y pool de conexiones
- Proporciona abstracción sobre la base de datos

**Características utilizadas**:
- **Async/Await**: Todas las operaciones de BD son asíncronas
- **Declarative Base**: Define modelos como clases Python
- **Relationships**: Define relaciones entre tablas (ForeignKey)
- **Sessions**: Maneja transacciones automáticamente
- **Query API**: Consultas type-safe

**Por qué es importante**:
- Evita SQL injection mediante queries parametrizadas
- Facilita el mantenimiento del código
- Permite cambiar de motor de BD con mínimos cambios
- Rendimiento optimizado con conexiones asíncronas

**Ejemplo de modelo**:
```python
# src/auth/infrastructure/models.py
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    # ...
```

---

### 6. asyncpg 0.29.0+

**Descripción**: Driver PostgreSQL asíncrono de alto rendimiento para Python.

**Versión**: 0.29.0 o superior

**Función en el proyecto**:
- Conexión nativa y rápida a PostgreSQL
- Permite operaciones de base de datos no bloqueantes
- Utilizado internamente por SQLAlchemy cuando se usa `postgresql+asyncpg://`

**Por qué es importante**:
- Más rápido que psycopg2 (driver síncrono tradicional)
- Permite manejar múltiples requests concurrentemente
- Optimizado para aplicaciones async/await

---

### 7. Alembic 1.13.1+

**Descripción**: Herramienta de migraciones de base de datos para SQLAlchemy.

**Versión**: 1.13.1 o superior

**Función en el proyecto**:
- Versionado del esquema de base de datos
- Permite aplicar cambios de esquema de forma ordenada
- Mantiene historial de cambios en `/alembic/versions/`
- Soporta rollback de migraciones

**Migraciones aplicadas**:
1. `001_create_object_types_and_genexus_objects.py` - Tablas iniciales
2. `20260731_1438_add_auth_system_and_created_by_fields.py` - Sistema de autenticación
3. `20260801_1120_add_last_login_to_users.py` - Tracking de login
4. `20260801_1200_add_must_change_password.py` - Contraseñas temporales

**Por qué es importante**:
- Cambios de esquema rastreables y reversibles
- Colaboración en equipo sin conflictos de BD
- Despliegues seguros en producción

**Comandos principales**:
```bash
alembic upgrade head      # Aplicar migraciones
alembic downgrade -1      # Revertir última migración
alembic revision --autogenerate -m "Mensaje"  # Crear migración
```

---

### 8. Pydantic V2 (2.5.3+)

**Descripción**: Librería de validación de datos y gestión de configuración usando type hints.

**Versión**: 2.5.3 o superior (versión 2.x)

**Función en el proyecto**:
- **Validación de requests**: Valida automáticamente datos de entrada en endpoints
- **Serialización de responses**: Convierte objetos Python a JSON
- **Configuración**: Lee y valida variables de entorno (con pydantic-settings)
- **DTOs**: Define Request y Response models

**Características utilizadas**:
- Type hints para validación
- Validadores personalizados (`@field_validator`)
- Conversión automática de tipos
- Mensajes de error descriptivos
- Generación de JSON Schema

**Por qué es importante**:
- Previene errores al validar datos en tiempo de request
- Documentación automática de modelos
- Seguridad al rechazar datos inválidos
- Rendimiento optimizado en V2

**Ejemplo**:
```python
# src/auth/presentation/dtos.py
class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    must_change_password: bool
```

---

### 9. python-jose[cryptography] 3.3.0+

**Descripción**: Librería para crear y verificar tokens JWT (JSON Web Tokens).

**Versión**: 3.3.0 o superior

**Función en el proyecto**:
- Generar tokens JWT al hacer login
- Verificar tokens JWT en cada request protegido
- Firmar tokens con `SECRET_KEY` usando algoritmo HS256

**Por qué es importante**:
- Autenticación stateless (no requiere sesiones en servidor)
- Seguridad mediante firma criptográfica
- Estándar de la industria para APIs REST

**Flujo en el proyecto**:
1. Usuario hace login → Backend genera JWT
2. JWT se almacena en cookie HttpOnly
3. Cada request incluye el JWT
4. Backend verifica firma y extrae user_id
5. Se obtiene el usuario desde la BD

**Ejemplo**:
```python
# src/auth/infrastructure/jwt_handler.py
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.access_token_expire_days)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt
```

---

### 10. bcrypt 4.0.0+

**Descripción**: Librería para hashing seguro de contraseñas.

**Versión**: 4.0.0 a <5.0.0

**Función en el proyecto**:
- Hashear contraseñas antes de guardarlas en la BD
- Verificar contraseñas al hacer login
- Usa salt aleatorio para cada contraseña

**Por qué es importante**:
- Nunca almacena contraseñas en texto plano
- Resistente a ataques de fuerza bruta (lento por diseño)
- Salt aleatorio previene rainbow tables
- Estándar de seguridad recomendado

**Ejemplo**:
```python
# src/auth/infrastructure/password_hasher.py
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )
```

---

### 11. structlog 24.1.0+

**Descripción**: Librería de logging estructurado para Python.

**Versión**: 24.1.0 o superior

**Función en el proyecto**:
- Logging estructurado con contexto adicional
- Salida en formato JSON (ideal para producción)
- Salida legible en desarrollo
- Información automática (timestamp, nivel, archivo, línea)

**Por qué es importante**:
- Facilita debugging y troubleshooting
- Logs parseables por herramientas (ELK, Splunk, etc.)
- Contexto rico (user_id, object_id, etc.)
- Rendimiento optimizado

**Ejemplo**:
```python
from src.shared.logging.logger import logger

logger.info(
    "User created successfully",
    user_id=created.id,
    username=created.username,
)
```

**Salida en desarrollo**:
```
[2026-08-01 10:00:00.123 INFO] User created successfully user_id=1 username=admin
```

---

### 12. Jinja2 (integrado con FastAPI)

**Descripción**: Motor de templates para Python.

**Función en el proyecto**:
- Renderiza páginas HTML dinámicas en `/web/...`
- Herencia de templates (base.html)
- Variables, loops, condicionales en HTML

**Templates principales**:
- `base.html` - Template base con navegación
- `login.html` - Página de login
- `change_password.html` - Cambio de contraseña
- `index.html` - Dashboard
- `object_types.html` - Gestión de tipos
- `objects.html` - Gestión de objetos
- `users.html` - Gestión de usuarios
- `import.html` - Importación CSV

**Por qué es importante**:
- Permite construir UI sin framework JavaScript pesado
- Server-side rendering rápido
- Fácil integración con FastAPI

---

### 13. Bootstrap 5

**Descripción**: Framework CSS para diseño responsive.

**Versión**: 5.3.0 (CDN)

**Función en el proyecto**:
- Estilos de la interfaz web
- Componentes UI (botones, modales, formularios, tablas)
- Grid system responsive
- Iconos (Bootstrap Icons)

**Por qué es importante**:
- UI profesional sin escribir mucho CSS
- Responsive out-of-the-box
- Ampliamente conocido y documentado

---

### 14. Docker y Docker Compose

**Descripción**: Plataforma de containerización.

**Versión**:
- Docker 20.10+
- Docker Compose 3.8+

**Función en el proyecto**:
- **Dockerfile**: Define imagen de la aplicación Python
- **docker-compose.yml**: Orquesta PostgreSQL + API

**Servicios definidos**:
1. **postgres**: PostgreSQL 15-alpine
2. **api**: Aplicación FastAPI

**Por qué es importante**:
- Entorno consistente en desarrollo y producción
- Fácil setup para nuevos desarrolladores
- Aislamiento de dependencias

---

## Dependencias de Desarrollo

### Testing

**pytest 7.4.4+**
- Framework de testing para Python
- Ejecución de tests unitarios e integración

**pytest-asyncio 0.23.3+**
- Soporte para tests asíncronos

**pytest-cov 4.1.0+**
- Medición de cobertura de código

**httpx 0.26.0+**
- Cliente HTTP async para tests de endpoints

**faker 22.2.0+**
- Generación de datos fake para tests

### Code Quality

**black 24.1.1+**
- Formateador de código automático
- Estilo consistente en todo el proyecto

**ruff 0.1.14+**
- Linter rápido (reemplazo de flake8, pylint, etc.)
- Detecta errores y malas prácticas

**mypy 1.8.0+**
- Type checker estático
- Verifica type hints

---

## Otras Dependencias Importantes

### chardet 5.2.0+
**Descripción**: Detección automática de encoding de archivos.

**Función**: Detectar encoding de archivos CSV antes de parsear.

**Por qué**: Maneja CSVs con diferentes encodings (UTF-8, Latin1, etc.)

---

### python-multipart 0.0.6+
**Descripción**: Parser de formularios multipart/form-data.

**Función**: Permite subir archivos a través de formularios.

**Por qué**: Necesario para el endpoint de importación CSV (`/api/imports/csv`).

---

### python-dotenv 1.0.0+
**Descripción**: Lee variables de entorno desde archivo `.env`.

**Función**: Cargar configuración desde `.env` al iniciar la aplicación.

**Por qué**: Facilita gestión de configuración por entorno.

---

### email-validator 2.0.0+
**Descripción**: Validación de direcciones de email.

**Función**: Validar formato de emails en registro de usuarios.

**Por qué**: Asegura que los emails sean válidos antes de guardarlos.

---

## Arquitectura Tecnológica

### Flujo de Información

```
┌─────────────┐
│   Browser   │
│  (Usuario)  │
└──────┬──────┘
       │ HTTP Request
       ↓
┌─────────────────────────────────┐
│        Nginx (Opcional)         │
│     (Reverse Proxy / HTTPS)     │
└─────────────┬───────────────────┘
              │
              ↓
┌─────────────────────────────────┐
│      Uvicorn (ASGI Server)      │
│  Ejecuta FastAPI Application    │
└─────────────┬───────────────────┘
              │
              ↓
┌─────────────────────────────────┐
│          FastAPI App            │
│  - Routing                      │
│  - Validación (Pydantic)        │
│  - Dependency Injection         │
│  - Autenticación (JWT)          │
└─────────────┬───────────────────┘
              │
              ↓
┌─────────────────────────────────┐
│      Application Layer          │
│  (Use Cases / Business Logic)   │
│  - CreateUser                   │
│  - AuthenticateUser             │
│  - ImportCSV                    │
│  - etc.                         │
└─────────────┬───────────────────┘
              │
              ↓
┌─────────────────────────────────┐
│    Infrastructure Layer         │
│  - SQLAlchemy Repositories      │
│  - Password Hasher (bcrypt)     │
│  - JWT Handler                  │
│  - CSV Parser                   │
└─────────────┬───────────────────┘
              │
              ↓
┌─────────────────────────────────┐
│       PostgreSQL 15+            │
│  - Almacenamiento persistente   │
│  - Transacciones ACID           │
└─────────────────────────────────┘
```

### Stack Completo

**Frontend**:
- HTML5
- CSS3 (Bootstrap 5)
- JavaScript (Vanilla)
- Jinja2 Templates

**Backend**:
- Python 3.11+
- FastAPI 0.109.0+
- Uvicorn 0.27.0+

**Base de Datos**:
- PostgreSQL 15+
- SQLAlchemy 2.0.25+ (ORM)
- asyncpg 0.29.0+ (Driver)
- Alembic 1.13.1+ (Migraciones)

**Autenticación**:
- JWT (python-jose 3.3.0+)
- bcrypt 4.0.0+
- Cookies HttpOnly

**Validación**:
- Pydantic V2 (2.5.3+)

**Logging**:
- structlog 24.1.0+

**Containerización**:
- Docker
- Docker Compose

---

## Servicios Externos

Actualmente el proyecto **no utiliza servicios externos de terceros**. Toda la funcionalidad está contenida en el stack descrito arriba.

En el futuro podría integrarse con:
- Servicios de email (SMTP, SendGrid, Mailgun)
- Servicios de almacenamiento (AWS S3, Azure Blob)
- Servicios de monitoreo (Sentry, DataDog)

---

## Consideraciones de Seguridad

Las tecnologías fueron elegidas considerando:

1. **Validación automática**: Pydantic rechaza datos inválidos
2. **SQL Injection**: SQLAlchemy usa queries parametrizadas
3. **Password Storage**: bcrypt con salt aleatorio
4. **Authentication**: JWT con firma criptográfica
5. **Cookies seguras**: HttpOnly, SameSite=Lax
6. **Logging**: structlog no loguea información sensible
7. **Type Safety**: mypy detecta errores en desarrollo

---

## Resumen de Versiones

| Tecnología | Versión Mínima |
|------------|----------------|
| Python | 3.11+ |
| FastAPI | 0.109.0+ |
| Uvicorn | 0.27.0+ |
| PostgreSQL | 15+ |
| SQLAlchemy | 2.0.25+ |
| asyncpg | 0.29.0+ |
| Alembic | 1.13.1+ |
| Pydantic | 2.5.3+ |
| python-jose | 3.3.0+ |
| bcrypt | 4.0.0 a <5.0.0 |
| structlog | 24.1.0+ |
| pytest | 7.4.4+ |
| black | 24.1.1+ |
| ruff | 0.1.14+ |
| mypy | 1.8.0+ |

---

**El stack tecnológico de GeneXus Object Registry está diseñado para ser moderno, seguro, mantenible y escalable, utilizando las mejores prácticas de desarrollo web con Python.**
