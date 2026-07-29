"""
Entidad que representa una fila del CSV de importación.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class CSVRow:
    """
    Representa una fila parseada del CSV.

    El CSV tiene 3 columnas:
    - name: Nombre del objeto GeneXus
    - description: Descripción funcional
    - objectType: Código numérico del tipo (se mapeará a nombre)
    """
    row_number: int
    name: str
    description: Optional[str]
    object_type_code: str  # Viene como string del CSV

    @property
    def is_valid(self) -> bool:
        """
        Valida que los campos obligatorios estén presentes.

        Returns:
            True si la fila es válida
        """
        # name y object_type_code son obligatorios
        return bool(self.name and self.name.strip() and self.object_type_code)

    def get_validation_error(self) -> Optional[str]:
        """
        Obtiene el mensaje de error de validación si la fila no es válida.

        Returns:
            Mensaje de error o None si es válida
        """
        if not self.name or not self.name.strip():
            return "El campo 'name' es obligatorio y no puede estar vacío"

        if not self.object_type_code:
            return "El campo 'objectType' es obligatorio"

        return None
