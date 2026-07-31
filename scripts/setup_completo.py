"""
Script para configurar la base de datos completa desde cero.
Ejecuta: python scripts/setup_completo.py
"""
import asyncio
import asyncpg
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

async def setup_database():
    """Configura la base de datos completa: limpia, crea tablas y carga datos."""
    # Obtener DATABASE_URL del .env
    database_url = os.getenv("DATABASE_URL", "")
    database_url = database_url.replace("postgresql+asyncpg://", "postgresql://")

    print("="*60)
    print("  SETUP COMPLETO DE BASE DE DATOS")
    print("  GeneXus Object Registry")
    print("="*60)
    print()

    print("Conectando a la base de datos...")
    conn = await asyncpg.connect(database_url)

    try:
        # ====================================================================
        # PASO 1: LIMPIAR BASE DE DATOS
        # ====================================================================
        print("\n[PASO 1/3] Limpiando base de datos existente...")
        print("-" * 60)

        await conn.execute("DROP TABLE IF EXISTS genexus_objects CASCADE;")
        print("  [OK] Tabla genexus_objects eliminada")

        await conn.execute("DROP TABLE IF EXISTS object_types CASCADE;")
        print("  [OK] Tabla object_types eliminada")

        await conn.execute("DROP SEQUENCE IF EXISTS object_types_id_seq CASCADE;")
        print("  [OK] Secuencia object_types_id_seq eliminada")

        await conn.execute("DROP TABLE IF EXISTS alembic_version CASCADE;")
        print("  [OK] Tabla alembic_version eliminada")

        await conn.execute("DROP TYPE IF EXISTS source_type_enum CASCADE;")
        print("  [OK] Tipo source_type_enum eliminado")

        # ====================================================================
        # PASO 2: CREAR ESTRUCTURA (TABLAS, TIPOS, ÍNDICES)
        # ====================================================================
        print("\n[PASO 2/3] Creando estructura de base de datos...")
        print("-" * 60)

        # Crear tipo ENUM
        await conn.execute("""
            CREATE TYPE source_type_enum AS ENUM ('MANUAL', 'CSV');
        """)
        print("  [OK] Tipo ENUM 'source_type_enum' creado")

        # Crear secuencia para object_types comenzando en 0
        await conn.execute("""
            CREATE SEQUENCE object_types_id_seq
            START WITH 0
            INCREMENT BY 1
            MINVALUE 0
            NO MAXVALUE
            CACHE 1;
        """)
        print("  [OK] Secuencia 'object_types_id_seq' creada (comienza en 0)")

        # Crear tabla object_types
        await conn.execute("""
            CREATE TABLE object_types (
                id INTEGER PRIMARY KEY DEFAULT nextval('object_types_id_seq'),
                name VARCHAR(100) NOT NULL UNIQUE,
                created_at TIMESTAMP NOT NULL DEFAULT now(),
                updated_at TIMESTAMP NOT NULL DEFAULT now()
            );
        """)
        print("  [OK] Tabla 'object_types' creada")

        # Asociar la secuencia con la columna
        await conn.execute("""
            ALTER SEQUENCE object_types_id_seq OWNED BY object_types.id;
        """)
        print("  [OK] Secuencia asociada a object_types.id")

        # Comentarios en object_types
        await conn.execute("""
            COMMENT ON TABLE object_types IS 'Tipos de objetos de GeneXus';
            COMMENT ON COLUMN object_types.id IS 'Identificador unico del tipo de objeto (autoincremental desde 0)';
            COMMENT ON COLUMN object_types.name IS 'Nombre del tipo de objeto (ej: PROCEDURE, TRANSACTION)';
            COMMENT ON COLUMN object_types.created_at IS 'Fecha de creacion';
            COMMENT ON COLUMN object_types.updated_at IS 'Fecha de ultima actualizacion';
        """)

        # Índice case-insensitive
        await conn.execute("""
            CREATE UNIQUE INDEX idx_object_types_name_lower
            ON object_types (lower(name));
        """)
        print("  [OK] Indice 'idx_object_types_name_lower' creado")

        # Crear tabla genexus_objects
        await conn.execute("""
            CREATE TABLE genexus_objects (
                id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                name VARCHAR(128) NOT NULL,
                description TEXT,
                object_type_id INTEGER NOT NULL REFERENCES object_types(id) ON DELETE RESTRICT,
                source_type source_type_enum NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT now(),
                updated_at TIMESTAMP NOT NULL DEFAULT now()
            );
        """)
        print("  [OK] Tabla 'genexus_objects' creada")

        # Comentarios en genexus_objects
        await conn.execute("""
            COMMENT ON TABLE genexus_objects IS 'Objetos de GeneXus';
            COMMENT ON COLUMN genexus_objects.id IS 'Identificador unico del objeto (autoincremental)';
            COMMENT ON COLUMN genexus_objects.name IS 'Nombre tecnico del objeto GeneXus (ej: AhrPr001)';
            COMMENT ON COLUMN genexus_objects.description IS 'Descripcion funcional del objeto';
            COMMENT ON COLUMN genexus_objects.object_type_id IS 'ID del tipo de objeto (FK a object_types)';
            COMMENT ON COLUMN genexus_objects.source_type IS 'Origen del registro (MANUAL o CSV)';
            COMMENT ON COLUMN genexus_objects.created_at IS 'Fecha de creacion';
            COMMENT ON COLUMN genexus_objects.updated_at IS 'Fecha de ultima actualizacion';
        """)

        # Crear índices en genexus_objects
        await conn.execute("""
            CREATE UNIQUE INDEX uq_genexus_objects_name_type
            ON genexus_objects (name, object_type_id);
        """)
        print("  [OK] Indice 'uq_genexus_objects_name_type' creado")

        await conn.execute("""
            CREATE INDEX idx_genexus_objects_object_type_id
            ON genexus_objects (object_type_id);
        """)
        print("  [OK] Indice 'idx_genexus_objects_object_type_id' creado")

        await conn.execute("""
            CREATE INDEX idx_genexus_objects_source_type
            ON genexus_objects (source_type);
        """)
        print("  [OK] Indice 'idx_genexus_objects_source_type' creado")

        await conn.execute("""
            CREATE INDEX idx_genexus_objects_name
            ON genexus_objects (name);
        """)
        print("  [OK] Indice 'idx_genexus_objects_name' creado")

        await conn.execute("""
            CREATE INDEX idx_genexus_objects_created_at
            ON genexus_objects (created_at DESC);
        """)
        print("  [OK] Indice 'idx_genexus_objects_created_at' creado")

        # Crear tabla de versiones de Alembic
        await conn.execute("""
            CREATE TABLE alembic_version (
                version_num VARCHAR(32) NOT NULL,
                CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
            );
        """)
        print("  [OK] Tabla 'alembic_version' creada")

        await conn.execute("""
            INSERT INTO alembic_version (version_num) VALUES ('001');
        """)
        print("  [OK] Version de migracion '001' registrada")

        # ====================================================================
        # RESUMEN
        # ====================================================================
        print("\n" + "="*60)
        print("  SETUP COMPLETADO EXITOSAMENTE")
        print("="*60)

        print("\n  Base de datos lista!")
        print("  La tabla 'object_types' esta vacia.")
        print("  El primer registro que insertes tendra ID = 0")

        print("\n  La base de datos esta lista para usar!")
        print("\n  Ahora puedes ejecutar:")
        print("    python src/main.py")
        print("\n  Y abrir en tu navegador:")
        print("    http://localhost:8000")

    except Exception as e:
        print(f"\n[ERROR] Ocurrio un error: {e}")
        raise

    finally:
        await conn.close()
        print("\nConexion cerrada.")

if __name__ == "__main__":
    asyncio.run(setup_database())
