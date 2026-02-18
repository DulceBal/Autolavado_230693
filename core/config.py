"""
Configuración central de la aplicación.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr



class Settings(BaseSettings):
    """
    Clase de configuración principal de la aplicación.
    """

    # ── Info general ──
    PROJECT_NAME: str = "Autolavado API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # ── Base de datos ──
    DB_HOST: str
    DB_PORT: int = 3307
    DB_USER: str
    DB_PASSWORD: SecretStr
    DB_NAME: str
    DB_ECHO: bool = False

    # ── Seguridad ──
    SECRET_KEY: SecretStr = Field(..., min_length=32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ── Debug ──
    DEBUG: bool = False

    # Configuración de Pydantic para leer el archivo .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def DATABASE_URL(self) -> str:
        """Construye y devuelve la URL de conexión a la base de datos."""
        return (
            f"mysql+pymysql://{self.DB_USER}:"
            f"{self.DB_PASSWORD.get_secret_value()}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


# Instancia global de configuración
settings = Settings()
