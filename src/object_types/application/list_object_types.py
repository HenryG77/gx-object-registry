"""
Caso de uso: Listar tipos de objetos.
"""
from typing import List, Tuple

from src.object_types.domain.object_type import ObjectType
from src.object_types.domain.object_type_repository import ObjectTypeRepository


class ListObjectTypes:
    """
    Caso de uso para listar tipos de objetos con paginación.

    Flujo:
    1. Validar parámetros de paginación
    2. Obtener tipos del repositorio
    3. Retornar lista y total
    """

    def __init__(self, repository: ObjectTypeRepository):
        """
        Inicializa el caso de uso.

        Args:
            repository: Repositorio de tipos de objetos
        """
        self.repository = repository

    async def execute(
        self, page: int = 1, page_size: int = 50
    ) -> Tuple[List[ObjectType], int]:
        """
        Ejecuta el caso de uso.

        Args:
            page: Número de página (empezando en 1)
            page_size: Cantidad de elementos por página

        Returns:
            Tupla (lista de tipos, total de registros)

        Raises:
            ValidationError: Si los parámetros son inválidos
        """
        # Validar parámetros
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 50
        if page_size > 1000:
            page_size = 1000

        # Obtener tipos
        types, total = await self.repository.list_all(page, page_size)

        return types, total
