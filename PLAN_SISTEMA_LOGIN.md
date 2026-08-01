# 📋 PLAN DE IMPLEMENTACIÓN: SISTEMA DE LOGIN

## 🎯 OBJETIVOS
1. Agregar login/autenticación de usuarios
2. Rastrear quién creó cada objeto (created_by)
3. Sesión persistente (sin expiración, login permanente)
4. Proteger todas las rutas excepto el login

---

## 🏗️ ARQUITECTURA PROPUESTA

### **Opción Elegida: JWT + Cookies**
- **Pros**: Estándar de la industria, escalable, sin estado en servidor
- **Contras**: Requiere manejo de tokens
- **Decisión**: ✅ USAR ESTA

---

## 🛠️ TECNOLOGÍAS A USAR

### **Dependencias Nuevas a Instalar**
```txt
# Autenticación y Seguridad
python-jose[cryptography]>=3.3.0  # Para generar JWT tokens
passlib[bcrypt]>=1.7.4            # Para hashear contraseñas
python-multipart                  # Ya instalado (para forms)
```

**Costo**: 2 dependencias nuevas (~5MB adicional)

---

## 📁 ESTRUCTURA DE ARCHIVOS

### ARCHIVOS NUEVOS A CREAR

```
src/
└── auth/
    ├── __init__.py
    ├── domain/
    │   ├── __init__.py
    │   ├── user.py                      # Entidad User
    │   └── user_repository.py           # Interface del repositorio
    ├── application/
    │   ├── __init__.py
    │   ├── register_user.py             # Caso de uso: Registrar usuario
    │   ├── authenticate_user.py         # Caso de uso: Login
    │   └── get_current_user.py          # Caso de uso: Obtener usuario actual
    ├── infrastructure/
    │   ├── __init__.py
    │   ├── models.py                    # Modelo SQLAlchemy User
    │   ├── sqlalchemy_user_repository.py
    │   ├── password_hasher.py           # Utils para hashear passwords
    │   └── jwt_handler.py               # Utils para crear/validar JWT
    └── presentation/
        ├── __init__.py
        ├── dtos.py                      # DTOs: LoginRequest, TokenResponse, etc.
        ├── router.py                    # Endpoints: /login, /register, /logout
        └── dependencies.py              # Dependency: get_current_user
```

**Total: 13 archivos nuevos**

### ARCHIVOS EXISTENTES A MODIFICAR

#### Base de Datos
- [ ] `src/genexus_objects/infrastructure/models.py` → Agregar campo `created_by`
- [ ] `src/object_types/infrastructure/models.py` → Agregar campo `created_by`

#### Domain Layer
- [ ] `src/genexus_objects/domain/genexus_object.py` → Agregar campo `created_by`
- [ ] `src/object_types/domain/object_type.py` → Agregar campo `created_by`

#### Application Layer
- [ ] `src/genexus_objects/application/create_genexus_object.py` → Recibir `user_id`
- [ ] `src/object_types/application/create_object_type.py` → Recibir `user_id`

#### Presentation Layer (Routers)
- [ ] `src/main.py` → Registrar router de auth, agregar middleware
- [ ] `src/genexus_objects/presentation/router.py` → Agregar dependency `current_user`
- [ ] `src/object_types/presentation/router.py` → Agregar dependency `current_user`
- [ ] `src/imports/presentation/router.py` → Agregar dependency `current_user`
- [ ] `src/web/router.py` → Proteger rutas, agregar ruta `/login`

#### Frontend (Templates)
- [ ] `src/web/templates/base.html` → Agregar botón "Logout" en navbar
- [ ] `src/web/templates/index.html` → Mostrar nombre de usuario logueado
- [ ] `src/web/templates/objects.html` → Mostrar columna "Creado por"
- [ ] `src/web/templates/object_types.html` → Mostrar columna "Creado por"
- [ ] `src/web/templates/login.html` → **CREAR NUEVO**

#### Configuración
- [ ] `.env` → Agregar `SECRET_KEY` para JWT
- [ ] `requirements.txt` → Agregar dependencias

**Total: 13 archivos modificados + 1 nuevo template**

---

## 🗄️ ESQUEMA DE BASE DE DATOS

### Tabla Nueva: `users`

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Modificaciones a Tablas Existentes

```sql
-- Agregar a genexus_objects
ALTER TABLE genexus_objects
ADD COLUMN created_by INTEGER REFERENCES users(id) ON DELETE SET NULL;

-- Agregar a object_types
ALTER TABLE object_types
ADD COLUMN created_by INTEGER REFERENCES users(id) ON DELETE SET NULL;
```

**Nota**: Los registros existentes tendrán `created_by = NULL`

---

## 🔐 FLUJO DE AUTENTICACIÓN

```
1. Usuario entra a cualquier URL
   ↓
2. Middleware verifica si hay JWT en cookie
   ↓
   NO → Redirige a /login
   SÍ → Valida JWT
   ↓
3. Si válido → Permite acceso + inyecta user_id
   Si inválido → Redirige a /login
   ↓
4. Usuario crea objeto
   ↓
5. Backend guarda con created_by = user_id
```

---

## 📝 IMPLEMENTACIÓN PASO A PASO

### FASE 1: Preparación y Dependencias ✅
- [x] **Paso 1.1**: Instalar dependencias nuevas
- [x] **Paso 1.2**: Agregar SECRET_KEY al .env
- [x] **Paso 1.3**: Crear estructura de carpetas `src/auth/`

**Testeo**: ✅ Dependencias instaladas correctamente (python-jose, passlib)

---

### FASE 2: Modelo de Datos (Database) ✅
- [x] **Paso 2.1**: Crear `src/auth/infrastructure/models.py` (UserModel)
- [x] **Paso 2.2**: Modificar `src/genexus_objects/infrastructure/models.py` (agregar created_by)
- [x] **Paso 2.3**: Modificar `src/object_types/infrastructure/models.py` (agregar created_by)
- [x] **Paso 2.4**: Crear migración de Alembic
- [x] **Paso 2.5**: Ejecutar migración

**Testeo**: ✅ Tablas creadas correctamente en PostgreSQL (users, created_by en genexus_objects y object_types)

---

### FASE 3: Domain Layer (Entidades) ✅
- [x] **Paso 3.1**: Crear `src/auth/domain/user.py` (entidad User)
- [x] **Paso 3.2**: Crear `src/auth/domain/user_repository.py` (interface)
- [x] **Paso 3.3**: Modificar `src/genexus_objects/domain/genexus_object.py` (agregar created_by)
- [x] **Paso 3.4**: Modificar `src/object_types/domain/object_type.py` (agregar created_by)

**Testeo**: ✅ Entidades creadas correctamente con campo created_by

---

### FASE 4: Infrastructure Layer (Repositorios y Utils) ✅
- [x] **Paso 4.1**: Crear `src/auth/infrastructure/password_hasher.py`
- [x] **Paso 4.2**: Crear `src/auth/infrastructure/jwt_handler.py`
- [x] **Paso 4.3**: Crear `src/auth/infrastructure/sqlalchemy_user_repository.py`

**Testeo**: ✅ Utilidades de seguridad y repositorio implementados correctamente

---

### FASE 5: Application Layer (Casos de Uso) ✅
- [x] **Paso 5.1**: Crear `src/auth/application/register_user.py`
- [x] **Paso 5.2**: Crear `src/auth/application/authenticate_user.py`
- [x] **Paso 5.3**: Crear `src/auth/application/get_current_user.py`
- [x] **Paso 5.4**: Modificar `src/genexus_objects/application/create_genexus_object.py`
- [x] **Paso 5.5**: Modificar `src/object_types/application/create_object_type.py`

**Testeo**: ✅ Casos de uso implementados correctamente

---

### FASE 6: Presentation Layer (API) ✅
- [x] **Paso 6.1**: Crear `src/auth/presentation/dtos.py`
- [x] **Paso 6.2**: Crear `src/auth/presentation/dependencies.py` (get_current_user)
- [x] **Paso 6.3**: Crear `src/auth/presentation/router.py` (endpoints /login, /register, /logout, /me)
- [x] **Paso 6.4**: Modificar `src/main.py` (registrar router de auth)
- [x] **Paso 6.5**: Modificar `src/genexus_objects/presentation/router.py` (agregar current_user)
- [x] **Paso 6.6**: Modificar `src/object_types/presentation/router.py` (agregar current_user)
- [x] **Paso 6.7**: Modificar `src/imports/presentation/router.py` (agregar current_user)
- [x] **Paso 6.8**: Modificar `src/imports/application/import_csv.py` (pasar created_by)

**Testeo**: Probar endpoints con Postman/curl:
- POST /api/auth/register (crear usuario)
- POST /api/auth/login (obtener token)
- GET /api/auth/me (con token, debe retornar usuario)
- POST /api/auth/logout (eliminar cookie)
- POST /api/object-types (con token, debe guardar created_by)
- POST /api/objects (con token, debe guardar created_by)
- POST /api/imports/csv (con token, debe guardar created_by en todos los objetos)

---

### FASE 7: Frontend (Templates) ✅
- [x] **Paso 7.1**: Crear `src/web/templates/login.html`
- [x] **Paso 7.2**: Modificar `src/web/templates/base.html` (agregar logout y perfil de usuario)
- [x] **Paso 7.3**: Modificar `src/web/templates/index.html` (mostrar usuario en bienvenida)
- [x] **Paso 7.4**: Modificar `src/web/templates/objects.html` (columna "Creado por")
- [x] **Paso 7.5**: Modificar `src/web/templates/object_types.html` (columna "Creado por")
- [x] **Paso 7.6**: Modificar `src/web/router.py` (proteger rutas con autenticación)
- [x] **Paso 7.7**: Agregar `created_by` a DTOs (GeneXusObjectResponse y ObjectTypeResponse)

**Testeo**:
- Entrar a /web sin login → debe mostrar error 401
- Ir a /web/login → debe mostrar formulario de login
- Hacer login → debe mostrar nombre de usuario en sidebar
- Crear objeto → debe guardar created_by
- Hacer logout → debe eliminar cookie y poder hacer login nuevamente
- Ver lista de objetos → debe mostrar columna "Creado por"

---

### FASE 8: Script de Inicialización ✅
- [x] **Paso 8.1**: Crear script `scripts/create_admin.py` para crear usuarios
- [x] **Paso 8.2**: Crear `scripts/README.md` con documentación completa

**Testeo**:
```bash
python scripts/create_admin.py
```
- Ejecutar script → debe solicitar credenciales y crear usuario
- Verificar que el usuario puede hacer login en `/web/login`
- Verificar que aparece en la base de datos con contraseña hasheada

---

### FASE 9: Testing Final ✅
- [x] Crear objeto tipo → verificar que guarda created_by
- [x] Crear objeto genexus → verificar que guarda created_by
- [x] Ver lista de objetos → verificar que muestra nombre de usuario
- [x] Logout y login de nuevo → verificar que mantiene sesión

**Testeo**: ✅ Todos los tests pasaron exitosamente:

- Usuario admin creado (ID: 1)
- Objeto tipo "API_OBJECT" creado con created_by: 1
- Objeto GeneXus "TestAuthObject" creado con created_by: 1
- Listas muestran correctamente el campo created_by
- Logout y login funcionan correctamente
- bcrypt actualizado a versión 4.x (compatible)

---

## 📊 RESUMEN DE COSTOS

| Categoría | Cantidad | Complejidad |
|-----------|----------|-------------|
| **Archivos nuevos** | 13 archivos | Media |
| **Archivos modificados** | 13 archivos | Baja-Media |
| **Migraciones DB** | 1 migración | Baja |
| **Dependencias** | 2 nuevas libs | Baja |
| **Templates HTML** | 1 nuevo + 4 modificados | Baja |
| **Scripts** | 1 nuevo | Baja |

**Tiempo estimado**: 3-4 horas de trabajo
**Complejidad general**: Media

---

## ⚠️ DECISIONES IMPORTANTES

### 1. Primer Usuario Admin
**Decisión**: Crear script inicial que genera usuario admin por defecto

```bash
python scripts/create_admin.py
```

**Credenciales por defecto**:
- Username: `admin`
- Password: `admin123` (cambiar después del primer login)

### 2. Datos Existentes
Los objetos creados antes del sistema de login tendrán `created_by = NULL`

### 3. Sesión Permanente
JWT con expiración de 365 días (1 año)

### 4. Seguridad
- Passwords hasheados con bcrypt (costo: 12 rounds)
- JWT firmado con clave secreta (almacenada en .env)
- HttpOnly cookies (protección contra XSS)
- SameSite=Lax (protección contra CSRF)

---

## 🎯 ENTREGABLES FINALES

Al terminar la implementación tendrás:

✅ Pantalla de login
✅ Sistema de registro de usuarios
✅ Protección de todas las rutas
✅ Columna "Creado por" en todas las tablas
✅ Sesión persistente (sin expiración frecuente)
✅ Botón de logout en navbar
✅ Nombre de usuario visible en interfaz
✅ Script para crear usuarios admin

---

## 📌 NOTAS DE IMPLEMENTACIÓN

### Variables de Entorno (.env)
Agregar:
```env
# JWT Configuration
SECRET_KEY=tu-clave-secreta-super-segura-cambiala
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=365
```

### Generar SECRET_KEY
```python
import secrets
print(secrets.token_urlsafe(32))
```

---

## 🔍 COMANDOS ÚTILES

### Crear migración
```bash
alembic revision --autogenerate -m "Add auth system and created_by fields"
```

### Aplicar migración
```bash
alembic upgrade head
```

### Crear usuario admin
```bash
python scripts/create_admin.py
```

### Testear JWT
```python
from src.auth.infrastructure.jwt_handler import create_access_token, verify_token

token = create_access_token({"sub": "1"})
print(token)
decoded = verify_token(token)
print(decoded)
```

---

## ✅ CHECKLIST DE PROGRESO

### Fase 1: Preparación ✅
- [x] Dependencias instaladas
- [x] .env configurado
- [x] Estructura de carpetas creada

### Fase 2: Base de Datos ✅
- [x] UserModel creado
- [x] Campos created_by agregados
- [x] Migración creada y ejecutada

### Fase 3: Domain ✅
- [x] User entity creada
- [x] Repositorio interface creado
- [x] Entidades modificadas

### Fase 4: Infrastructure ✅
- [x] password_hasher.py
- [x] jwt_handler.py
- [x] user_repository.py

### Fase 5: Application ✅
- [x] register_user.py
- [x] authenticate_user.py
- [x] get_current_user.py
- [x] Casos de uso modificados

### Fase 6: Presentation (API) ✅
- [x] DTOs creados
- [x] Dependencies creados
- [x] Router de auth
- [x] Routers modificados

### Fase 7: Frontend ✅
- [x] login.html
- [x] base.html modificado
- [x] Templates modificados

### Fase 8: Inicialización ✅
- [x] Script create_admin.py

### Fase 9: Testing ✅
- [x] Tests pasando
- [x] Integración completa

---

## 🎉 ESTADO ACTUAL

**Fecha de inicio**: 2026-07-31
**Fecha de finalización**: 2026-08-01
**Fase actual**: ✅ TODAS LAS FASES COMPLETADAS
**Progreso**: 100% (9/9 fases completadas)

### Completado:
- ✅ FASE 1: Preparación y Dependencias
  - python-jose y passlib instalados
  - SECRET_KEY generada y agregada a .env
  - Estructura de carpetas src/auth/ creada

- ✅ FASE 2: Modelo de Datos (Database)
  - Tabla users creada con 8 columnas (id, username, email, hashed_password, full_name, is_active, created_at, updated_at)
  - Campo created_by agregado a genexus_objects
  - Campo created_by agregado a object_types
  - Migración 55adc69b9133 ejecutada exitosamente
  - Relaciones FK configuradas con ON DELETE SET NULL

- ✅ FASE 3: Domain Layer (Entidades)
  - Entidad User creada con validaciones de negocio
  - Interface UserRepository creada con todos los métodos necesarios
  - Campo created_by agregado a GeneXusObject (factory methods actualizados)
  - Campo created_by agregado a ObjectType (factory method actualizado)

- ✅ FASE 4: Infrastructure Layer
  - password_hasher.py con bcrypt (hash_password, verify_password)
  - jwt_handler.py con python-jose (create_access_token, verify_token, get_user_id_from_token)
  - sqlalchemy_user_repository.py implementado completamente
  - Excepciones personalizadas agregadas (UserNotFoundError, UserAlreadyExistsError, etc.)
  - Códigos de error agregados al sistema

- ✅ FASE 5: Application Layer (Casos de Uso)
  - register_user.py - Registrar nuevos usuarios con validaciones
  - authenticate_user.py - Login con verificación de password y generación de JWT
  - get_current_user.py - Obtener usuario desde token JWT
  - create_genexus_object.py modificado para aceptar created_by
  - create_object_type.py modificado para aceptar created_by

- ✅ FASE 6: Presentation Layer (API)
  - DTOs creados (RegisterRequest, LoginRequest, TokenResponse, UserResponse)
  - Dependencies creados (get_current_user con soporte para cookies y headers)
  - Router de auth con endpoints /register, /login, /logout, /me
  - Routers modificados (object_types, genexus_objects, imports) para requerir autenticación
  - Cookies HttpOnly configuradas para almacenar tokens JWT
  - Todos los endpoints protegidos correctamente

- ✅ FASE 7: Frontend (Templates)
  - login.html creado con diseño gradient y validación de formularios
  - base.html modificado con sección de perfil de usuario y botón logout
  - index.html modificado para mostrar saludo personalizado al usuario
  - objects.html modificado con columna "Creado por"
  - object_types.html modificado con columna "Creado por"
  - web/router.py modificado para proteger todas las rutas excepto /login
  - DTOs actualizados con campo created_by en respuestas

- ✅ FASE 8: Script de Inicialización
  - scripts/create_admin.py creado (script interactivo para crear usuarios)
  - scripts/README.md creado con documentación completa
  - Validación de inputs (username, email, password)
  - Verificación de usuarios existentes
  - Confirmación antes de crear usuario

- ✅ FASE 9: Testing Final
  - Usuario admin creado exitosamente (ID: 1)
  - Objeto tipo "API_OBJECT" creado con created_by: 1
  - Objeto GeneXus "TestAuthObject" creado con created_by: 1
  - Listas muestran correctamente el campo created_by
  - Logout y login funcionan correctamente
  - Sesión persistente verificada
  - bcrypt actualizado a versión 4.x para compatibilidad

---

## 📞 CONTACTO Y SOPORTE

Si encuentras algún problema durante la implementación, revisar:
1. Logs de la aplicación
2. Logs de PostgreSQL
3. Consola del navegador (para frontend)

---

**Última actualización**: 2026-07-31
