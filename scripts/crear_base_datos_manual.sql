-- ============================================================================
-- SCRIPT PARA CREAR LA BASE DE DATOS MANUALMENTE
-- GeneXus Object Registry
-- ============================================================================
-- Este script crea todas las tablas, tipos e índices necesarios.
-- Puedes ejecutarlo en pgAdmin 4 para aprender cómo funciona la estructura.
-- ============================================================================

-- PASO 1: Crear tipo ENUM para el origen de los datos
-- Este tipo permite solo dos valores: 'MANUAL' (creado a mano) o 'CSV' (importado)
CREATE TYPE source_type_enum AS ENUM ('MANUAL', 'CSV');

-- ============================================================================
-- PASO 2: Crear tabla OBJECT_TYPES (Tipos de objetos de GeneXus)
-- ============================================================================
-- Esta tabla almacena los tipos de objetos (PROCEDURE, TRANSACTION, etc.)
CREATE TABLE object_types (
    -- ID único usando UUID (más seguro que integer autoincremental)
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Nombre del tipo (ej: PROCEDURE, TRANSACTION, DATA_PROVIDER)
    name VARCHAR(100) NOT NULL UNIQUE,

    -- Fechas de auditoría (se actualizan automáticamente)
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);

-- Agregar comentarios a la tabla (documentación en la BD)
COMMENT ON TABLE object_types IS 'Tipos de objetos de GeneXus';
COMMENT ON COLUMN object_types.id IS 'Identificador único del tipo de objeto';
COMMENT ON COLUMN object_types.name IS 'Nombre del tipo de objeto (ej: PROCEDURE, TRANSACTION)';
COMMENT ON COLUMN object_types.created_at IS 'Fecha de creación';
COMMENT ON COLUMN object_types.updated_at IS 'Fecha de última actualización';

-- Crear índice case-insensitive para búsquedas por nombre
-- Esto permite buscar "procedure", "PROCEDURE", "Procedure" como iguales
CREATE UNIQUE INDEX idx_object_types_name_lower
ON object_types (lower(name));

-- ============================================================================
-- PASO 3: Crear tabla GENEXUS_OBJECTS (Objetos de GeneXus)
-- ============================================================================
-- Esta tabla almacena los objetos individuales (AhrPr001, ClienteMnt, etc.)
CREATE TABLE genexus_objects (
    -- ID único usando UUID
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Nombre técnico del objeto (ej: AhrPr001, ClienteMnt)
    name VARCHAR(128) NOT NULL,

    -- Descripción funcional (ej: "Procedimiento para enviar emails")
    description TEXT,

    -- Relación con la tabla object_types (Clave Foránea)
    object_type_id UUID NOT NULL REFERENCES object_types(id) ON DELETE RESTRICT,

    -- Origen del registro: ¿fue creado manualmente o importado desde CSV?
    source_type source_type_enum NOT NULL,

    -- Fechas de auditoría
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);

-- Agregar comentarios a la tabla
COMMENT ON TABLE genexus_objects IS 'Objetos de GeneXus';
COMMENT ON COLUMN genexus_objects.id IS 'Identificador único del objeto';
COMMENT ON COLUMN genexus_objects.name IS 'Nombre técnico del objeto GeneXus (ej: AhrPr001)';
COMMENT ON COLUMN genexus_objects.description IS 'Descripción funcional del objeto';
COMMENT ON COLUMN genexus_objects.object_type_id IS 'ID del tipo de objeto (FK a object_types)';
COMMENT ON COLUMN genexus_objects.source_type IS 'Origen del registro (MANUAL o CSV)';
COMMENT ON COLUMN genexus_objects.created_at IS 'Fecha de creación';
COMMENT ON COLUMN genexus_objects.updated_at IS 'Fecha de última actualización';

-- ============================================================================
-- PASO 4: Crear ÍNDICES para optimizar las consultas
-- ============================================================================

-- Índice 1: Unicidad de (nombre + tipo)
-- Esto evita duplicados: no puede haber dos "AhrPr001" del tipo "PROCEDURE"
CREATE UNIQUE INDEX uq_genexus_objects_name_type
ON genexus_objects (name, object_type_id);

-- Índice 2: Búsquedas por tipo de objeto
-- Acelera consultas como "dame todos los PROCEDURES"
CREATE INDEX idx_genexus_objects_object_type_id
ON genexus_objects (object_type_id);

-- Índice 3: Búsquedas por origen (MANUAL vs CSV)
-- Acelera consultas como "dame todos los objetos importados"
CREATE INDEX idx_genexus_objects_source_type
ON genexus_objects (source_type);

-- Índice 4: Ordenamiento por nombre
-- Acelera ordenamientos alfabéticos
CREATE INDEX idx_genexus_objects_name
ON genexus_objects (name);

-- Índice 5: Ordenamiento por fecha (más recientes primero)
-- Acelera consultas como "últimos objetos creados"
CREATE INDEX idx_genexus_objects_created_at
ON genexus_objects (created_at DESC);

-- ============================================================================
-- PASO 5: Crear tabla de control de versiones de Alembic
-- ============================================================================
-- Esta tabla registra qué migraciones se han aplicado
CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Registrar que hemos aplicado la migración inicial
INSERT INTO alembic_version (version_num) VALUES ('001');

-- ============================================================================
-- VERIFICACIÓN: Consultas para revisar que todo se creó correctamente
-- ============================================================================

-- Ver todas las tablas creadas
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- Ver todos los tipos enum creados
SELECT typname
FROM pg_type
WHERE typtype = 'e';

-- Ver todos los índices creados
SELECT tablename, indexname
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

-- ============================================================================
-- FIN DEL SCRIPT
-- ============================================================================
