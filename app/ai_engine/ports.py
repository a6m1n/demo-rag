from abc import abstractmethod
from typing import runtime_checkable, Protocol, Union

import numpy as np
from fastapi import UploadFile


@runtime_checkable
class DocumentLoaderPort(Protocol):
    @staticmethod
    @abstractmethod
    async def load_document(file: Union[UploadFile, str]):
        ...


@runtime_checkable
class TextEmbedderPort(Protocol):
    @abstractmethod
    def embed_docs(self, documents):
        ...

    @abstractmethod
    def embed_text(self, text: str) -> np.ndarray:
        ...
