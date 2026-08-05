"""
Caso de uso: Importar objetos GeneXus desde CSV.
"""
from typing import List

from src.imports.domain.csv_parser import CSVParser
from src.imports.domain.csv_row import CSVRow
from src.imports.domain.import_result import ImportResult
from src.imports.domain.object_type_mapper import ObjectTypeMapper
from src.genexus_objects.domain.genexus_object import GeneXusObject
from src.genexus_objects.domain.genexus_object_repository import GeneXusObjectRepository
from src.object_types.domain.object_type_repository import ObjectTypeRepository
from src.shared.errors.exceptions import ObjectAlreadyExistsError, ObjectTypeNotFoundError
from src.shared.logging.logger import logger


class ImportCSV:
    """
    Caso de uso para importar objetos GeneXus desde un archivo CSV.

    IMPORTANTE: Esta operación ELIMINA TODOS los objetos existentes
    y los reemplaza con los datos del CSV. Los IDs se reinician desde 1.

    Flujo:
    1. Parsear el archivo CSV
    2. Cargar tipos de objeto para mapping
    3. Eliminar TODOS los objetos existentes
    4. Para cada fila:
       a. Validar formato
       b. Mapear código de tipo a ID
       c. Crear nuevo objeto
    5. Retornar resultado con estadísticas y errores
    """

    def __init__(
        self,
        genexus_object_repository: GeneXusObjectRepository,
        object_type_repository: ObjectTypeRepository,
    ):
        """
        Inicializa el caso de uso.

        Args:
            genexus_object_repository: Repositorio de objetos GeneXus
            object_type_repository: Repositorio de tipos de objeto
        """
        self.genexus_object_repository = genexus_object_repository
        self.object_type_repository = object_type_repository
        self.csv_parser = CSVParser(strict_headers=True)

    async def execute(self, csv_content: str, created_by: int | None = None) -> ImportResult:
        """
        Ejecuta la importación desde contenido CSV.

        Args:
            csv_content: Contenido del archivo CSV
            created_by: ID del usuario que realiza la importación (opcional)

        Returns:
            Resultado de la importación con estadísticas y errores
        """
        logger.info("Starting CSV import", created_by=str(created_by) if created_by else None)
        result = ImportResult()

        try:
            # 1. Parsear CSV
            rows = self.csv_parser.parse_content(csv_content)
            result.total_rows = len(rows)

            if result.total_rows == 0:
                logger.warning("CSV file is empty")
                return result

            # 2. Cargar tipos de objeto para mapping
            object_types, _ = await self.object_type_repository.list_all(page_size=10000)
            if not object_types:
                logger.error("No object types found in database")
                result.add_error(
                    row_number=0,
                    message="No hay tipos de objeto en la base de datos. Cree al menos un tipo antes de importar.",
                )
                return result

            type_mapper = ObjectTypeMapper(object_types)
            logger.info(
                "Object type mappings",
                mappings=type_mapper.get_available_mappings(),
            )

            # 3. Eliminar TODOS los objetos existentes antes de importar
            deleted_count = await self.genexus_object_repository.delete_all()
            logger.info("All existing objects deleted before import", count=deleted_count)

            # 4. Procesar cada fila
            for row in rows:
                await self._process_row(row, type_mapper, result, created_by)

            logger.info(
                "CSV import completed",
                summary=result.get_summary(),
            )

            return result

        except ValueError as e:
            # Error en el formato del CSV
            logger.error("Invalid CSV format", error=str(e))
            result.add_error(
                row_number=0,
                message=f"Formato de CSV inválido: {str(e)}",
            )
            return result

        except Exception as e:
            # Error inesperado
            logger.error("Unexpected error during import", error=str(e))
            result.add_error(
                row_number=0,
                message=f"Error inesperado: {str(e)}",
            )
            return result

    async def _process_row(
        self,
        row: CSVRow,
        type_mapper: ObjectTypeMapper,
        result: ImportResult,
        created_by: int | None = None,
    ) -> None:
        """
        Procesa una fila del CSV.

        Args:
            row: Fila parseada
            type_mapper: Mapper de tipos
            result: Resultado acumulado
            created_by: ID del usuario que realiza la importación (opcional)
        """
        try:
            # Validar formato básico
            if not row.is_valid:
                error_msg = row.get_validation_error()
                result.add_error(
                    row_number=row.row_number,
                    message=error_msg or "Fila inválida",
                    raw_data={
                        "name": row.name,
                        "description": row.description,
                        "objectType": row.object_type_code,
                    },
                )
                return

            # Mapear código de tipo a ID
            object_type_id = type_mapper.get_type_id(row.object_type_code)
            if object_type_id is None:
                result.add_error(
                    row_number=row.row_number,
                    field="objectType",
                    message=f"Código de tipo '{row.object_type_code}' no válido. "
                            f"Tipos disponibles: {type_mapper.get_available_mappings()}",
                    raw_data={
                        "name": row.name,
                        "objectType": row.object_type_code,
                    },
                )
                return

            # Crear nuevo objeto (todos son nuevos porque eliminamos todo antes)
            await self._create_object(row, object_type_id, result, created_by)

        except Exception as e:
            logger.error(
                "Error processing row",
                row_number=row.row_number,
                error=str(e),
            )
            result.add_error(
                row_number=row.row_number,
                message=f"Error procesando fila: {str(e)}",
                raw_data={
                    "name": row.name,
                    "description": row.description,
                    "objectType": row.object_type_code,
                },
            )

    async def _create_object(
        self,
        row: CSVRow,
        object_type_id,
        result: ImportResult,
        created_by: int | None = None,
    ) -> None:
        """
        Crea un nuevo objeto desde la fila CSV.

        Args:
            row: Fila con datos
            object_type_id: ID del tipo de objeto
            result: Resultado acumulado
            created_by: ID del usuario que realiza la importación (opcional)
        """
        try:
            # Crear entidad de dominio
            genexus_object = GeneXusObject.create_from_csv(
                name=row.name,
                object_type_id=object_type_id,
                created_by=created_by,
                description=row.description,
            )

            # Persistir
            created = await self.genexus_object_repository.create(genexus_object)

            result.add_created(created.id)

            logger.debug(
                "Object created from CSV",
                row_number=row.row_number,
                object_id=str(created.id),
                name=created.name,
            )

        except ObjectAlreadyExistsError as e:
            # Race condition: el objeto fue creado entre la verificación y la creación
            result.add_error(
                row_number=row.row_number,
                message=str(e),
                raw_data={
                    "name": row.name,
                    "objectType": row.object_type_code,
                },
            )

        except ObjectTypeNotFoundError as e:
            result.add_error(
                row_number=row.row_number,
                field="objectType",
                message=str(e),
                raw_data={
                    "name": row.name,
                    "objectType": row.object_type_code,
                },
            )

