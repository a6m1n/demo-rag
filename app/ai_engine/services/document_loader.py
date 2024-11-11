from typing import Union
from pathlib import Path

from starlette.datastructures import UploadFile

from app.ai_engine.ports import DocumentLoaderPort
from app.ai_engine.services.loaders import PdfLoader


PDF_EXTENSION = ".pdf"
TXT_EXTENSION = ".txt"


class DocumentLoader(DocumentLoaderPort):
    @staticmethod
    async def load_document(file: Union[UploadFile, str]):
        """
        Uploads a document, returns the text, and saves its vectors in Milvus.
        """
        if isinstance(file, UploadFile):
            extension = Path(file.filename).suffix.lower()
            if extension == PDF_EXTENSION:
                return await PdfLoader.load(file)
            # TODO: Refactor and Connect it after MVP
            # elif extension == TXT_EXTENSION:
            #     return await TxtLoader.load(file)
            else:
                raise ValueError(
                    "Unsupported file format. Please provide a .pdf file"
                )
        elif isinstance(file, str):
            return file
        else:
            raise ValueError(
                "Input must be a file path, an UploadFile, or a text string."
            )
