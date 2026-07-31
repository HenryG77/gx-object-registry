# 🚀 Guía de Inicio Rápido

## ⚡ Forma Más Fácil (Scripts Automáticos)

### 🆕 Primera vez:
```bash
setup_primera_vez.bat
```

### ▶️ Veces subsiguientes:
```bash
iniciar.bat
```

### ⏹️ Para detener:
- Presiona `Ctrl+C` en la terminal donde corre la aplicación

---

## 📋 Forma Manual - Primera Vez (Setup Completo)

Ejecuta estos comandos **solo la primera vez** o después de borrar la base de datos:

```bash
# 1. Asegúrate de que PostgreSQL esté corriendo
#    (verificar en pgAdmin 4 o services.msc)

# 2. Crear las tablas
alembic upgrade head

# 3. Cargar tipos de objeto iniciales
python scripts/seed_database.py

# 4. Levantar la aplicación
python src/main.py
```

## ⚡ Veces Subsiguientes (Inicio Rápido)

Cuando ya está todo configurado, solo necesitas:

```bash
# 1. Asegúrate de que PostgreSQL esté corriendo
#    (verificar en pgAdmin 4)

# 2. Levantar la aplicación
python src/main.py
```

## 🌐 URLs

Después de levantar, abre en tu navegador:

- **Interfaz Web**: http://localhost:8000
- **API Swagger**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🛑 Detener Todo

```bash
# Detener la aplicación
Ctrl+C (en la terminal donde está corriendo)

# Detener PostgreSQL (opcional)
# Opción 1: En pgAdmin 4 -> Click derecho en servidor -> Disconnect
# Opción 2: services.msc -> PostgreSQL -> Detener servicio
```

## 🔄 Reiniciar PostgreSQL

```bash
# Opción 1: En pgAdmin 4
# Click derecho en servidor -> Disconnect
# Luego: Click derecho -> Connect Server

# Opción 2: Servicios de Windows
# Win+R -> services.msc -> PostgreSQL -> Reiniciar
```

## 📊 Verificar Estado

```bash
# Verificar que PostgreSQL está corriendo
# Abrir pgAdmin 4 y conectarse al servidor

# Verificar que la app está corriendo
curl http://localhost:8000/health
# O abre en navegador: http://localhost:8000/health
```

## 🗄️ Conectar con pgAdmin 4

- **Host**: localhost
- **Puerto**: 5432
- **Usuario**: gxregistry
- **Contraseña**: gxregistry123
- **Base de datos**: gxregistry_db

## ⚠️ Problemas Comunes

### La app no encuentra módulos
```bash
# Asegúrate de estar en el directorio del proyecto
cd c:\Users\operador\Proyectos\web\gx-object-registry

# Luego ejecuta
python src/main.py
```

### PostgreSQL no arranca
```bash
# Ver los logs
docker compose logs postgres

# Reiniciar contenedor
docker compose restart postgres
```

### Puerto 8000 ya está en uso
```bash
# Encontrar proceso usando el puerto
netstat -ano | findstr :8000

# Matar el proceso (reemplaza PID)
taskkill /PID <numero_pid> /F
```

### Base de datos vacía
```bash
# Ejecutar seed de nuevo
python scripts/seed_database.py
```

## 📝 Resumen de Comandos Útiles

```bash
# Ver migraciones aplicadas
alembic current

# Historial de migraciones
alembic history

# Resetear base de datos (¡cuidado, borra todo!)
alembic downgrade base
alembic upgrade head
python scripts/seed_database.py
```
