"""
Configuración de la aplicación.
Lee las variables de entorno del archivo .env
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Database
    database_url: str
    database_pool_size: int = 20
    database_max_overflow: int = 10
    
    # Application
    app_env: str = "development"
    debug: bool = True
    log_level: str = "INFO"
    
    # API
    api_prefix: str = "/api"
    api_version: str = "v1"
    api_title: str = "GeneXus Object Registry"
    api_description: str = "API para administrar objetos de GeneXus"
    
    # CORS
    cors_origins: str = "http://localhost:3000"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convierte CORS_ORIGINS de string a lista"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    # Import Settings
    max_file_size_mb: int = 50
    max_errors_to_report: int = 100
    csv_batch_size: int = 500
    
    # Security
    secret_key: str = "change-this-in-production"
    allowed_hosts: str = "localhost,127.0.0.1"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


# Instancia global de configuración
settings = Settings()
