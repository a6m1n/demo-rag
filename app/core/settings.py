from enum import Enum

from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseType(str, Enum):
    POSTGRES = "postgres"
    MILVUS = "milvus"


class Settings(BaseSettings):
    DB_URL: str
    DB_TYPE: DatabaseType

    EMBEDDING_MODEL_NAME: str = Field(
        "all-MiniLM-L6-v2", description="Model used for creating embeddings"
    )
    OPENAI_API_KEY: str = Field("EMPTY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
