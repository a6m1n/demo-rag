from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer


class MiniLMEmbeddings(Embeddings):
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed a list of documents and return their embeddings."""
        return self.model.encode(texts).tolist()

    def embed_query(self, text: str) -> list[float]:
        """Embed a single query and return its embedding."""
        return self.model.encode([text])[0].tolist()
