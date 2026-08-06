# Instalación Rápida - GeneXus Object Registry

**Para servidores/VMs que ya tienen instalados:**
- Ubuntu Server 22.04.5 LTS
- OpenSSH Server
- Git
- Python 3.11
- PostgreSQL 15+

---

## 1. Configurar PostgreSQL

```bash
cd /tmp
sudo -u postgres psql -c "CREATE USER gxuser WITH PASSWORD 'gxpassword';"
sudo -u postgres psql -c "CREATE DATABASE gx_object_registry OWNER gxuser;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE gx_object_registry TO gxuser;"
```

## 2. Clonar repositorio

```bash
cd ~
git clone https://github.com/HenryG77/gx-object-registry.git
cd gx-object-registry
```

## 3. Crear entorno virtual

```bash
python3.11 -m venv venv
source venv/bin/activate
```

## 4. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install jinja2
```

## 5. Configurar archivo .env

Generar SECRET_KEY:

```bash
python3.11 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copiar y editar archivo .env:

```bash
cp .env.example .env
nano .env
```

Editar las siguientes variables:

```text
DATABASE_URL=postgresql+asyncpg://gxuser:gxpassword@localhost:5432/gx_object_registry
APP_ENV=production
DEBUG=false
SECRET_KEY=CAMBIAR_ESTA_CLAVE_SECRETA
```

## 6. Ejecutar migraciones de base de datos

```bash
alembic upgrade head
```

## 7. Crear usuario administrador

```bash
python scripts/create_admin.py
```

El script te pedirá:

- **Username**: Nombre de usuario (3-50 caracteres)
- **Email**: Correo electrónico válido
- **Nombre completo**: Opcional
- **Contraseña**: Mínimo 6 caracteres

Ejemplo de credenciales:

```text
Username: admin
Email: admin@example.com
Nombre completo: Administrador
Contraseña: admin123
```

## 8. Iniciar el servidor

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en:

- **Aplicación web**: <http://localhost:8000/>
- **Documentación API**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>

**Nota**: Para acceder desde Windows, asegúrate de tener configurado el port forwarding en VirtualBox para el puerto 8000.

---

## 9. Actualizar código cuando hay cambios (Opcional)

Cuando se hacen cambios en el repositorio, ejecuta estos comandos para actualizar:

```bash
cd ~/gx-object-registry

# Detener el servidor (Ctrl+C si está corriendo)

# Actualizar código desde GitHub
git pull

# Activar entorno virtual
source venv/bin/activate

# Aplicar nuevas migraciones (si las hay)
alembic upgrade head

# Reiniciar el servidor
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Si ya tienes datos y hay problemas con las secuencias

Si después de actualizar e importar datos aparece un error sobre secuencias, ejecuta:

```bash
sudo -u postgres psql -d gx_object_registry -c "SELECT setval('genexus_objects_id_seq', COALESCE((SELECT MAX(id) FROM genexus_objects), 0) + 1, false);"
sudo -u postgres psql -d gx_object_registry -c "SELECT setval('object_types_id_seq', COALESCE((SELECT MAX(id) FROM object_types), 0) + 1, false);"
```

---

## Requisitos previos (deben estar instalados)

Si tu servidor NO tiene estos componentes, usa [instalacion_completa_vm.md](instalacion_completa_vm.md) en su lugar.

- Ubuntu Server 22.04.5 LTS
- OpenSSH Server
- Git
- Python 3.11 (vía deadsnakes PPA)
- PostgreSQL 15+
