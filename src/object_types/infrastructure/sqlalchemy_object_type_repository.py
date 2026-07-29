"""
Implementación del repositorio de ObjectType usando SQLAlchemy.
"""
from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.object_types.domain.object_type import ObjectType
from src.object_types.domain.object_type_repository import ObjectTypeRepository
from src.object_types.infrastructure.models import ObjectTypeModel
from src.shared.errors.exceptions import (
    ObjectTypeNotFoundError,
    ObjectTypeAlreadyExistsError,
    ObjectTypeInUseError,
    DatabaseError,
)
from src.shared.logging.logger import logger


class SQLAlchemyObjectTypeRepository(ObjectTypeRepository):
    """
    Implementación de ObjectTypeRepository usando SQLAlchemy.

    Traduce entre la entidad de dominio ObjectType y el modelo
    de base de datos ObjectTypeModel.
    """

    def __init__(self, session: AsyncSession):
        """
        Inicializa el repositorio.

        Args:
            session: Sesión activa de SQLAlchemy
        """
        self.session = session

    def _to_domain(self, model: ObjectTypeModel) -> ObjectType:
        """
        Convierte un modelo de BD a entidad de dominio.

        Args:
            model: Modelo de SQLAlchemy

        Returns:
            Entidad de dominio ObjectType
        """
        return ObjectType(
            id=model.id,
            name=model.name,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: ObjectType) -> ObjectTypeModel:
        """
        Convierte una entidad de dominio a modelo de BD.

        Args:
            entity: Entidad de dominio

        Returns:
            Modelo de SQLAlchemy
        """
        return ObjectTypeModel(
            id=entity.id,
            name=entity.name,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def create(self, object_type: ObjectType) -> ObjectType:
        """Crea un nuevo tipo de objeto."""
        try:
            model = self._to_model(object_type)
            self.session.add(model)
            await self.session.flush()

            logger.info(
                "ObjectType created",
                object_type_id=str(object_type.id),
                name=object_type.name,
            )

            return self._to_domain(model)

        except IntegrityError as e:
            await self.session.rollback()
            logger.warning(
                "ObjectType creation failed - already exists",
                name=object_type.name,
            )
            raise ObjectTypeAlreadyExistsError(object_type.name)

        except Exception as e:
            await self.session.rollback()
            logger.error("Database error creating ObjectType", error=str(e))
            raise DatabaseError(str(e))

    async def find_by_id(self, object_type_id: UUID) -> Optional[ObjectType]:
        """Busca un tipo por ID."""
        try:
            stmt = select(ObjectTypeModel).where(ObjectTypeModel.id == object_type_id)
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()

            if model is None:
                return None

            return self._to_domain(model)

        except Exception as e:
            logger.error("Database error finding ObjectType by ID", error=str(e))
            raise DatabaseError(str(e))

    async def find_by_name(self, name: str) -> Optional[ObjectType]:
        """Busca un tipo por nombre (case-insensitive)."""
        try:
            stmt = select(ObjectTypeModel).where(
                func.lower(ObjectTypeModel.name) == func.lower(name.strip())
            )
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()

            if model is None:
                return None

            return self._to_domain(model)

        except Exception as e:
            logger.error("Database error finding ObjectType by name", error=str(e))
            raise DatabaseError(str(e))

    async def exists_by_name(self, name: str) -> bool:
        """Verifica si existe un tipo con ese nombre."""
        result = await self.find_by_name(name)
        return result is not None

    async def list_all(
        self, page: int = 1, page_size: int = 50
    ) -> Tuple[List[ObjectType], int]:
        """Lista tipos con paginación."""
        try:
            # Contar total
            count_stmt = select(func.count()).select_from(ObjectTypeModel)
            total_result = await self.session.execute(count_stmt)
            total = total_result.scalar()

            # Obtener página
            offset = (page - 1) * page_size
            stmt = (
                select(ObjectTypeModel)
                .order_by(ObjectTypeModel.name)
                .limit(page_size)
                .offset(offset)
            )
            result = await self.session.execute(stmt)
            models = result.scalars().all()

            entities = [self._to_domain(model) for model in models]

            return entities, total

        except Exception as e:
            logger.error("Database error listing ObjectTypes", error=str(e))
            raise DatabaseError(str(e))

    async def update(self, object_type: ObjectType) -> ObjectType:
        """Actualiza un tipo de objeto."""
        try:
            # Verificar que existe
            stmt = select(ObjectTypeModel).where(ObjectTypeModel.id == object_type.id)
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()

            if model is None:
                raise ObjectTypeNotFoundError(str(object_type.id))

            # Actualizar campos
            model.name = object_type.name
            model.updated_at = object_type.updated_at

            await self.session.flush()

            logger.info(
                "ObjectType updated",
                object_type_id=str(object_type.id),
                name=object_type.name,
            )

            return self._to_domain(model)

        except ObjectTypeNotFoundError:
            raise

        except IntegrityError:
            await self.session.rollback()
            logger.warning(
                "ObjectType update failed - name already exists",
                name=object_type.name,
            )
            raise ObjectTypeAlreadyExistsError(object_type.name)

        except Exception as e:
            await self.session.rollback()
            logger.error("Database error updating ObjectType", error=str(e))
            raise DatabaseError(str(e))

    async def delete(self, object_type_id: UUID) -> None:
        """Elimina un tipo de objeto."""
        try:
            # Verificar que existe
            model = await self.session.get(ObjectTypeModel, object_type_id)
            if model is None:
                raise ObjectTypeNotFoundError(str(object_type_id))

            # Verificar que no tenga objetos relacionados
            count = await self.count_related_objects(object_type_id)
            if count > 0:
                raise ObjectTypeInUseError(str(object_type_id), count)

            # Eliminar
            await self.session.delete(model)
            await self.session.flush()

            logger.info("ObjectType deleted", object_type_id=str(object_type_id))

        except (ObjectTypeNotFoundError, ObjectTypeInUseError):
            raise

        except Exception as e:
            await self.session.rollback()
            logger.error("Database error deleting ObjectType", error=str(e))
            raise DatabaseError(str(e))

    async def has_related_objects(self, object_type_id: UUID) -> bool:
        """Verifica si tiene objetos relacionados."""
        count = await self.count_related_objects(object_type_id)
        return count > 0

    async def count_related_objects(self, object_type_id: UUID) -> int:
        """
        Cuenta objetos relacionados.

        NOTA: Este método será implementado completamente cuando
        creemos el módulo genexus_objects. Por ahora retorna 0.
        """
        # TODO: Implementar cuando tengamos GeneXusObjectModel
        # from src.genexus_objects.infrastructure.models import GeneXusObjectModel
        # stmt = select(func.count()).select_from(GeneXusObjectModel).where(
        #     GeneXusObjectModel.object_type_id == object_type_id
        # )
        # result = await self.session.execute(stmt)
        # return result.scalar()

        return 0  # Por ahora retorna 0 (no hay objetos relacionados aún)
