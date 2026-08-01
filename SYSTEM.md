# Sistema - GeneXus Object Registry

Este documento explica qué es el sistema GeneXus Object Registry, su propósito y cómo funciona desde un punto de vista funcional.

---

## Descripción General

### ¿Qué es GeneXus Object Registry?

**GeneXus Object Registry** es un sistema de gestión y registro de objetos GeneXus que permite catalogar, organizar y administrar la información sobre objetos técnicos utilizados en proyectos de desarrollo con la plataforma GeneXus.

### ¿Para qué fue desarrollado?

El sistema fue diseñado para resolver la necesidad de:

1. **Centralizar** la información de objetos GeneXus en un único repositorio
2. **Categorizar** objetos según su tipo (Procedures, Transactions, Work Panels, etc.)
3. **Importar** masivamente objetos desde archivos CSV
4. **Consultar** y buscar objetos de manera eficiente
5. **Auditar** quién creó cada objeto y cuándo
6. **Gestionar** usuarios con diferentes niveles de acceso

### ¿Qué problema busca resolver?

En proyectos grandes de GeneXus, puede haber cientos o miles de objetos técnicos dispersos. Este sistema permite:

- **Visibilidad**: Tener un catálogo completo de todos los objetos
- **Organización**: Clasificar objetos por tipo
- **Trazabilidad**: Saber quién creó cada objeto
- **Automatización**: Importar objetos masivamente desde CSVs
- **Control de acceso**: Restringir quién puede modificar información

### ¿Quiénes son sus usuarios?

El sistema está dirigido a:

1. **Desarrolladores GeneXus**: Consultan y registran objetos
2. **Líderes técnicos**: Gestionan catálogos de objetos
3. **Administradores de sistema**: Gestionan usuarios y permisos
4. **Analistas**: Consultan estadísticas y reportes

### Objetivo Principal

Proveer una **plataforma centralizada** para la gestión completa del ciclo de vida de objetos GeneXus, desde su registro hasta su consulta, con trazabilidad completa y control de acceso.

---

## Funcionalidades Principales

### 1. Gestión de Usuarios

**Descripción**: Administración completa de usuarios del sistema.

**Capacidades**:
- Crear nuevos usuarios
- Listar usuarios existentes
- Actualizar información de usuarios (email, nombre completo)
- Activar/desactivar usuarios
- Resetear contraseñas
- Ver estadísticas por usuario

**Acceso**: Solo usuarios autenticados (administradores)

---

### 2. Autenticación y Seguridad

**Descripción**: Sistema de login seguro con JWT.

**Capacidades**:
- Inicio de sesión con usuario y contraseña
- Cambio de contraseña obligatorio cuando se resetea
- Cambio de contraseña voluntario
- Cierre de sesión
- Tracking de último login
- Cookies HttpOnly para seguridad

**Acceso**: Todos los usuarios

---

### 3. Gestión de Tipos de Objetos

**Descripción**: Administración de categorías de objetos GeneXus.

**Capacidades**:
- Crear nuevos tipos de objetos (ej: PROCEDURE, TRANSACTION, WORK_PANEL)
- Listar todos los tipos de objetos
- Actualizar nombres de tipos
- Eliminar tipos (solo si no tienen objetos asociados)
- Búsqueda case-insensitive

**Ejemplos de tipos**:
- `PROCEDURE` - Procedimientos
- `TRANSACTION` - Transacciones
- `WORK_PANEL` - Paneles de trabajo
- `WEB_PANEL` - Paneles web
- `DATA_PROVIDER` - Proveedores de datos
- Y más...

**Acceso**: Usuarios autenticados

---

### 4. Gestión de Objetos GeneXus

**Descripción**: Administración completa de objetos GeneXus registrados.

**Capacidades**:
- Crear nuevos objetos
  - Nombre técnico (ej: `AhrPr001`)
  - Descripción (ej: "Recupera Tasa de Interés")
  - Tipo de objeto (debe existir previamente)
- Listar objetos con paginación
- Buscar objetos por nombre
- Filtrar por tipo de objeto
- Filtrar por origen (MANUAL o CSV)
- Actualizar información de objetos
- Eliminar objetos
- Ver auditoría (quién creó, cuándo)

**Restricciones**:
- No se pueden crear objetos duplicados (mismo nombre y tipo)
- El tipo de objeto debe existir previamente

**Acceso**: Usuarios autenticados

---

### 5. Importación Masiva desde CSV

**Descripción**: Importar cientos o miles de objetos desde archivos CSV.

**Capacidades**:
- Subir archivo CSV con formato específico
- Validar formato y contenido
- Procesar importación en lotes
- Eliminar objetos existentes antes de importar (opcional)
- Reportar errores detallados por fila
- Mapping automático de códigos a tipos

**Formato CSV esperado**:
```csv
name;description;objectType
AhrPr001;Recupera Tasa Interés;PROCEDURE
AhrTn001;Tipos de Cuentas;TRANSACTION
AhrTr001;Apertura de Cuenta;WORK_PANEL
```

**Delimitador**: Punto y coma (`;`)

**Headers obligatorios**:
- `name`: Nombre técnico del objeto
- `description`: Descripción (puede estar vacía)
- `objectType`: Código del tipo de objeto

**Validaciones**:
- Archivo no mayor a 50 MB (configurable)
- Headers correctos
- Formato CSV válido
- Tipos de objetos deben existir
- Nombres no duplicados

**Acceso**: Usuarios autenticados

---

### 6. Dashboard y Panel de Control

**Descripción**: Vista principal del sistema.

**Capacidades**:
- Vista general del sistema
- Acceso rápido a módulos principales
- Información del usuario logueado
- Navegación entre módulos

**Acceso**: Usuarios autenticados

---

### 7. Interfaz Web Completa

**Descripción**: Interfaz gráfica para todas las operaciones.

**Páginas disponibles**:
- Login
- Dashboard
- Gestión de tipos de objetos
- Gestión de objetos GeneXus
- Importación CSV
- Gestión de usuarios (admin)
- Cambio de contraseña

**Acceso**: Depende de la página (login es pública, el resto requiere autenticación)

---

## Módulos del Sistema

### Módulo: Autenticación (`auth`)

**Objetivo**: Gestionar el acceso al sistema y la identidad de los usuarios.

**Funcionalidades**:
- Registro de usuarios
- Login con credenciales
- Logout
- Cambio de contraseña
- Verificación de JWT
- Tracking de sesiones

**Usuarios que pueden utilizarlo**: Todos (login) / Administradores (gestión)

**Principales acciones**:
- **Iniciar sesión**: Validar credenciales y generar token JWT
- **Cerrar sesión**: Eliminar cookie de autenticación
- **Cambiar contraseña**: Actualizar contraseña propia
- **Resetear contraseña**: Administrador resetea contraseña de otro usuario

---

### Módulo: Tipos de Objetos (`object_types`)

**Objetivo**: Administrar las categorías de objetos GeneXus.

**Funcionalidades**:
- CRUD completo de tipos
- Validación de unicidad (case-insensitive)
- Restricción de eliminación si hay objetos asociados

**Usuarios que pueden utilizarlo**: Usuarios autenticados

**Principales acciones**:
- **Crear tipo**: Registrar nuevo tipo (ej: "PROCEDURE")
- **Listar tipos**: Ver todos los tipos disponibles
- **Actualizar tipo**: Cambiar nombre
- **Eliminar tipo**: Solo si no tiene objetos asociados

---

### Módulo: Objetos GeneXus (`genexus_objects`)

**Objetivo**: Registrar y gestionar objetos técnicos de GeneXus.

**Funcionalidades**:
- CRUD completo de objetos
- Búsqueda y filtrado avanzado
- Paginación
- Auditoría de creación
- Rastreo de origen (MANUAL o CSV)

**Usuarios que pueden utilizarlo**: Usuarios autenticados

**Principales acciones**:
- **Crear objeto**: Registrar nuevo objeto con nombre, descripción y tipo
- **Buscar objetos**: Filtrar por nombre, tipo u origen
- **Actualizar objeto**: Modificar descripción
- **Eliminar objeto**: Remover registro
- **Ver auditoría**: Consultar quién creó el objeto y cuándo

---

### Módulo: Importación (`imports`)

**Objetivo**: Facilitar carga masiva de objetos desde archivos CSV.

**Funcionalidades**:
- Parser de CSV con validación
- Importación en lotes
- Reporte de errores detallado
- Mapping de tipos

**Usuarios que pueden utilizarlo**: Usuarios autenticados

**Principales acciones**:
- **Subir CSV**: Cargar archivo con objetos
- **Validar formato**: Verificar headers y contenido
- **Importar**: Procesar e insertar objetos en BD
- **Ver reporte**: Consultar resultado (éxitos y errores)

---

### Módulo: Interfaz Web (`web`)

**Objetivo**: Proporcionar interfaz gráfica para todas las operaciones.

**Funcionalidades**:
- Páginas HTML renderizadas server-side
- Formularios interactivos
- Modales para acciones
- Tablas con paginación
- Búsqueda en tiempo real

**Usuarios que pueden utilizarlo**: Todos (login es público)

**Principales acciones**:
- **Navegar**: Acceder a diferentes módulos
- **Interactuar**: Realizar operaciones vía interfaz gráfica
- **Visualizar**: Ver información en tablas y formularios

---

## Usuarios, Roles y Permisos

### Tipos de Usuarios

Actualmente el sistema tiene un modelo simple:

1. **Usuarios Autenticados**: Tienen acceso completo a todas las funcionalidades
2. **Usuarios No Autenticados**: Solo pueden acceder a la página de login

> **Nota**: El sistema no tiene roles diferenciados (admin vs usuario regular). Todos los usuarios autenticados tienen los mismos permisos.

### Control de Acceso

**Páginas Públicas**:
- `/web/login` - Página de inicio de sesión
- `/web/change-password` - Cambio de contraseña (requiere estar logueado)

**Páginas Protegidas** (requieren autenticación):
- `/web/` - Dashboard
- `/web/object-types` - Gestión de tipos
- `/web/objects` - Gestión de objetos
- `/web/users` - Gestión de usuarios
- `/web/import` - Importación CSV

**API Protegida**:
Todos los endpoints `/api/...` requieren autenticación excepto `/api/auth/login` y `/api/auth/register`.

### Auditoría

El sistema registra automáticamente:
- **Quién creó cada objeto**: Campo `created_by` en objetos y tipos
- **Cuándo se creó**: Campo `created_at`
- **Última actualización**: Campo `updated_at`
- **Último login**: Campo `last_login` en usuarios

---

## Flujo de Autenticación

### 1. Inicio de Sesión Exitoso

```
1. Usuario accede a /web/login
2. Ingresa username y password
3. Click en "Iniciar Sesión"
   │
   ↓
4. Frontend envía POST a /api/auth/login
   │
   ↓
5. Backend valida credenciales con bcrypt
   │
   ├─ Si son inválidas → Error 401
   │
   └─ Si son válidas:
      │
      ├─ Genera JWT firmado
      ├─ Almacena JWT en cookie HttpOnly
      ├─ Actualiza last_login del usuario
      │
      └─ Verifica must_change_password:
         │
         ├─ Si es true → Redirige a /web/change-password
         │
         └─ Si es false → Redirige a /web/ (Dashboard)
```

### 2. Credenciales Incorrectas

```
1. Usuario ingresa credenciales incorrectas
   │
   ↓
2. Backend verifica usuario y contraseña
   │
   └─ No coinciden → Error 401: "Credenciales inválidas"
      │
      ↓
3. Frontend muestra mensaje de error
4. Usuario puede intentar nuevamente
```

### 3. Contraseña Temporal (Cambio Obligatorio)

```
1. Administrador resetea contraseña de usuario
   │
   ↓
2. Sistema asigna contraseña temporal = username
3. Marca must_change_password = true
   │
   ↓
4. Usuario inicia sesión con contraseña temporal
   │
   ↓
5. Sistema detecta must_change_password = true
   │
   ↓
6. Redirige a /web/change-password (no puede cancelar)
   │
   ↓
7. Usuario ingresa nueva contraseña
8. Sistema valida:
   - Mínimo 6 caracteres
   - No puede ser igual al username
   │
   ↓
9. Sistema actualiza contraseña
10. Marca must_change_password = false
    │
    ↓
11. Usuario puede acceder al sistema normalmente
```

### 4. Cambio de Contraseña Voluntario

```
1. Usuario autenticado accede a configuración
   │
   ↓
2. Selecciona "Cambiar Contraseña"
   │
   ↓
3. Ingresa:
   - Contraseña actual
   - Nueva contraseña
   - Confirmación
   │
   ↓
4. Sistema valida:
   - Contraseña actual es correcta
   - Nueva contraseña cumple requisitos
   - Confirmación coincide
   │
   ↓
5. Sistema actualiza contraseña
   │
   ↓
6. Usuario continúa usando el sistema
```

### 5. Cierre de Sesión

```
1. Usuario click en "Cerrar Sesión"
   │
   ↓
2. Frontend envía POST a /api/auth/logout
   │
   ↓
3. Backend elimina cookie de autenticación
   │
   ↓
4. Usuario es redirigido a /web/login
```

### 6. Sesión Activa

```
1. Usuario accede a cualquier página protegida
   │
   ↓
2. Frontend incluye cookie JWT en el request
   │
   ↓
3. Backend verifica JWT:
   │
   ├─ Si es válido:
   │  │
   │  ├─ Extrae user_id del token
   │  ├─ Consulta usuario en BD
   │  └─ Permite acceso
   │
   └─ Si es inválido/expirado:
      │
      └─ Error 401 → Redirige a login
```

---

## Flujo Funcional de Procesos Principales

### Creación de un Tipo de Objeto

```
1. Usuario autenticado accede a /web/object-types
   │
   ↓
2. Click en "Crear Tipo de Objeto"
   │
   ↓
3. Se abre modal con formulario:
   - Nombre (ej: "PROCEDURE")
   │
   ↓
4. Usuario ingresa nombre y click "Crear"
   │
   ↓
5. Frontend envía POST a /api/object-types
   │
   ↓
6. Backend valida:
   - Nombre no vacío
   - Nombre único (case-insensitive)
   │
   ├─ Si falla validación → Error 400/409
   │
   └─ Si pasa:
      │
      ├─ Crea registro en BD
      ├─ Registra created_by = user_id actual
      └─ Devuelve tipo creado
         │
         ↓
7. Frontend cierra modal y recarga tabla
8. Usuario ve el nuevo tipo en la lista
```

---

### Creación de un Objeto GeneXus

```
1. Usuario autenticado accede a /web/objects
   │
   ↓
2. Click en "Crear Objeto"
   │
   ↓
3. Se abre modal con formulario:
   - Nombre técnico (ej: "AhrPr001")
   - Descripción (ej: "Recupera Tasa Interés")
   - Tipo de objeto (select)
   │
   ↓
4. Usuario completa datos y click "Crear"
   │
   ↓
5. Frontend envía POST a /api/objects
   │
   ↓
6. Backend valida:
   - Nombre no vacío (máx 128 caracteres)
   - Tipo existe
   - (nombre, tipo) no duplicado
   │
   ├─ Si falla → Error 400/404/409
   │
   └─ Si pasa:
      │
      ├─ Crea registro en BD
      ├─ Marca source_type = "MANUAL"
      ├─ Registra created_by = user_id actual
      └─ Devuelve objeto creado
         │
         ↓
7. Frontend cierra modal y recarga tabla
8. Usuario ve el nuevo objeto en la lista
```

---

### Importación de Objetos desde CSV

```
1. Usuario autenticado accede a /web/import
   │
   ↓
2. Selecciona archivo CSV desde su computadora
   │
   ↓
3. Opcionalmente marca "Eliminar objetos existentes"
   │
   ↓
4. Click en "Importar"
   │
   ↓
5. Frontend envía POST a /api/imports/csv con archivo
   │
   ↓
6. Backend procesa:
   │
   ├─ Detecta encoding del archivo (UTF-8, Latin1, etc.)
   ├─ Parsea CSV con delimitador ";"
   ├─ Valida headers: name;description;objectType
   ├─ Si "Eliminar" está marcado → Elimina objetos previos
   │
   └─ Por cada fila:
      │
      ├─ Valida nombre (no vacío, máx 128 caracteres)
      ├─ Valida que objectType exista
      ├─ Valida que (name, type) no esté duplicado
      │
      ├─ Si pasa validación:
      │  │
      │  ├─ Crea objeto en BD
      │  ├─ Marca source_type = "CSV"
      │  └─ Registra created_by = user_id actual
      │
      └─ Si falla:
         │
         └─ Registra error con número de fila y razón
   │
   ↓
7. Backend devuelve resultado:
   - Total procesado
   - Éxitos
   - Errores (con detalle)
   │
   ↓
8. Frontend muestra resumen:
   - "✓ 150 objetos importados"
   - "✗ 5 errores"
   - Lista de errores si existen
   │
   ↓
9. Usuario puede descargar reporte de errores
```

---

### Búsqueda de Objetos

```
1. Usuario en /web/objects
   │
   ↓
2. Ingresa texto en campo de búsqueda (ej: "Ahr")
   │
   ↓
3. Frontend envía GET a /api/objects?search=Ahr
   │
   ↓
4. Backend busca objetos con nombre LIKE '%Ahr%'
   │
   ↓
5. Devuelve resultados paginados
   │
   ↓
6. Frontend muestra tabla con resultados
   │
   ↓
7. Usuario puede:
   - Filtrar por tipo (select)
   - Filtrar por origen (MANUAL/CSV)
   - Navegar páginas
   - Ver detalles
   - Editar
   - Eliminar
```

---

### Restablecimiento de Contraseña (Administrador)

```
1. Administrador en /web/users
   │
   ↓
2. Click en botón "Resetear Contraseña" de un usuario
   │
   ↓
3. Se abre modal de confirmación:
   "La contraseña temporal será igual al nombre de usuario.
    El usuario deberá cambiarla en su próximo login."
   │
   ↓
4. Administrador confirma
   │
   ↓
5. Frontend envía POST a /api/users/{id}/reset-password
   │
   ↓
6. Backend:
   │
   ├─ Obtiene usuario por ID
   ├─ Asigna password = username (hasheado)
   ├─ Marca must_change_password = true
   └─ Guarda cambios
      │
      ↓
7. Frontend muestra mensaje:
   "✓ Contraseña reseteada. La contraseña temporal es: {username}"
   │
   ↓
8. Usuario afectado:
   - En su próximo login usará su username como password
   - Será forzado a cambiar la contraseña
   - No podrá acceder al sistema hasta cambiarla
```

---

### Desactivación de Usuario

```
1. Administrador en /web/users
   │
   ↓
2. Click en toggle "Activo/Inactivo" de un usuario
   │
   ↓
3. Se solicita confirmación
   │
   ↓
4. Frontend envía PATCH a /api/users/{id}/status
   │
   ↓
5. Backend:
   │
   ├─ Obtiene usuario
   ├─ Marca is_active = false
   └─ Guarda cambios
      │
      ↓
6. Usuario desactivado:
   - No puede iniciar sesión
   - Si está logueado, su sesión sigue válida hasta expiración
   - Aparece como "Inactivo" en la lista
```

---

## Reglas de Negocio

### Usuarios

1. **Username único**: No pueden existir dos usuarios con el mismo username
2. **Email único**: No pueden existir dos usuarios con el mismo email
3. **Contraseña mínima**: Las contraseñas deben tener al menos 6 caracteres
4. **Contraseña temporal**: Cuando se resetea, la contraseña temporal es igual al username
5. **Cambio obligatorio**: Si `must_change_password = true`, el usuario debe cambiar su contraseña antes de acceder
6. **Nueva contraseña != username**: Al cambiar contraseña temporal, la nueva no puede ser igual al username
7. **Desactivación**: Los usuarios desactivados (`is_active = false`) no pueden iniciar sesión
8. **Auditoría de login**: Se registra `last_login` cada vez que el usuario inicia sesión

### Tipos de Objetos

1. **Nombre único**: No pueden existir dos tipos con el mismo nombre (case-insensitive)
   - Ejemplo: "PROCEDURE" = "procedure" = "Procedure"
2. **No eliminar si en uso**: No se puede eliminar un tipo si tiene objetos GeneXus asociados
3. **Longitud**: El nombre debe tener entre 1 y 100 caracteres
4. **Auditoría**: Se registra quién creó el tipo (`created_by`)

### Objetos GeneXus

1. **Combinación única**: No pueden existir dos objetos con el mismo nombre y tipo
   - Ejemplo: Puede haber "AhrPr001" de tipo PROCEDURE y "AhrPr001" de tipo TRANSACTION
2. **Tipo debe existir**: El `object_type_id` debe referenciar un tipo existente
3. **Longitud de nombre**: El nombre debe tener entre 1 y 128 caracteres
4. **Origen rastreado**: Cada objeto registra si fue creado MANUAL o via CSV
5. **Auditoría**: Se registra quién creó el objeto (`created_by`)
6. **No cambiar nombre duplicado**: Al actualizar, no se puede cambiar a un nombre que ya existe (para ese tipo)

### Importación CSV

1. **Tamaño máximo**: El archivo no puede superar 50 MB (configurable)
2. **Formato**: Debe ser CSV con delimitador `;`
3. **Headers obligatorios**: Debe tener exactamente `name;description;objectType`
4. **Tipos pre-existentes**: Los tipos referenciados en `objectType` deben existir previamente
5. **Procesamiento en lotes**: Se procesan en lotes de 500 registros (configurable)
6. **Errores no bloquean**: Si una fila falla, se continúa con las siguientes
7. **Reporte completo**: Se reportan hasta 100 errores (configurable)
8. **Origen CSV**: Todos los objetos importados se marcan con `source_type = "CSV"`

### Autenticación y Seguridad

1. **JWT firmado**: Todos los tokens son firmados con `SECRET_KEY`
2. **Expiración**: Los tokens expiran después de 365 días (configurable)
3. **Cookies HttpOnly**: Los tokens se almacenan en cookies inaccesibles desde JavaScript
4. **Hash bcrypt**: Las contraseñas se hashean con bcrypt (12 rounds)
5. **Sin contraseñas en logs**: Nunca se loguean contraseñas (ni siquiera hasheadas)
6. **Verificación en cada request**: Cada endpoint protegido verifica el JWT

---

## Resumen del Funcionamiento

**GeneXus Object Registry** es un sistema integral que:

1. **Centraliza** la gestión de objetos GeneXus en un repositorio único
2. **Organiza** objetos por tipos categorizados
3. **Facilita** la carga masiva mediante importación CSV
4. **Asegura** el acceso mediante autenticación JWT
5. **Audita** todas las operaciones (quién, cuándo)
6. **Proporciona** una interfaz web intuitiva
7. **Expone** una API REST documentada

### Relación entre Módulos

```
┌──────────────────────────────────────────┐
│            USUARIOS (auth)               │
│  - Autenticación                         │
│  - Gestión de credenciales               │
│  - Control de acceso                     │
└────────────┬─────────────────────────────┘
             │ created_by
             │
             ↓
┌──────────────────────────────────────────┐
│       TIPOS DE OBJETOS (object_types)    │
│  - Categorías de objetos GeneXus         │
│  - PROCEDURE, TRANSACTION, etc.          │
└────────────┬─────────────────────────────┘
             │ object_type_id
             │
             ↓
┌──────────────────────────────────────────┐
│     OBJETOS GENEXUS (genexus_objects)    │
│  - Catálogo de objetos técnicos          │
│  - Nombre + Descripción + Tipo           │
│  - Origen: MANUAL o CSV                  │
└────────────┬─────────────────────────────┘
             │
             ↑ importa masivamente
             │
┌──────────────────────────────────────────┐
│        IMPORTACIÓN CSV (imports)         │
│  - Carga masiva desde archivos           │
│  - Validación y procesamiento            │
│  - Reporte de errores                    │
└──────────────────────────────────────────┘
```

### Flujo Típico de Uso

**Configuración Inicial**:
1. Crear usuario administrador
2. Iniciar sesión
3. Crear tipos de objetos básicos (PROCEDURE, TRANSACTION, etc.)

**Uso Diario**:
1. Importar objetos desde CSV (carga inicial)
2. Crear objetos manualmente (nuevos desarrollos)
3. Buscar y consultar objetos
4. Actualizar descripciones
5. Ver auditoría

**Administración**:
1. Crear nuevos usuarios
2. Resetear contraseñas
3. Desactivar usuarios inactivos
4. Consultar estadísticas

---

**El sistema GeneXus Object Registry proporciona una solución completa, segura y eficiente para la gestión centralizada de objetos GeneXus en proyectos de cualquier tamaño.**
