"""
Router FastAPI para genexus_objects.

Define los endpoints REST para gestionar objetos GeneXus.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.domain.user import User
from src.auth.presentation.dependencies import get_current_user
from src.genexus_objects.application.create_genexus_object import CreateGeneXusObject
from src.genexus_objects.application.search_genexus_objects import SearchGeneXusObjects
from src.genexus_objects.application.get_genexus_object_by_id import GetGeneXusObjectById
from src.genexus_objects.application.update_genexus_object import UpdateGeneXusObject
from src.genexus_objects.application.delete_genexus_object import DeleteGeneXusObject
from src.genexus_objects.infrastructure.sqlalchemy_genexus_object_repository import (
    SQLAlchemyGeneXusObjectRepository,
)
from src.genexus_objects.presentation.dtos import (
    CreateGeneXusObjectRequest,
    UpdateGeneXusObjectRequest,
    GeneXusObjectResponse,
    GeneXusObjectListResponse,
    SourceTypeDTO,
)
from src.object_types.infrastructure.sqlalchemy_object_type_repository import (
    SQLAlchemyObjectTypeRepository,
)
from src.shared.database.connection import get_session
from src.shared.logging.logger import logger


router = APIRouter(prefix="/objects", tags=["GeneXus Objects"])


def get_genexus_object_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> SQLAlchemyGeneXusObjectRepository:
    """
    Dependency para obtener el repositorio de objetos GeneXus.

    Args:
        session: Sesión de base de datos

    Returns:
        Repositorio de objetos GeneXus
    """
    return SQLAlchemyGeneXusObjectRepository(session)


def get_object_type_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> SQLAlchemyObjectTypeRepository:
    """
    Dependency para obtener el repositorio de tipos de objeto.

    Args:
        session: Sesión de base de datos

    Returns:
        Repositorio de tipos de objeto
    """
    return SQLAlchemyObjectTypeRepository(session)


@router.post(
    "",
    response_model=GeneXusObjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear objeto GeneXus",
    description="Crea un nuevo objeto GeneXus de forma manual.",
)
async def create_genexus_object(
    request: CreateGeneXusObjectRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    repository: Annotated[
        SQLAlchemyGeneXusObjectRepository,
        Depends(get_genexus_object_repository),
    ],
    object_type_repo: Annotated[
        SQLAlchemyObjectTypeRepository,
        Depends(get_object_type_repository),
    ],
) -> GeneXusObjectResponse:
    """
    Crea un nuevo objeto GeneXus.

    Args:
        request: Datos del objeto a crear
        current_user: Usuario autenticado
        repository: Repositorio de objetos
        object_type_repo: Repositorio de tipos de objeto

    Returns:
        Objeto creado

    Raises:
        401: Si no está autenticado
        ObjectAlreadyExistsError: Si ya existe un objeto con ese nombre y tipo
        ObjectTypeNotFoundError: Si el tipo no existe
    """
    logger.info(
        "Creating GeneXusObject",
        name=request.name,
        object_type_id=str(request.object_type_id),
        created_by=str(current_user.id),
    )

    use_case = CreateGeneXusObject(repository)
    genexus_object = await use_case.execute(
        name=request.name,
        object_type_id=request.object_type_id,
        created_by=current_user.id,
        description=request.description,
        id=request.id,
    )

    # Obtener el nombre del tipo para denormalizar
    object_type = await object_type_repo.find_by_id(genexus_object.object_type_id)
    object_type_name = object_type.name if object_type else None

    response = GeneXusObjectResponse.model_validate(genexus_object)
    response.object_type_name = object_type_name

    return response


@router.get(
    "",
    response_model=GeneXusObjectListResponse,
    summary="Listar y buscar objetos GeneXus",
    description="Lista objetos GeneXus con filtros opcionales y paginación.",
)
async def search_genexus_objects(
    repository: Annotated[
        SQLAlchemyGeneXusObjectRepository,
        Depends(get_genexus_object_repository),
    ],
    object_type_repo: Annotated[
        SQLAlchemyObjectTypeRepository,
        Depends(get_object_type_repository),
    ],
    search: Annotated[str | None, Query(description="Búsqueda en nombre y descripción")] = None,
    name: Annotated[str | None, Query(description="Filtro por nombre (búsqueda parcial)")] = None,
    description: Annotated[str | None, Query(description="Filtro por descripción (búsqueda parcial)")] = None,
    object_type_id: Annotated[int | None, Query(description="Filtro por tipo de objeto")] = None,
    source_type: Annotated[SourceTypeDTO | None, Query(description="Filtro por origen (MANUAL/CSV)")] = None,
    page: Annotated[int, Query(ge=1, description="Número de página")] = 1,
    page_size: Annotated[int, Query(ge=1, le=1000, description="Tamaño de página")] = 50,
    sort_by: Annotated[str, Query(pattern="^(id|name|created_at|updated_at|object_type_name|source_type)$", description="Campo de ordenamiento")] = "id",
    sort_order: Annotated[str, Query(pattern="^(asc|desc)$", description="Orden (asc/desc)")] = "asc",
) -> GeneXusObjectListResponse:
    """
    Busca objetos GeneXus con filtros opcionales.

    Args:
        repository: Repositorio de objetos
        object_type_repo: Repositorio de tipos
        search: Búsqueda general
        name: Filtro por nombre exacto
        object_type_id: Filtro por tipo
        source_type: Filtro por origen
        page: Número de página
        page_size: Tamaño de página
        sort_by: Campo de ordenamiento
        sort_order: Orden

    Returns:
        Lista paginada de objetos
    """
    logger.info(
        "Searching GeneXusObjects",
        search=search,
        name=name,
        object_type_id=str(object_type_id) if object_type_id else None,
        source_type=source_type,
        page=page,
        page_size=page_size,
    )

    # Ejecutar caso de uso
    use_case = SearchGeneXusObjects(repository)
    objects, total = await use_case.execute(
        search=search,
        name=name,
        description=description,
        object_type_id=object_type_id,
        source_type=source_type,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    # Denormalizar nombres de tipos
    # Obtener todos los tipos únicos
    type_ids = list(set(obj.object_type_id for obj in objects))
    types_map = {}
    for type_id in type_ids:
        obj_type = await object_type_repo.find_by_id(type_id)
        if obj_type:
            types_map[type_id] = obj_type.name

    # Crear responses con nombres denormalizados
    items = []
    for obj in objects:
        response = GeneXusObjectResponse.model_validate(obj)
        response.object_type_name = types_map.get(obj.object_type_id)
        items.append(response)

    return GeneXusObjectListResponse.create(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{object_id}",
    response_model=GeneXusObjectResponse,
    summary="Obtener objeto GeneXus por ID",
    description="Obtiene un objeto GeneXus específico por su ID.",
)
async def get_genexus_object(
    object_id: int,
    repository: Annotated[
        SQLAlchemyGeneXusObjectRepository,
        Depends(get_genexus_object_repository),
    ],
    object_type_repo: Annotated[
        SQLAlchemyObjectTypeRepository,
        Depends(get_object_type_repository),
    ],
) -> GeneXusObjectResponse:
    """
    Obtiene un objeto GeneXus por su ID.

    Args:
        object_id: ID del objeto
        repository: Repositorio de objetos
        object_type_repo: Repositorio de tipos

    Returns:
        Objeto encontrado

    Raises:
        ObjectNotFoundError: Si el objeto no existe
    """
    logger.info("Getting GeneXusObject by ID", object_id=str(object_id))

    use_case = GetGeneXusObjectById(repository)
    genexus_object = await use_case.execute(object_id)

    # Denormalizar tipo
    object_type = await object_type_repo.find_by_id(genexus_object.object_type_id)
    object_type_name = object_type.name if object_type else None

    response = GeneXusObjectResponse.model_validate(genexus_object)
    response.object_type_name = object_type_name

    return response


@router.patch(
    "/{object_id}",
    response_model=GeneXusObjectResponse,
    summary="Actualizar objeto GeneXus",
    description="Actualiza parcialmente un objeto GeneXus existente.",
)
async def update_genexus_object(
    object_id: int,
    request: UpdateGeneXusObjectRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    repository: Annotated[
        SQLAlchemyGeneXusObjectRepository,
        Depends(get_genexus_object_repository),
    ],
    object_type_repo: Annotated[
        SQLAlchemyObjectTypeRepository,
        Depends(get_object_type_repository),
    ],
) -> GeneXusObjectResponse:
    """
    Actualiza un objeto GeneXus existente.

    Args:
        object_id: ID del objeto a actualizar
        request: Datos a actualizar
        current_user: Usuario autenticado
        repository: Repositorio de objetos
        object_type_repo: Repositorio de tipos

    Returns:
        Objeto actualizado

    Raises:
        401: Si no está autenticado
        ObjectNotFoundError: Si el objeto no existe
        ObjectAlreadyExistsError: Si el nuevo nombre/tipo ya existe
        ObjectTypeNotFoundError: Si el nuevo tipo no existe
    """
    logger.info(
        "Updating GeneXusObject",
        object_id=str(object_id),
        name=request.name,
        object_type_id=str(request.object_type_id) if request.object_type_id else None,
        user_id=str(current_user.id),
    )

    use_case = UpdateGeneXusObject(repository)
    genexus_object = await use_case.execute(
        object_id=object_id,
        name=request.name,
        description=request.description,
        object_type_id=request.object_type_id,
    )

    # Denormalizar tipo
    object_type = await object_type_repo.find_by_id(genexus_object.object_type_id)
    object_type_name = object_type.name if object_type else None

    response = GeneXusObjectResponse.model_validate(genexus_object)
    response.object_type_name = object_type_name

    return response


@router.delete(
    "/{object_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar objeto GeneXus",
    description="Elimina un objeto GeneXus existente.",
)
async def delete_genexus_object(
    object_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    repository: Annotated[
        SQLAlchemyGeneXusObjectRepository,
        Depends(get_genexus_object_repository),
    ],
) -> None:
    """
    Elimina un objeto GeneXus.

    Args:
        object_id: ID del objeto a eliminar
        current_user: Usuario autenticado
        repository: Repositorio de objetos

    Raises:
        401: Si no está autenticado
        ObjectNotFoundError: Si el objeto no existe
    """
    logger.info(
        "Deleting GeneXusObject",
        object_id=str(object_id),
        user_id=str(current_user.id),
    )

    use_case = DeleteGeneXusObject(repository)
    await use_case.execute(object_id)
