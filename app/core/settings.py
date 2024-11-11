from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    MILVUS_URL: str
    EMBEDDING_MODEL_NAME: str = 'all-MiniLM-L6-v2'
