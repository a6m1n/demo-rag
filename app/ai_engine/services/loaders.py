import os
import tempfile
from abc import ABC, abstractmethod
from typing import List

import aiofiles
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
    async def _prepare_temp_file(file):
        temp_file_path = os.path.join(tempfile.gettempdir(), file.filename)

        async with aiofiles.open(temp_file_path, "wb") as temp_file:
            content = await file.read()
            await temp_file.write(content)

        return temp_file_path

    @staticmethod
    async def load(file: UploadFile) -> List[Document]:
        try:
            temp_file_path = await PdfLoader._prepare_temp_file(file)

            loader = PyPDFLoader(temp_file_path)
            documents = loader.load()
            documents = [
                Document(
                    page_content=doc.page_content,
                    metadata={**doc.metadata, "source": file.filename},
                )
                for doc in documents
            ]
        except Exception as e:
            print(f"Error loading PDF file: {e}")
            raise e
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

        return documents


# class TxtLoader(DocumentLoaderBase):
#     @staticmethod
#     async def load(file: UploadFile) -> str:
#         text = await file.read()
#         return text.decode("utf-8")
