from fastapi import HTTPException, UploadFile, File
from injector import Inject
from pydantic import BaseModel
from pydiator_core.interfaces import BaseRequest, BaseHandler

from app.ai_engine.ports import DocumentLoaderPort, TextEmbedderPort
from app.core.ports import MilvusConnectionPort


class DocumentLoaderRequest(BaseModel, BaseRequest):
    file: UploadFile = File(...)


class DocumentLoaderResponse(BaseModel, BaseRequest):
    message: str


class DocumentLoaderHandler(BaseHandler):
    def __init__(
        self,
        document_loader: Inject[DocumentLoaderPort],
        text_embedder: Inject[TextEmbedderPort],
        milvus_client: Inject[MilvusConnectionPort],
    ):
        self.document_loader = document_loader
        self.text_embedder = text_embedder
        self.milvus_client = milvus_client

    async def handle(self, req: DocumentLoaderRequest) -> DocumentLoaderResponse:
        try:
            docs = await self.document_loader.load_document(req.file)
            embed_data = self.text_embedder.embed_docs(docs)
            self.milvus_client.insert_embedding(embed_data, filename=req.file.filename)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        return DocumentLoaderResponse(message=f"{req.file.filename} was uploaded")
