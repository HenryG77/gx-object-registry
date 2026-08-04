"""
Caso de uso: Eliminar objeto GeneXus.
"""
from src.genexus_objects.domain.genexus_object_repository import GeneXusObjectRepository
from src.shared.errors.exceptions import ObjectNotFoundError
from src.shared.logging.logger import logger


class DeleteGeneXusObject:
    """
    Caso de uso para eliminar un objeto GeneXus.

    Flujo:
    1. Verificar que el objeto existe
    2. Eliminar del repositorio
    """

    def __init__(self, repository: GeneXusObjectRepository):
        """
        Inicializa el caso de uso.

        Args:
            repository: Repositorio de objetos GeneXus
        """
        self.repository = repository

    async def execute(self, object_id: int) -> None:
        """
        Ejecuta el caso de uso.

        Args:
            object_id: ID del objeto a eliminar

        Raises:
            ObjectNotFoundError: Si el objeto no existe
        """
        # Verificar que existe
        genexus_object = await self.repository.find_by_id(object_id)
        if genexus_object is None:
            raise ObjectNotFoundError(str(object_id))

        # Eliminar
        await self.repository.delete(object_id)

        logger.info(
            "GeneXusObject deleted successfully",
            object_id=str(object_id),
        )
