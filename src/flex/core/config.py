from typing import Any, Dict, Optional

from pydantic import BaseSettings, EmailStr, PostgresDsn, validator


class Settings(BaseSettings):
    DEBUG: bool = False
    API_PREFIX = "/api"
    DOCS_URL: str = "/docs"
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    PROJECT_NAME: str
    VERSION: str = "0.1.0"
    disable_docs: bool = False

    @property
    def fastapi_kwargs(
        self,
    ) -> Dict[str, Any]:
        fastapi_kwargs: Dict[str, Any] = {
            "debug": self.DEBUG,
            "docs_url": self.DOCS_URL,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "title": self.PROJECT_NAME,
            "version": self.VERSION,
        }
        if self.disable_docs:
            fastapi_kwargs.update(
                {
                    "docs_url": None,
                    "openapi_url": None,
                    "redoc_url": None,
                }
            )
        return fastapi_kwargs

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 11520
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    SECRET_KEY: str

    @validator(
        "SQLALCHEMY_DATABASE_URI",
        pre=True,
    )
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True


def get_settings() -> Settings:
    return Settings()


settings = Settings()
