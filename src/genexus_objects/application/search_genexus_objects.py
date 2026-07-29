"""
Caso de uso: Buscar y filtrar objetos GeneXus.
"""
from typing import List, Tuple, Optional
from uuid import UUID

from src.genexus_objects.domain.genexus_object import GeneXusObject, SourceType
from src.genexus_objects.domain.genexus_object_repository import GeneXusObjectRepository


class SearchGeneXusObjects:
    """
    Caso de uso para buscar objetos GeneXus con filtros avanzados.

    Flujo:
    1. Validar parámetros de búsqueda
    2. Aplicar filtros
    3. Aplicar paginación
    4. Retornar resultados
    """

    def __init__(self, repository: GeneXusObjectRepository):
        """
        Inicializa el caso de uso.

        Args:
            repository: Repositorio de objetos GeneXus
        """
        self.repository = repository

    async def execute(
        self,
        search: Optional[str] = None,
        name: Optional[str] = None,
        object_type_id: Optional[UUID] = None,
        source_type: Optional[SourceType] = None,
        page: int = 1,
        page_size: int = 50,
        sort_by: str = "name",
        sort_order: str = "asc",
    ) -> Tuple[List[GeneXusObject], int]:
        """
        Ejecuta el caso de uso.

        Args:
            search: Búsqueda general en name y description
            name: Filtro exacto por nombre
            object_type_id: Filtro por tipo
            source_type: Filtro por origen (MANUAL/CSV)
            page: Número de página (empezando en 1)
            page_size: Cantidad de elementos por página
            sort_by: Campo por el que ordenar
            sort_order: Orden (asc/desc)

        Returns:
            Tupla (lista de objetos, total de registros)
        """
        # Validar parámetros
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 50
        if page_size > 1000:
            page_size = 1000

        # Validar sort_by
        valid_sort_fields = ["name", "created_at", "updated_at"]
        if sort_by not in valid_sort_fields:
            sort_by = "name"

        # Validar sort_order
        if sort_order not in ["asc", "desc"]:
            sort_order = "asc"

        # Buscar en repositorio
        objects, total = await self.repository.search(
            search=search,
            name=name,
            object_type_id=object_type_id,
            source_type=source_type,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        return objects, total
