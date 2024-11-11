from injector import Inject
from sentence_transformers import SentenceTransformer
import numpy as np

from app.ai_engine.ports import TextEmbedderPort
from app.core.settings import Settings


class TextEmbedder(TextEmbedderPort):
    def __init__(self, settings: Inject[Settings],):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)

    def embed_docs(self, documents):
        data = []
        for doc in documents:
            embedding = self.model.encode(doc.page_content)
            data.append(
                {
                    "embeddings": embedding,
                    "page_content": doc.page_content,
                    "page_number": doc.metadata["page"],
                }
            )

        return data

    def embed_text(self, text: str) -> np.ndarray:
        """
        Transforms text into a vector representation using SentenceTransformer
        """
        embedding = self.model.encode(text)
        return np.array(embedding, dtype=np.float32)
