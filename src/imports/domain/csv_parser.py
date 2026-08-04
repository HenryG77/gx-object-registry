"""
Parser para archivos CSV de importación de objetos GeneXus.
"""
import csv
from io import StringIO
from typing import List, Iterator
from pathlib import Path

from src.imports.domain.csv_row import CSVRow
from src.shared.logging.logger import logger


class CSVParser:
    """
    Parser para archivos CSV de objetos GeneXus.

    Formato esperado:
    - Delimitador: punto y coma (;)
    - Encoding: UTF-8
    - Encabezados: name;description;objectType
    - Soporte para campos con comillas cuando contienen caracteres especiales
    """

    DELIMITER = ";"
    ENCODING = "utf-8"
    EXPECTED_HEADERS = ["name", "description", "objectType"]

    def __init__(self, strict_headers: bool = True):
        """
        Inicializa el parser.

        Args:
            strict_headers: Si es True, valida que los headers coincidan exactamente
        """
        self.strict_headers = strict_headers

    def parse_file(self, file_path: Path) -> List[CSVRow]:
        """
        Parsea un archivo CSV desde el sistema de archivos.

        Args:
            file_path: Ruta al archivo CSV

        Returns:
            Lista de filas parseadas

        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si el formato del CSV es inválido
        """
        logger.info("Parsing CSV file", file_path=str(file_path))

        if not file_path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

        with open(file_path, mode="r", encoding=self.ENCODING) as file:
            content = file.read()

        return self.parse_content(content)

    def parse_content(self, content: str) -> List[CSVRow]:
        """
        Parsea el contenido de un CSV.

        Args:
            content: Contenido del CSV como string

        Returns:
            Lista de filas parseadas

        Raises:
            ValueError: Si el formato del CSV es inválido
        """
        logger.info("Parsing CSV content", content_length=len(content))

        rows = []
        reader = csv.DictReader(
            StringIO(content),
            delimiter=self.DELIMITER,
            quotechar='"',
            skipinitialspace=True,
        )

        # Validar headers
        if self.strict_headers and reader.fieldnames != self.EXPECTED_HEADERS:
            raise ValueError(
                f"Headers inválidos. Esperados: {self.EXPECTED_HEADERS}, "
                f"Encontrados: {reader.fieldnames}"
            )

        # Parsear filas
        for index, row_data in enumerate(reader, start=1):
            try:
                row = self._parse_row(index + 1, row_data)  # +1 para contar header
                rows.append(row)
            except Exception as e:
                logger.warning(
                    "Error parsing CSV row",
                    row_number=index + 1,
                    error=str(e),
                    row_data=row_data,
                )
                # Continuar con las siguientes filas
                # El error será manejado por el use case

        logger.info("CSV parsing completed", total_rows=len(rows))
        return rows

    def parse_stream(self, file_stream: Iterator[str]) -> List[CSVRow]:
        """
        Parsea un stream de archivo (útil para archivos subidos por HTTP).

        Args:
            file_stream: Stream de contenido

        Returns:
            Lista de filas parseadas

        Raises:
            ValueError: Si el formato del CSV es inválido
        """
        # Leer todo el contenido del stream
        content = "".join(line for line in file_stream)
        return self.parse_content(content)

    def _parse_row(self, row_number: int, row_data: dict) -> CSVRow:
        """
        Parsea una fila del CSV en una entidad CSVRow.

        Args:
            row_number: Número de fila (para tracking)
            row_data: Diccionario con los datos de la fila

        Returns:
            CSVRow parseada
        """
        # Obtener valores con normalización
        name = self._normalize_string(row_data.get("name", ""))
        description = self._normalize_optional_string(row_data.get("description"))
        object_type_code = self._normalize_string(row_data.get("objectType", ""))

        return CSVRow(
            row_number=row_number,
            name=name,
            description=description,
            object_type_code=object_type_code,
        )

    @staticmethod
    def _normalize_string(value: str) -> str:
        """
        Normaliza un string (trim).

        Args:
            value: Valor a normalizar

        Returns:
            String normalizado
        """
        return value.strip() if value else ""

    @staticmethod
    def _normalize_optional_string(value: str | None) -> str | None:
        """
        Normaliza un string opcional (None si está vacío).

        Args:
            value: Valor a normalizar

        Returns:
            String normalizado o None
        """
        if not value or not value.strip():
            return None
        return value.strip()
