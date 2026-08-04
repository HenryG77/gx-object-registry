"""
Implementación del repositorio de GeneXusObject usando SQLAlchemy.
"""
from typing import Optional, List, Tuple
from sqlalchemy import select, func, or_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from src.genexus_objects.domain.genexus_object import GeneXusObject, SourceType
from src.genexus_objects.domain.genexus_object_repository import GeneXusObjectRepository
from src.genexus_objects.infrastructure.models import GeneXusObjectModel, SourceTypeEnum
from src.object_types.infrastructure.models import ObjectTypeModel
from src.shared.errors.exceptions import (
    ObjectNotFoundError,
    ObjectAlreadyExistsError,
    ObjectTypeNotFoundError,
    DatabaseError,
)
from src.shared.logging.logger import logger


class SQLAlchemyGeneXusObjectRepository(GeneXusObjectRepository):
    """
    Implementación de GeneXusObjectRepository usando SQLAlchemy.

    Traduce entre la entidad de dominio GeneXusObject y el modelo
    de base de datos GeneXusObjectModel.
    """

    def __init__(self, session: AsyncSession):
        """
        Inicializa el repositorio.

        Args:
            session: Sesión activa de SQLAlchemy
        """
        self.session = session

    def _to_domain(self, model: GeneXusObjectModel) -> GeneXusObject:
        """
        Convierte un modelo de BD a entidad de dominio.

        Args:
            model: Modelo de SQLAlchemy

        Returns:
            Entidad de dominio GeneXusObject
        """
        return GeneXusObject(
            id=model.id,
            name=model.name,
            description=model.description,
            object_type_id=model.object_type_id,
            source_type=SourceType(model.source_type.value),
            created_by=model.created_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: GeneXusObject) -> GeneXusObjectModel:
        """
        Convierte una entidad de dominio a modelo de BD.

        Args:
            entity: Entidad de dominio

        Returns:
            Modelo de SQLAlchemy
        """
        return GeneXusObjectModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            object_type_id=entity.object_type_id,
            source_type=SourceTypeEnum(entity.source_type.value),
            created_by=entity.created_by,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def _verify_object_type_exists(self, object_type_id: int) -> None:
        """
        Verifica que el tipo de objeto existe.

        Args:
            object_type_id: ID del tipo a verificar

        Raises:
            ObjectTypeNotFoundError: Si el tipo no existe
        """
        stmt = select(ObjectTypeModel.id).where(ObjectTypeModel.id == object_type_id)
        result = await self.session.execute(stmt)
        exists = result.scalar_one_or_none() is not None

        if not exists:
            raise ObjectTypeNotFoundError(str(object_type_id))

    async def create(self, genexus_object: GeneXusObject) -> GeneXusObject:
        """Crea un nuevo objeto GeneXus."""
        try:
            # Verificar que el tipo existe
            await self._verify_object_type_exists(genexus_object.object_type_id)

            model = self._to_model(genexus_object)

            # Si no se proporciona ID, obtener el siguiente de la secuencia
            if model.id is None:
                from sqlalchemy import text
                result = await self.session.execute(text("SELECT nextval('genexus_objects_id_seq')"))
                model.id = result.scalar()

            self.session.add(model)
            await self.session.flush()

            logger.info(
                "GeneXusObject created",
                object_id=str(model.id),
                name=genexus_object.name,
                object_type_id=str(genexus_object.object_type_id),
            )

            return self._to_domain(model)

        except ObjectTypeNotFoundError:
            await self.session.rollback()
            raise

        except IntegrityError as e:
            await self.session.rollback()
            logger.warning(
                "GeneXusObject creation failed - already exists",
                name=genexus_object.name,
                object_type_id=str(genexus_object.object_type_id),
            )
            raise ObjectAlreadyExistsError(
                genexus_object.name,
                str(genexus_object.object_type_id),
            )

        except Exception as e:
            await self.session.rollback()
            logger.error("Database error creating GeneXusObject", error=str(e))
            raise DatabaseError(str(e))

    async def bulk_create(self, objects: List[GeneXusObject]) -> List[GeneXusObject]:
        """Crea múltiples objetos en lote."""
        try:
            models = [self._to_model(obj) for obj in objects]
            self.session.add_all(models)
            await self.session.flush()

            logger.info("Bulk create GeneXusObjects", count=len(objects))

            return [self._to_domain(model) for model in models]

        except Exception as e:
            await self.session.rollback()
            logger.error("Database error bulk creating GeneXusObjects", error=str(e))
            raise DatabaseError(str(e))

    async def find_by_id(self, object_id: int) -> Optional[GeneXusObject]:
        """Busca un objeto por ID."""
        try:
            stmt = (
                select(GeneXusObjectModel)
                .options(selectinload(GeneXusObjectModel.object_type))
                .where(GeneXusObjectModel.id == object_id)
            )
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()

            if model is None:
                return None

            return self._to_domain(model)

        except Exception as e:
            logger.error("Database error finding GeneXusObject by ID", error=str(e))
            raise DatabaseError(str(e))

    async def find_by_name_and_type(
        self,
        name: str,
        object_type_id: int,
    ) -> Optional[GeneXusObject]:
        """Busca un objeto por nombre y tipo."""
        try:
            stmt = (
                select(GeneXusObjectModel)
                .options(selectinload(GeneXusObjectModel.object_type))
                .where(
                    GeneXusObjectModel.name == name.strip(),
                    GeneXusObjectModel.object_type_id == object_type_id,
                )
            )
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()

            if model is None:
                return None

            return self._to_domain(model)

        except Exception as e:
            logger.error("Database error finding GeneXusObject by name and type", error=str(e))
            raise DatabaseError(str(e))

    async def exists_by_name_and_type(
        self,
        name: str,
        object_type_id: int,
    ) -> bool:
        """Verifica si existe un objeto con ese nombre y tipo."""
        result = await self.find_by_name_and_type(name, object_type_id)
        return result is not None

    async def search(
        self,
        search: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        object_type_id: Optional[int] = None,
        source_type: Optional[SourceType] = None,
        page: int = 1,
        page_size: int = 50,
        sort_by: str = "name",
        sort_order: str = "asc",
    ) -> Tuple[List[GeneXusObject], int]:
        """Búsqueda avanzada con filtros."""
        try:
            # Construir query base
            query = select(GeneXusObjectModel).options(
                selectinload(GeneXusObjectModel.object_type)
            )

            # Aplicar filtros
            filters = []

            # Búsqueda general en name y description
            if search:
                search_pattern = f"%{search}%"
                filters.append(
                    or_(
                        GeneXusObjectModel.name.ilike(search_pattern),
                        GeneXusObjectModel.description.ilike(search_pattern),
                    )
                )

            # Filtro por nombre (búsqueda parcial con ILIKE)
            if name:
                name_pattern = f"%{name}%"
                filters.append(GeneXusObjectModel.name.ilike(name_pattern))

            # Filtro por descripción (búsqueda parcial con ILIKE)
            if description:
                description_pattern = f"%{description}%"
                filters.append(GeneXusObjectModel.description.ilike(description_pattern))

            # Filtro por tipo
            if object_type_id is not None:
                filters.append(GeneXusObjectModel.object_type_id == object_type_id)

            # Filtro por origen
            if source_type:
                filters.append(GeneXusObjectModel.source_type == SourceTypeEnum(source_type.value))

            # Aplicar filtros al query
            if filters:
                query = query.where(*filters)

            # Contar total
            count_query = select(func.count()).select_from(query.subquery())
            total_result = await self.session.execute(count_query)
            total = total_result.scalar()

            # Aplicar ordenamiento
            if sort_by == "id":
                order_col = GeneXusObjectModel.id
            elif sort_by == "created_at":
                order_col = GeneXusObjectModel.created_at
            elif sort_by == "updated_at":
                order_col = GeneXusObjectModel.updated_at
            elif sort_by == "object_type_name":
                order_col = ObjectTypeModel.name
            elif sort_by == "source_type":
                order_col = GeneXusObjectModel.source_type
            else:  # default: name
                order_col = GeneXusObjectModel.name

            # Agregar join si se ordena por object_type_name
            if sort_by == "object_type_name":
                query = query.join(ObjectTypeModel, GeneXusObjectModel.object_type_id == ObjectTypeModel.id)

            if sort_order == "desc":
                query = query.order_by(order_col.desc())
            else:
                query = query.order_by(order_col.asc())

            # Aplicar paginación
            offset = (page - 1) * page_size
            query = query.limit(page_size).offset(offset)

            # Ejecutar query
            result = await self.session.execute(query)
            models = result.scalars().all()

            entities = [self._to_domain(model) for model in models]

            return entities, total

        except Exception as e:
            logger.error("Database error searching GeneXusObjects", error=str(e))
            raise DatabaseError(str(e))

    async def update(self, genexus_object: GeneXusObject) -> GeneXusObject:
        """Actualiza un objeto existente."""
        try:
            # Buscar objeto
            stmt = select(GeneXusObjectModel).where(
                GeneXusObjectModel.id == genexus_object.id
            )
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()

            if model is None:
                raise ObjectNotFoundError(str(genexus_object.id))

            # Verificar que el nuevo tipo existe (si cambió)
            if model.object_type_id != genexus_object.object_type_id:
                await self._verify_object_type_exists(genexus_object.object_type_id)

            # Actualizar campos
            model.name = genexus_object.name
            model.description = genexus_object.description
            model.object_type_id = genexus_object.object_type_id
            model.updated_at = genexus_object.updated_at

            await self.session.flush()

            logger.info(
                "GeneXusObject updated",
                object_id=str(genexus_object.id),
                name=genexus_object.name,
            )

            return self._to_domain(model)

        except (ObjectNotFoundError, ObjectTypeNotFoundError):
            raise

        except IntegrityError:
            await self.session.rollback()
            logger.warning(
                "GeneXusObject update failed - duplicate",
                name=genexus_object.name,
                object_type_id=str(genexus_object.object_type_id),
            )
            raise ObjectAlreadyExistsError(
                genexus_object.name,
                str(genexus_object.object_type_id),
            )

        except Exception as e:
            await self.session.rollback()
            logger.error("Database error updating GeneXusObject", error=str(e))
            raise DatabaseError(str(e))

    async def bulk_update(self, objects: List[GeneXusObject]) -> List[GeneXusObject]:
        """Actualiza múltiples objetos en lote."""
        try:
            updated = []
            for obj in objects:
                updated_obj = await self.update(obj)
                updated.append(updated_obj)

            logger.info("Bulk update GeneXusObjects", count=len(objects))

            return updated

        except Exception as e:
            await self.session.rollback()
            logger.error("Database error bulk updating GeneXusObjects", error=str(e))
            raise DatabaseError(str(e))

    async def delete(self, object_id: int) -> None:
        """Elimina un objeto."""
        try:
            # Verificar que existe
            model = await self.session.get(GeneXusObjectModel, object_id)
            if model is None:
                raise ObjectNotFoundError(str(object_id))

            # Eliminar
            await self.session.delete(model)
            await self.session.flush()

            logger.info("GeneXusObject deleted", object_id=str(object_id))

        except ObjectNotFoundError:
            raise

        except Exception as e:
            await self.session.rollback()
            logger.error("Database error deleting GeneXusObject", error=str(e))
            raise DatabaseError(str(e))

    async def delete_all(self) -> int:
        """Elimina TODOS los objetos y reinicia la secuencia de IDs."""
        try:
            from sqlalchemy import text, func, delete

            # Contar cuántos vamos a eliminar
            count_stmt = select(func.count()).select_from(GeneXusObjectModel)
            count_result = await self.session.execute(count_stmt)
            total = count_result.scalar()

            # Eliminar todos los registros
            delete_stmt = delete(GeneXusObjectModel)
            await self.session.execute(delete_stmt)

            # Reiniciar la secuencia de IDs a 1
            await self.session.execute(
                text("ALTER SEQUENCE genexus_objects_id_seq RESTART WITH 1")
            )

            await self.session.flush()

            logger.info("All GeneXusObjects deleted and sequence reset", count=total)

            return total

        except Exception as e:
            await self.session.rollback()
            logger.error("Database error deleting all GeneXusObjects", error=str(e))
            raise DatabaseError(str(e))
