# Scripts de Utilidad

Este directorio contiene scripts de utilidad para la administración del sistema.

## create_admin.py

Script para crear usuarios en el sistema (especialmente útil para crear el primer usuario administrador).

### Uso

```bash
python scripts/create_admin.py
```

El script te pedirá:
- **Username**: Nombre de usuario (3-50 caracteres)
- **Email**: Correo electrónico válido
- **Nombre completo**: Nombre completo del usuario (opcional)
- **Contraseña**: Contraseña segura (mínimo 6 caracteres)

### Ejemplo

```bash
$ python scripts/create_admin.py

============================================================
  CREAR USUARIO ADMINISTRADOR
============================================================

Ingresa los datos del nuevo usuario:
------------------------------------------------------------
Username (3-50 caracteres): admin
Email: admin@example.com
Nombre completo (opcional): Administrador del Sistema
Contraseña (mínimo 6 caracteres): ******
Confirmar contraseña: ******

------------------------------------------------------------
Datos del usuario:
  Username:  admin
  Email:     admin@example.com
  Nombre:    Administrador del Sistema
------------------------------------------------------------

¿Crear este usuario? (S/n): s

Creando usuario...

✅ Usuario creado exitosamente!

============================================================
  CREDENCIALES DE ACCESO
============================================================
  Username:  admin
  Email:     admin@example.com
  Nombre:    Administrador del Sistema
  ID:        1
============================================================

Puedes iniciar sesión en: http://localhost:8000/web/login
```

### Notas

- Si ya existen usuarios en el sistema, el script te preguntará si quieres crear uno adicional
- Las contraseñas se hashean con bcrypt antes de guardarse en la base de datos
- El script valida que el username y email no estén duplicados

## Crear usuarios adicionales

Puedes ejecutar el script `create_admin.py` múltiples veces para crear usuarios adicionales. No es necesario que sean administradores - todos los usuarios tienen los mismos permisos en el sistema actual.

## reset_password.py

Script para resetear la contraseña de un usuario existente.

### Uso

```bash
python scripts/reset_password.py
```

El script te pedirá:
- **Username o Email**: Identificador del usuario
- **Nueva Contraseña**: Contraseña segura (mínimo 6 caracteres)
- **Confirmar Contraseña**: Confirmación de la nueva contraseña

### Ejemplo

```bash
$ python scripts/reset_password.py

============================================================
  RESETEAR CONTRASENA DE USUARIO
============================================================

Buscar usuario por:
Username o Email: admin

------------------------------------------------------------
Usuario encontrado:
  ID:       1
  Username: admin
  Email:    admin@example.com
  Nombre:   Administrador del Sistema
  Activo:   Si
------------------------------------------------------------

Deseas resetear la contrasena de 'admin'? (s/N): s

Nueva contrasena (minimo 6 caracteres): ******
Confirmar contrasena: ******

============================================================
  CONTRASENA ACTUALIZADA EXITOSAMENTE
============================================================

La contrasena de 'admin' ha sido actualizada.

El usuario puede iniciar sesion en: http://localhost:8000/web/login
```

### Notas

- El script busca el usuario por username o email automáticamente
- La nueva contraseña se hashea con bcrypt antes de guardarse
- Requiere confirmar la nueva contraseña para evitar errores de tipeo

## Alternativa: Usar la API

También puedes crear usuarios usando la API REST directamente:

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "admin123",
    "full_name": "Administrador"
  }'
```

## Solución de problemas

### Error de conexión a la base de datos

Asegúrate de que:
1. PostgreSQL esté corriendo
2. El archivo `.env` tenga la configuración correcta de `DATABASE_URL`
3. La base de datos exista (ejecuta las migraciones de Alembic si es necesario)

### Usuario ya existe

Si intentas crear un usuario con un username o email que ya existe, recibirás un error. Usa credenciales diferentes.
