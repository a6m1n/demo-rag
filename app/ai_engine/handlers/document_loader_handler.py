from fastapi import HTTPException, UploadFile, File
from injector import Inject
from pydantic import BaseModel
from pydiator_core.interfaces import BaseRequest, BaseHandler

from app.ai_engine.ports import DocumentLoaderPort, TextEmbedderPort
from app.core.infrastructure.milvus.milvus_connection_provider import (
    MilvusConnectionProvider,
)
from app.core.infrastructure.psql.psq_connection_provider import PSQLConnectionProvider
from app.core.ports import DbConnectionPort


class DocumentLoaderRequest(BaseModel, BaseRequest):
    file: UploadFile = File(...)


class DocumentLoaderResponse(BaseModel, BaseRequest):
    message: str


class DocumentLoaderHandler(BaseHandler):
    def __init__(
        self,
        document_loader: Inject[DocumentLoaderPort],
        text_embedder: Inject[TextEmbedderPort],
        db_client: Inject[DbConnectionPort],
    ):
        self.document_loader = document_loader
        self.text_embedder = text_embedder
        self.db_client = db_client

    async def handle_creation_for_milvus(self, req: DocumentLoaderRequest):
        docs = await self.document_loader.load_document(req.file)
        embed_data = self.text_embedder.embed_docs(docs)
        self.db_client.insert_embedding(embed_data, filename=req.file.filename)

    async def handle_creation_for_pgvector(self, req: DocumentLoaderRequest):
        docs = await self.document_loader.load_document(req.file)
        splited_documents = self.text_embedder.split_documents(docs)
        self.db_client.insert_embedding(splited_documents)

    async def handle(self, req: DocumentLoaderRequest) -> DocumentLoaderResponse:
        data_dict = {
            MilvusConnectionProvider: self.handle_creation_for_milvus,
            PSQLConnectionProvider: self.handle_creation_for_pgvector,
        }

        handler = data_dict.get(type(self.db_client))
        if not handler:
            raise HTTPException(
                status_code=400, detail="Unsupported database client type"
            )

        try:
            await handler(req)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        return DocumentLoaderResponse(
            message=f"The file '{req.file.filename}' was successfully uploaded"
        )
