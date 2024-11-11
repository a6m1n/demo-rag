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
    CHAT_GPT_MODEL_NAME: str = "meta-llama/Meta-Llama-3.1-8B-Instruct"
    CHAT_GPT_API_BASE: str = "https://llama3-1-8b-api.llm.lab.epam.com/v1"
    LLM_TEMPERATURE: float = 0.1
    LLM_MAX_TOKENS: int = 200

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
