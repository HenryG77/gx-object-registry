# 🚀 Setup de la Base de Datos

Sigue estos pasos **en orden** para configurar la base de datos:

## Paso 1: Levantar PostgreSQL

```bash
docker-compose up -d postgres
```

Espera 5-10 segundos para que PostgreSQL esté completamente listo.

## Paso 2: Verificar que está corriendo

```bash
docker-compose ps
```

Deberías ver algo como:
```
NAME                IMAGE          STATUS
postgres-container  postgres:15    Up 10 seconds (healthy)
```

## Paso 3: Ejecutar migraciones (crear tablas)

```bash
alembic upgrade head
```

Esto creará las tablas `object_types` y `genexus_objects`.

## Paso 4: Insertar datos iniciales (seed)

```bash
python scripts/seed_database.py
```

Esto creará 12 tipos de objeto predefinidos (PROCEDURE, TRANSACTION, etc.).

## Paso 5: Levantar la aplicación

```bash
python src/main.py
```

O con uvicorn directamente:
```bash
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## ✅ Verificar

Abre tu navegador en:
- **Swagger UI**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **ReDoc**: http://localhost:8000/redoc

---

## 🔧 Comandos útiles

### Ver logs de PostgreSQL
```bash
docker-compose logs -f postgres
```

### Conectarse a PostgreSQL
```bash
docker-compose exec postgres psql -U gxregistry -d gxregistry_db
```

### Resetear la base de datos
```bash
alembic downgrade base
alembic upgrade head
python scripts/seed_database.py
```

### Ver migraciones aplicadas
```bash
alembic current
```

### Detener todo
```bash
docker-compose down
```
