"""
Resultado de la importación de objetos desde CSV.
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ImportError:
    """
    Error ocurrido durante la importación de una fila.
    """
    row_number: int
    field: Optional[str]
    message: str
    raw_data: dict

    def __str__(self) -> str:
        """Representación en string del error."""
        field_info = f" ({self.field})" if self.field else ""
        return f"Fila {self.row_number}{field_info}: {self.message}"


@dataclass
class ImportResult:
    """
    Resultado de una importación CSV.

    Registra estadísticas y errores del proceso de importación.
    Nota: El proceso elimina TODOS los objetos existentes antes de importar,
    por lo que todos los objetos importados son creados nuevos.
    """
    total_rows: int = 0
    created_count: int = 0
    error_count: int = 0
    errors: List[ImportError] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        """Indica si hubo errores durante la importación."""
        return self.error_count > 0

    def add_created(self, object_id: int) -> None:
        """
        Registra un objeto creado.

        Args:
            object_id: ID del objeto creado
        """
        self.created_count += 1

    def add_error(
        self,
        row_number: int,
        message: str,
        field: Optional[str] = None,
        raw_data: Optional[dict] = None,
    ) -> None:
        """
        Registra un error.

        Args:
            row_number: Número de fila (empezando en 1)
            message: Mensaje de error
            field: Campo que causó el error (opcional)
            raw_data: Datos crudos de la fila (opcional)
        """
        self.error_count += 1
        error = ImportError(
            row_number=row_number,
            field=field,
            message=message,
            raw_data=raw_data or {},
        )
        self.errors.append(error)

    def get_summary(self) -> dict:
        """
        Obtiene un resumen del resultado.

        Returns:
            Diccionario con estadísticas de la importación
        """
        return {
            "total_rows": self.total_rows,
            "created_count": self.created_count,
            "error_count": self.error_count,
            "has_errors": self.has_errors,
        }
