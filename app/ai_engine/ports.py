from abc import abstractmethod
from typing import runtime_checkable, Protocol, Union, List

import numpy as np
from fastapi import UploadFile
from langchain_core.documents import Document


@runtime_checkable
class DocumentLoaderPort(Protocol):
    @staticmethod
    @abstractmethod
    async def load_document(file: Union[UploadFile, str]): ...


@runtime_checkable
class TextEmbedderPort(Protocol):
    @abstractmethod
    def embed_docs(self, documents): ...

    @abstractmethod
    def embed_text(self, text: str) -> np.ndarray: ...

    @abstractmethod
    def split_documents(self, documents: List[Document]): ...
