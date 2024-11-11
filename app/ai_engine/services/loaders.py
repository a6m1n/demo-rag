import os
import tempfile
from abc import ABC, abstractmethod
from typing import List

from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


class DocumentLoaderBase(ABC):
    @staticmethod
    @abstractmethod
    async def load(file: UploadFile) -> List[str]:
        pass


class PdfLoader(DocumentLoaderBase):
    @staticmethod
    async def load(file: UploadFile) -> List[Document]:
        # TODO: Refactor it
        temp_file_path = os.path.join(tempfile.gettempdir(), file.filename)

        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name

        loader = PyPDFLoader(temp_file_path)
        documents = loader.load()
        os.remove(temp_file_path)
        return documents


# class TxtLoader(DocumentLoaderBase):
#     @staticmethod
#     async def load(file: UploadFile) -> str:
#         text = await file.read()
#         return text.decode("utf-8")
