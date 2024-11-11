from typing import List

from injector import Inject
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np

from app.ai_engine.ports import TextEmbedderPort
from app.core.settings import Settings


class TextEmbedder(TextEmbedderPort):
    def __init__(
        self,
        settings: Inject[Settings],
    ):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            is_separator_regex=False,
            keep_separator=False,
            separators=["\n\n", ".\n" ". ", "."],
        )

    def embed_docs(self, documents):
        data = []
        for doc in documents:
            for content in self.splitter.split_text(doc.page_content):
                embedding = self.model.encode(content)
                data.append(
                    {
                        "embeddings": embedding,
                        "page_content": content,
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

    def split_documents(self, documents: List[Document]):
        return self.splitter.split_documents(documents)
