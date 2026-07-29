"""
Router FastAPI para importación de objetos desde CSV.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.imports.application.import_csv import ImportCSV
from src.imports.domain.object_type_mapper import ObjectTypeMapper
from src.imports.presentation.dtos import (
    ImportResultResponse,
    ImportErrorDTO,
    ObjectTypeMappingsResponse,
    ObjectTypeMappingDTO,
)
from src.genexus_objects.infrastructure.sqlalchemy_genexus_object_repository import (
    SQLAlchemyGeneXusObjectRepository,
)
from src.object_types.infrastructure.sqlalchemy_object_type_repository import (
    SQLAlchemyObjectTypeRepository,
)
from src.shared.database.connection import get_session
from src.shared.config.settings import settings
from src.shared.logging.logger import logger


router = APIRouter(prefix="/imports", tags=["CSV Imports"])


def get_genexus_object_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> SQLAlchemyGeneXusObjectRepository:
    """Dependency para obtener el repositorio de objetos GeneXus."""
    return SQLAlchemyGeneXusObjectRepository(session)


def get_object_type_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> SQLAlchemyObjectTypeRepository:
    """Dependency para obtener el repositorio de tipos de objeto."""
    return SQLAlchemyObjectTypeRepository(session)


@router.get(
    "/mappings",
    response_model=ObjectTypeMappingsResponse,
    summary="Obtener mappings de tipos de objeto",
    description="Retorna los códigos numéricos y sus correspondientes tipos de objeto para usar en el CSV.",
)
async def get_object_type_mappings(
    object_type_repo: Annotated[
        SQLAlchemyObjectTypeRepository,
        Depends(get_object_type_repository),
    ],
) -> ObjectTypeMappingsResponse:
    """
    Obtiene los mappings de códigos a tipos de objeto.

    Útil para que el usuario sepa qué código usar en el CSV
    para cada tipo de objeto.

    Args:
        object_type_repo: Repositorio de tipos

    Returns:
        Mappings disponibles
    """
    logger.info("Getting object type mappings")

    # Cargar todos los tipos
    object_types = await object_type_repo.list_all()

    if not object_types:
        return ObjectTypeMappingsResponse(mappings=[], total=0)

    # Crear mapper
    mapper = ObjectTypeMapper(object_types)

    # Construir response
    mappings = []
    for code, type_id in mapper.types_by_code.items():
        type_name = mapper.get_type_name(type_id)
        mappings.append(
            ObjectTypeMappingDTO(
                code=code,
                name=type_name or "",
                id=type_id,
            )
        )

    # Ordenar por código numérico
    mappings.sort(key=lambda m: int(m.code))

    return ObjectTypeMappingsResponse(
        mappings=mappings,
        total=len(mappings),
    )


@router.post(
    "/csv",
    response_model=ImportResultResponse,
    status_code=status.HTTP_200_OK,
    summary="Importar objetos desde CSV",
    description="Importa objetos GeneXus desde un archivo CSV. Crea objetos nuevos o actualiza existentes.",
)
async def import_csv_file(
    file: Annotated[UploadFile, File(description="Archivo CSV con objetos GeneXus")],
    genexus_repo: Annotated[
        SQLAlchemyGeneXusObjectRepository,
        Depends(get_genexus_object_repository),
    ],
    object_type_repo: Annotated[
        SQLAlchemyObjectTypeRepository,
        Depends(get_object_type_repository),
    ],
) -> ImportResultResponse:
    """
    Importa objetos GeneXus desde un archivo CSV.

    El CSV debe tener el siguiente formato:
    - Delimitador: punto y coma (;)
    - Encoding: UTF-8
    - Headers: name;description;objectType
    - objectType: código numérico (usar /imports/mappings para ver códigos disponibles)

    Estrategia de importación:
    - Si el objeto (name + type) ya existe: se actualiza
    - Si no existe: se crea nuevo

    Args:
        file: Archivo CSV subido
        genexus_repo: Repositorio de objetos
        object_type_repo: Repositorio de tipos

    Returns:
        Resultado de la importación con estadísticas y errores

    Raises:
        HTTPException: Si el archivo es demasiado grande o tiene formato inválido
    """
    logger.info(
        "Starting CSV import from uploaded file",
        filename=file.filename,
        content_type=file.content_type,
    )

    # Validar tipo de archivo
    if file.content_type not in ["text/csv", "application/csv", "text/plain"]:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Tipo de archivo no soportado: {file.content_type}. Use text/csv.",
        )

    # Validar extensión
    if file.filename and not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo debe tener extensión .csv",
        )

    try:
        # Leer contenido
        content_bytes = await file.read()

        # Validar tamaño
        max_size_bytes = settings.max_file_size_mb * 1024 * 1024
        if len(content_bytes) > max_size_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Archivo demasiado grande. Máximo: {settings.max_file_size_mb}MB",
            )

        # Decodificar a string
        try:
            content_str = content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo debe estar codificado en UTF-8",
            )

        # Ejecutar importación
        use_case = ImportCSV(genexus_repo, object_type_repo)
        result = await use_case.execute(content_str)

        # Convertir a DTO
        response = ImportResultResponse(
            total_rows=result.total_rows,
            success_count=result.success_count,
            created_count=result.created_count,
            updated_count=result.updated_count,
            skipped_count=result.skipped_count,
            error_count=result.error_count,
            has_errors=result.has_errors,
            errors=[
                ImportErrorDTO(
                    row_number=err.row_number,
                    field=err.field,
                    message=err.message,
                    raw_data=err.raw_data,
                )
                for err in result.errors
            ],
            created_ids=result.created_ids,
            updated_ids=result.updated_ids,
        )

        logger.info(
            "CSV import completed",
            filename=file.filename,
            summary=result.get_summary(),
        )

        return response

    except HTTPException:
        raise

    except Exception as e:
        logger.error("Unexpected error during CSV import", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado durante la importación: {str(e)}",
        )
