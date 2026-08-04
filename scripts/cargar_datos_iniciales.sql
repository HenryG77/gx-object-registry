-- ============================================================================
-- SCRIPT PARA CARGAR DATOS INICIALES (SEED DATA)
-- GeneXus Object Registry
-- ============================================================================
-- Este script inserta los tipos de objeto básicos de GeneXus.
-- Ejecuta este script DESPUÉS de crear_base_datos_manual.sql
-- ============================================================================

-- INSERTAR TIPOS DE OBJETO DE GENEXUS
-- Cada tipo representa una categoría de objeto en GeneXus
-- Los UUIDs son generados automáticamente por PostgreSQL

INSERT INTO object_types (name) VALUES
    ('PROCEDURE'),           -- Procedimientos
    ('TRANSACTION'),         -- Transacciones (ABMs)
    ('DATA_PROVIDER'),       -- Proveedores de datos
    ('WEB_PANEL'),          -- Paneles web
    ('WORK_WITH'),          -- Work With (pantallas de consulta)
    ('DASHBOARD'),          -- Dashboards
    ('SD_PANEL'),           -- Smart Devices Panels
    ('MASTER_PAGE'),        -- Páginas maestras
    ('THEME'),              -- Temas visuales
    ('DOMAIN'),             -- Dominios de datos
    ('IMAGE'),              -- Imágenes
    ('STYLE')               -- Estilos CSS
ON CONFLICT (name) DO NOTHING;  -- Si ya existe, no hacer nada (evita errores)

-- ============================================================================
-- VERIFICACIÓN: Ver los tipos de objeto creados
-- ============================================================================

SELECT
    id,
    name,
    created_at,
    updated_at
FROM object_types
ORDER BY name;

-- ============================================================================
-- EJEMPLO: Insertar algunos objetos de prueba
-- ============================================================================

-- Primero obtenemos el ID del tipo PROCEDURE
-- (en una consulta real, sustituye este UUID por el que te devolvió la consulta anterior)

-- Ejemplo de INSERT de un objeto (comentado para que no se ejecute automáticamente)
/*
INSERT INTO genexus_objects (name, description, object_type_id, source_type)
VALUES (
    'AhrPr001',
    'Procedimiento para enviar emails de notificación',
    (SELECT id FROM object_types WHERE name = 'PROCEDURE'),
    'MANUAL'
);

INSERT INTO genexus_objects (name, description, object_type_id, source_type)
VALUES (
    'ClienteMnt',
    'Transacción para mantenimiento de clientes',
    (SELECT id FROM object_types WHERE name = 'TRANSACTION'),
    'MANUAL'
);

INSERT INTO genexus_objects (name, description, object_type_id, source_type)
VALUES (
    'GetProductos',
    'Data Provider que lista productos activos',
    (SELECT id FROM object_types WHERE name = 'DATA_PROVIDER'),
    'MANUAL'
);
*/

-- ============================================================================
-- CONSULTAS ÚTILES PARA VERIFICAR LOS DATOS
-- ============================================================================

-- Ver cuántos tipos de objeto hay
SELECT COUNT(*) as total_tipos FROM object_types;

-- Ver cuántos objetos hay por tipo
SELECT
    ot.name as tipo,
    COUNT(go.id) as cantidad
FROM object_types ot
LEFT JOIN genexus_objects go ON go.object_type_id = ot.id
GROUP BY ot.name
ORDER BY ot.name;

-- Ver todos los objetos con su tipo
SELECT
    go.name as objeto,
    ot.name as tipo,
    go.description,
    go.source_type as origen,
    go.created_at as fecha_creacion
FROM genexus_objects go
INNER JOIN object_types ot ON go.object_type_id = ot.id
ORDER BY go.created_at DESC;

-- ============================================================================
-- FIN DEL SCRIPT
-- ============================================================================
