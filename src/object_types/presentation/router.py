"""
Router de FastAPI para object_types.

Define los endpoints REST para administrar tipos de objetos.
"""
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.shared.database.connection import get_session
from src.object_types.infrastructure.sqlalchemy_object_type_repository import (
    SQLAlchemyObjectTypeRepository,
)
from src.object_types.application.create_object_type import CreateObjectType
from src.object_types.application.list_object_types import ListObjectTypes
from src.object_types.application.get_object_type_by_id import GetObjectTypeById
from src.object_types.application.update_object_type import UpdateObjectType
from src.object_types.application.delete_object_type import DeleteObjectType
from src.object_types.presentation.dtos import (
    CreateObjectTypeRequest,
    UpdateObjectTypeRequest,
    ObjectTypeResponse,
    ObjectTypeListResponse,
)


router = APIRouter(
    prefix="/object-types",
    tags=["Object Types"],
)


# ============================================================================
# Dependency para obtener el repositorio
# ============================================================================


def get_repository(
    session: AsyncSession = Depends(get_session),
) -> SQLAlchemyObjectTypeRepository:
    """
    Dependency injection del repositorio.

    Args:
        session: Sesión de base de datos

    Returns:
        Repositorio de object types
    """
    return SQLAlchemyObjectTypeRepository(session)


# ============================================================================
# Endpoints
# ============================================================================


@router.post(
    "",
    response_model=ObjectTypeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear tipo de objeto",
    description="Crea un nuevo tipo de objeto GeneXus.",
)
async def create_object_type(
    request: CreateObjectTypeRequest,
    repository: SQLAlchemyObjectTypeRepository = Depends(get_repository),
):
    """
    Crea un nuevo tipo de objeto.

    Args:
        request: Datos del tipo a crear
        repository: Repositorio de tipos

    Returns:
        Tipo de objeto creado

    Raises:
        409: Si ya existe un tipo con ese nombre
    """
    use_case = CreateObjectType(repository)
    object_type = await use_case.execute(request.name, id=request.id)
    return ObjectTypeResponse.model_validate(object_type)


@router.get(
    "",
    response_model=ObjectTypeListResponse,
    status_code=status.HTTP_200_OK,
    summary="Listar tipos de objetos",
    description="Obtiene una lista paginada de tipos de objetos.",
)
async def list_object_types(
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(50, ge=1, le=1000, description="Tamaño de página"),
    sort_by: str = Query("id", description="Campo por el que ordenar (id, name, created_at, updated_at)"),
    sort_order: str = Query("asc", description="Orden (asc/desc)"),
    repository: SQLAlchemyObjectTypeRepository = Depends(get_repository),
):
    """
    Lista todos los tipos de objetos con paginación.

    Args:
        page: Número de página (empezando en 1)
        page_size: Cantidad de elementos por página (máximo 1000)
        sort_by: Campo por el que ordenar
        sort_order: Orden (asc/desc)
        repository: Repositorio de tipos

    Returns:
        Lista paginada de tipos
    """
    use_case = ListObjectTypes(repository)
    types, total = await use_case.execute(page, page_size, sort_by, sort_order)

    items = [ObjectTypeResponse.model_validate(t) for t in types]
    return ObjectTypeListResponse.create(items, total, page, page_size)


@router.get(
    "/{object_type_id}",
    response_model=ObjectTypeResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener tipo por ID",
    description="Obtiene un tipo de objeto específico por su ID.",
)
async def get_object_type_by_id(
    object_type_id: int,
    repository: SQLAlchemyObjectTypeRepository = Depends(get_repository),
):
    """
    Obtiene un tipo de objeto por su ID.

    Args:
        object_type_id: ID del tipo a buscar
        repository: Repositorio de tipos

    Returns:
        Tipo de objeto encontrado

    Raises:
        404: Si el tipo no existe
    """
    use_case = GetObjectTypeById(repository)
    object_type = await use_case.execute(object_type_id)
    return ObjectTypeResponse.model_validate(object_type)


@router.patch(
    "/{object_type_id}",
    response_model=ObjectTypeResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar tipo de objeto",
    description="Actualiza el nombre de un tipo de objeto existente.",
)
async def update_object_type(
    object_type_id: int,
    request: UpdateObjectTypeRequest,
    repository: SQLAlchemyObjectTypeRepository = Depends(get_repository),
):
    """
    Actualiza un tipo de objeto.

    Args:
        object_type_id: ID del tipo a actualizar
        request: Datos actualizados
        repository: Repositorio de tipos

    Returns:
        Tipo de objeto actualizado

    Raises:
        404: Si el tipo no existe
        409: Si el nuevo nombre ya existe
    """
    use_case = UpdateObjectType(repository)
    object_type = await use_case.execute(object_type_id, request.name)
    return ObjectTypeResponse.model_validate(object_type)


@router.delete(
    "/{object_type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar tipo de objeto",
    description="Elimina un tipo de objeto. No se puede eliminar si tiene objetos relacionados.",
)
async def delete_object_type(
    object_type_id: int,
    repository: SQLAlchemyObjectTypeRepository = Depends(get_repository),
):
    """
    Elimina un tipo de objeto.

    Args:
        object_type_id: ID del tipo a eliminar
        repository: Repositorio de tipos

    Raises:
        404: Si el tipo no existe
        409: Si el tipo tiene objetos relacionados
    """
    use_case = DeleteObjectType(repository)
    await use_case.execute(object_type_id)
    return None
