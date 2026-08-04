# Instalación en Servidor con PostgreSQL Ya Instalado

**Guía de Instalación Simplificada para Servidor Ubuntu con PostgreSQL**

Esta guía asume que:
- ✅ El servidor Ubuntu ya está instalado y funcionando
- ✅ PostgreSQL ya está instalado
- ✅ Tienes acceso SSH al servidor
- ✅ Vas a usar acceso directo por IP:PUERTO (sin dominio, sin Nginx)

---

## Tabla de Contenidos

1. [Requisitos Previos](#1-requisitos-previos)
2. [Crear Usuario del Sistema](#2-crear-usuario-del-sistema)
3. [Configurar Base de Datos PostgreSQL](#3-configurar-base-de-datos-postgresql)
4. [Subir el Código al Servidor](#4-subir-el-código-al-servidor)
5. [Instalar Python y Dependencias](#5-instalar-python-y-dependencias)
6. [Configurar Variables de Entorno](#6-configurar-variables-de-entorno)
7. [Configurar Servicio Systemd](#7-configurar-servicio-systemd)
8. [Configurar Puerto de Acceso](#8-configurar-puerto-de-acceso)
9. [Configurar Firewall](#9-configurar-firewall)
10. [Solicitar Apertura de Puerto a Red](#10-solicitar-apertura-de-puerto-a-red)
11. [Verificación Final](#11-verificación-final)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. Requisitos Previos

### 1.1 Información que Necesitas Tener

Antes de empezar, ten a mano:

- 🔑 **Usuario y contraseña SSH** del servidor
- 🌐 **IP del servidor** (ejemplo: 192.168.1.100)
- 🔢 **Puerto que vas a usar** (ejemplo: 8080)
- 👤 **Contacto del administrador de red** (Jorge)

### 1.2 Verificar PostgreSQL

Conéctate al servidor y verifica que PostgreSQL está instalado:

```bash
psql --version
sudo systemctl status postgresql
```

**Resultado esperado:**
```
psql (PostgreSQL) 15.x
Active: active (running)
```

---

## 2. Crear Usuario del Sistema

### 2.1 Crear Usuario `gxapp`

Este usuario correrá la aplicación (por seguridad, NO usar root):

```bash
sudo useradd -m -s /bin/bash gxapp
sudo passwd gxapp
# Ingresa una contraseña segura
```

### 2.2 Crear Directorio de Aplicaciones

```bash
sudo mkdir -p /home/gxapp/apps
sudo chown -R gxapp:gxapp /home/gxapp/apps
```

---

## 3. Configurar Base de Datos PostgreSQL

### 3.1 Crear Usuario y Base de Datos

```bash
sudo -u postgres psql
```

Dentro de `psql`, ejecuta:

```sql
-- Crear usuario
CREATE USER gxapp WITH PASSWORD 'tu_password_seguro_aqui';

-- Crear base de datos
CREATE DATABASE gxregistry_prod OWNER gxapp;

-- Dar permisos
GRANT ALL PRIVILEGES ON DATABASE gxregistry_prod TO gxapp;

-- Salir
\q
```

### 3.2 Verificar Conexión

```bash
psql -U gxapp -d gxregistry_prod -h localhost
# Ingresa el password
# Si conecta correctamente, escribe \q para salir
```

### 3.3 Crear Tablas y Cargar Datos Iniciales

**Opción A: Si tienes un archivo SQL de schema completo**

```bash
psql -U gxapp -d gxregistry_prod -h localhost < schema.sql
```

**Opción B: Crear tablas manualmente**

Conéctate a la base de datos:

```bash
psql -U gxapp -d gxregistry_prod -h localhost
```

Y ejecuta:

```sql
-- Crear tabla de usuarios
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    is_superuser BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla de tipos de objetos
CREATE TABLE object_types (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla de objetos GeneXus
CREATE TABLE genexus_objects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    object_type_id INTEGER REFERENCES object_types(id),
    description TEXT,
    module VARCHAR(255),
    kb_name VARCHAR(255),
    kb_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar los 27 tipos de objetos GeneXus
INSERT INTO object_types (id, name, created_at, updated_at) VALUES
(0, 'TRANSACTION', NOW(), NOW()),
(1, 'PROCEDURE', NOW(), NOW()),
(2, 'REPORT', NOW(), NOW()),
(3, 'MENUBAR', NOW(), NOW()),
(4, 'WORKPANEL', NOW(), NOW()),
(5, 'WEBPANEL', NOW(), NOW()),
(6, 'DATAVIEW', NOW(), NOW()),
(7, 'STRUCTURE', NOW(), NOW()),
(8, 'EXTERNALOBJECT', NOW(), NOW()),
(9, 'DATAPROVIDER', NOW(), NOW()),
(10, 'THEME', NOW(), NOW()),
(11, 'DATASELECTOR', NOW(), NOW()),
(12, 'DOMAIN', NOW(), NOW()),
(13, 'IMAGE', NOW(), NOW()),
(17, 'DASHBOARD', NOW(), NOW()),
(18, 'DATASTORE', NOW(), NOW()),
(19, 'MASTERPAGECONTENT', NOW(), NOW()),
(20, 'BUSINESSCOMPONENT', NOW(), NOW()),
(21, 'PANEL', NOW(), NOW()),
(22, 'SDPANEL', NOW(), NOW()),
(23, 'APIPROCEDURE', NOW(), NOW()),
(24, 'APIOBJECT', NOW(), NOW()),
(25, 'CONTEXTMENU', NOW(), NOW()),
(26, 'DIAGRAM', NOW(), NOW()),
(27, 'CONVERSIONMAP', NOW(), NOW()),
(28, 'LANGUAGE', NOW(), NOW());

-- Crear usuario administrador (password: admin123 - CAMBIAR EN PRODUCCIÓN)
INSERT INTO users (username, email, hashed_password, full_name, is_active, is_superuser)
VALUES (
    'admin',
    'admin@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqXw5L3zKK',
    'Administrador',
    true,
    true
);

\q
```

**⚠️ IMPORTANTE:** El password hasheado anterior corresponde a `admin123`. Cámbialo después del primer login.

---

## 4. Subir el Código al Servidor

### 4.1 Opción A: Clonar desde Git

Si tienes el código en un repositorio Git:

```bash
sudo su - gxapp
cd /home/gxapp/apps
git clone https://github.com/tu-usuario/gx-object-registry.git
cd gx-object-registry
exit
```

### 4.2 Opción B: Subir con SCP

Desde tu máquina local (Windows):

```bash
# Comprimir el proyecto
tar -czf gx-registry.tar.gz gx-object-registry/

# Subir al servidor
scp gx-registry.tar.gz usuario@IP_SERVIDOR:/home/gxapp/apps/

# En el servidor, descomprimir
ssh usuario@IP_SERVIDOR
sudo su - gxapp
cd /home/gxapp/apps
tar -xzf gx-registry.tar.gz
exit
exit
```

### 4.3 Verificar Estructura

```bash
ls -la /home/gxapp/apps/gx-object-registry
```

Deberías ver:
```
drwxr-xr-x  src/
-rw-r--r--  requirements.txt
-rw-r--r--  .env.example
...
```

---

## 5. Instalar Python y Dependencias

### 5.1 Instalar Python 3.10+

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
python3 --version
```

### 5.2 Crear Virtual Environment

```bash
sudo su - gxapp
cd /home/gxapp/apps/gx-object-registry
python3 -m venv venv
source venv/bin/activate
```

### 5.3 Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Tiempo estimado:** 2-5 minutos

### 5.4 Verificar Instalación

```bash
pip list | grep -i fastapi
pip list | grep -i uvicorn
pip list | grep -i asyncpg
```

Deberías ver:
```
fastapi        0.115.6
uvicorn        0.34.0
asyncpg        0.30.0
```

```bash
deactivate
exit
```

---

## 6. Configurar Variables de Entorno

### 6.1 Crear Archivo `.env`

```bash
sudo su - gxapp
cd /home/gxapp/apps/gx-object-registry
vim .env
```

### 6.2 Contenido del Archivo `.env`

```env
# Entorno
ENVIRONMENT=production

# Base de datos
DATABASE_URL=postgresql+asyncpg://gxapp:tu_password_seguro_aqui@localhost:5432/gxregistry_prod

# JWT Secret (generar uno único)
SECRET_KEY=tu_clave_secreta_super_segura_aqui_cambiar_esto

# Configuración de seguridad
ALLOWED_HOSTS=*
CORS_ORIGINS=*

# Logging
LOG_LEVEL=INFO
```

### 6.3 Generar SECRET_KEY Seguro

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copia el resultado y úsalo en `SECRET_KEY`.

### 6.4 Proteger el Archivo

```bash
chmod 600 .env
ls -la .env
```

Resultado esperado:
```
-rw------- 1 gxapp gxapp 245 .env
```

```bash
exit
```

---

## 7. Configurar Servicio Systemd

### 7.1 Crear Archivo de Servicio

```bash
sudo vim /etc/systemd/system/gxregistry.service
```

### 7.2 Contenido del Archivo

```ini
[Unit]
Description=GeneXus Object Registry Service
After=network.target postgresql.service
Requires=postgresql.service

[Service]
Type=simple
User=gxapp
Group=gxapp
WorkingDirectory=/home/gxapp/apps/gx-object-registry
Environment="PATH=/home/gxapp/apps/gx-object-registry/venv/bin"
ExecStart=/home/gxapp/apps/gx-object-registry/venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8080
Restart=always
RestartSec=10

# Seguridad
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

**⚠️ NOTA:** El puerto está configurado en 8080. Si quieres usar otro puerto (8081, 9000, etc.), cámbialo aquí.

### 7.3 Habilitar y Arrancar Servicio

```bash
sudo systemctl daemon-reload
sudo systemctl enable gxregistry
sudo systemctl start gxregistry
```

### 7.4 Verificar Estado

```bash
sudo systemctl status gxregistry
```

**Resultado esperado:**
```
● gxregistry.service - GeneXus Object Registry Service
   Loaded: loaded (/etc/systemd/system/gxregistry.service; enabled)
   Active: active (running) since ...
```

### 7.5 Ver Logs

```bash
sudo journalctl -u gxregistry -f
```

Presiona `Ctrl+C` para salir.

---

## 8. Configurar Puerto de Acceso

### 8.1 Verificar que el Servicio Escucha en el Puerto

```bash
sudo netstat -tlnp | grep :8080
```

**Resultado esperado:**
```
tcp        0      0 0.0.0.0:8080            0.0.0.0:*               LISTEN      12345/python3
```

### 8.2 Probar Acceso Local

```bash
curl -I http://localhost:8080/web/login
```

**Resultado esperado:**
```
HTTP/1.1 200 OK
...
```

---

## 9. Configurar Firewall

### 9.1 Verificar UFW

```bash
sudo ufw status
```

### 9.2 Configurar Reglas

```bash
# Permitir SSH (IMPORTANTE: hacer esto primero)
sudo ufw allow 22/tcp comment 'SSH'

# Permitir el puerto de la aplicación (cambiar 8080 si usas otro puerto)
sudo ufw allow 8080/tcp comment 'GX Registry'
```

### 9.3 Habilitar Firewall

```bash
sudo ufw --force enable
```

### 9.4 Verificar Reglas

```bash
sudo ufw status
```

**Resultado esperado:**
```
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere                  # SSH
8080/tcp                   ALLOW       Anywhere                  # GX Registry
```

---

## 10. Solicitar Apertura de Puerto a Red

### 10.1 Obtener IP del Servidor

```bash
ip addr show | grep "inet " | grep -v 127.0.0.1
```

Ejemplo de resultado:
```
inet 192.168.1.100/24 brd 192.168.1.255 scope global eth0
```

Tu IP es: **192.168.1.100**

### 10.2 Información para Jorge (Administrador de Red)

Envía esta información a Jorge:

```
┌─────────────────────────────────────────────────────┐
│     SOLICITUD DE APERTURA DE PUERTO                 │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Aplicación:  GeneXus Object Registry               │
│  Servidor:    192.168.1.100                         │
│  Puerto:      8080                                   │
│  Protocolo:   TCP                                    │
│  Dirección:   Entrante (Inbound)                    │
│  Desde:       Red interna de la empresa             │
│  Uso:         Acceso web a la aplicación            │
│                                                      │
│  URL de acceso:                                      │
│  http://192.168.1.100:8080/web/login                │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Reemplaza `192.168.1.100` con la IP real de tu servidor.**

---

## 11. Verificación Final

### 11.1 Verificación Local

Desde el servidor:

```bash
curl http://localhost:8080/web/login
```

Deberías ver HTML de la página de login.

### 11.2 Verificación desde Otra Computadora

Desde cualquier computadora en la misma red:

1. Abre un navegador (Chrome, Firefox, Edge)
2. Ve a: `http://IP_DEL_SERVIDOR:8080/web/login`
3. Deberías ver la página de login

### 11.3 Login de Prueba

- **Usuario:** admin
- **Contraseña:** admin123

**⚠️ IMPORTANTE:** Cambia la contraseña del admin inmediatamente.

### 11.4 Verificar Funcionalidad

Una vez logueado, verifica:

1. ✅ Navegación entre secciones (Objetos, Tipos de Objetos, Usuarios)
2. ✅ Importar archivo de objetos GeneXus
3. ✅ Buscar objetos
4. ✅ Logout

---

## 12. Troubleshooting

### 12.1 Servicio No Arranca

**Problema:** `sudo systemctl status gxregistry` muestra "failed"

**Solución:**

```bash
# Ver logs detallados
sudo journalctl -u gxregistry -n 50

# Verificar sintaxis del archivo .env
sudo su - gxapp
cd /home/gxapp/apps/gx-object-registry
cat .env
```

Errores comunes:
- DATABASE_URL incorrecto
- SECRET_KEY vacío
- Permisos incorrectos en archivos

---

### 12.2 No Conecta a la Base de Datos

**Problema:** Error "connection refused" o "password authentication failed"

**Solución:**

```bash
# Verificar que PostgreSQL está corriendo
sudo systemctl status postgresql

# Probar conexión manual
psql -U gxapp -d gxregistry_prod -h localhost

# Verificar usuario y password en .env
sudo su - gxapp
cat /home/gxapp/apps/gx-object-registry/.env | grep DATABASE_URL
```

---

### 12.3 "Token inválido o expirado" al Navegar

**Problema:** Login funciona pero navegación entre secciones falla

**Causa:** Este bug ya fue corregido en [src/auth/presentation/router.py](src/auth/presentation/router.py) y [src/web/templates/login.html](src/web/templates/login.html)

**Verificar:**

```bash
sudo su - gxapp
cd /home/gxapp/apps/gx-object-registry
grep 'path="/"' src/auth/presentation/router.py
```

Deberías ver:
```python
path="/",  # Esta línea debe estar presente
```

---

### 12.4 Error al Importar Objetos (código 0 inválido)

**Problema:** "Código de tipo '0' no válido"

**Causa:** Faltan tipos de objetos en la base de datos

**Solución:**

```bash
psql -U gxapp -d gxregistry_prod -h localhost
```

```sql
-- Verificar cuántos tipos hay
SELECT COUNT(*) FROM object_types;
```

Debería haber **27 tipos**. Si hay menos:

```sql
-- Borrar tipos existentes
DELETE FROM object_types;

-- Insertar los 27 tipos completos (ver sección 3.3)
INSERT INTO object_types (id, name, created_at, updated_at) VALUES
(0, 'TRANSACTION', NOW(), NOW()),
(1, 'PROCEDURE', NOW(), NOW()),
...
```

---

### 12.5 Puerto Ya en Uso

**Problema:** "Address already in use"

**Solución:**

```bash
# Ver qué está usando el puerto 8080
sudo netstat -tlnp | grep :8080

# Si es otro proceso, matarlo o cambiar puerto en el servicio
sudo vim /etc/systemd/system/gxregistry.service
# Cambiar --port 8080 a --port 8081 (u otro puerto disponible)

# Recargar y reiniciar
sudo systemctl daemon-reload
sudo systemctl restart gxregistry

# No olvides actualizar el firewall
sudo ufw allow 8081/tcp comment 'GX Registry'
sudo ufw delete allow 8080/tcp
```

---

### 12.6 No Accede desde Otra Computadora

**Problema:** Desde el navegador en otra PC no carga la página

**Verificar:**

1. **Firewall del servidor:**
   ```bash
   sudo ufw status | grep 8080
   ```
   Debe mostrar `ALLOW`.

2. **Servicio corriendo:**
   ```bash
   sudo systemctl status gxregistry
   ```
   Debe estar `active (running)`.

3. **Escuchando en 0.0.0.0 (no en 127.0.0.1):**
   ```bash
   sudo netstat -tlnp | grep :8080
   ```
   Debe mostrar `0.0.0.0:8080` (NO `127.0.0.1:8080`).

4. **Firewall de red (Jorge debe verificar):**
   - El router/firewall de la empresa debe permitir el puerto 8080
   - Contactar a Jorge con la información de la Sección 10.2

---

### 12.7 Logs para Debugging

```bash
# Ver logs en tiempo real
sudo journalctl -u gxregistry -f

# Ver últimos 100 logs
sudo journalctl -u gxregistry -n 100

# Ver logs con scroll
sudo journalctl -u gxregistry --no-pager

# Ver logs de PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

---

## Resumen de Comandos Útiles

### Gestión del Servicio

```bash
# Estado del servicio
sudo systemctl status gxregistry

# Iniciar servicio
sudo systemctl start gxregistry

# Detener servicio
sudo systemctl stop gxregistry

# Reiniciar servicio
sudo systemctl restart gxregistry

# Ver logs
sudo journalctl -u gxregistry -f
```

### Base de Datos

```bash
# Conectar a la base de datos
psql -U gxapp -d gxregistry_prod -h localhost

# Backup de la base de datos
pg_dump -U gxapp -h localhost gxregistry_prod > backup.sql

# Restaurar backup
psql -U gxapp -d gxregistry_prod -h localhost < backup.sql
```

### Verificación

```bash
# Ver puertos en uso
sudo netstat -tlnp

# Ver estado del firewall
sudo ufw status

# Ver IP del servidor
ip addr show

# Probar conectividad
curl http://localhost:8080/web/login
```

---

## Arquitectura del Despliegue

```
┌─────────────────────────────────────────────────┐
│         Cliente (Navegador Web)                 │
│    http://192.168.1.100:8080/web/login         │
└────────────────┬────────────────────────────────┘
                 │
                 │ Puerto 8080
                 ▼
┌─────────────────────────────────────────────────┐
│         Firewall UFW (Servidor)                 │
│           Permite Puerto 8080                   │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│    Uvicorn (FastAPI App) - 0.0.0.0:8080        │
│    Usuario: gxapp                               │
│    Dir: /home/gxapp/apps/gx-object-registry     │
│    Servicio: gxregistry.service                 │
└────────────────┬────────────────────────────────┘
                 │
                 │ localhost:5432
                 ▼
┌─────────────────────────────────────────────────┐
│        PostgreSQL 15                            │
│        Base de datos: gxregistry_prod           │
│        Usuario: gxapp                           │
└─────────────────────────────────────────────────┘
```

---

## Checklist de Instalación

Usa este checklist para asegurarte de que completaste todos los pasos:

- [ ] PostgreSQL verificado y funcionando
- [ ] Usuario `gxapp` creado
- [ ] Base de datos `gxregistry_prod` creada
- [ ] Usuario PostgreSQL `gxapp` creado
- [ ] Tablas creadas
- [ ] 27 tipos de objetos insertados
- [ ] Usuario admin creado
- [ ] Código subido al servidor
- [ ] Virtual environment creado
- [ ] Dependencias instaladas
- [ ] Archivo `.env` configurado
- [ ] Servicio systemd creado
- [ ] Servicio habilitado y corriendo
- [ ] Puerto 8080 escuchando en 0.0.0.0
- [ ] Firewall UFW configurado (SSH + 8080)
- [ ] Acceso local verificado (curl)
- [ ] Información enviada a Jorge
- [ ] Acceso desde otra PC verificado
- [ ] Login exitoso con admin/admin123
- [ ] Navegación entre secciones funciona
- [ ] Importación de objetos funciona
- [ ] Contraseña de admin cambiada

---

## Contacto y Soporte

Si encuentras problemas no cubiertos en esta guía:

1. **Revisar logs:** `sudo journalctl -u gxregistry -n 100`
2. **Verificar estado:** `sudo systemctl status gxregistry`
3. **Consultar troubleshooting:** Sección 12 de este documento

---

**Documentación generada para: GeneXus Object Registry**
**Versión:** 1.0
**Última actualización:** 2026-08-04
