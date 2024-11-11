from injector import Inject
from langchain_postgres import PGVector

from app.core.ports import DbConnectionPort
from app.core.settings import Settings
from app.core.utils import MiniLMEmbeddings


class PSQLConnectionProvider(DbConnectionPort):
    def __init__(
        self,
        settings: Inject[Settings],
    ):
        self.uri = settings.DB_URL
        self.embeddings = MiniLMEmbeddings(settings.EMBEDDING_MODEL_NAME)

        self.client = PGVector(
            embeddings=self.embeddings,
            collection_name=self.collection_name,
            connection=self.uri,
            use_jsonb=True,
        )

    def close(self):
        if self.client:
            self.client = None

    def insert_embedding(self, pages):
        return self.client.add_documents(pages)

    def search_data(self, query: str):
        return self.client.similarity_search(query=query, k=5)
