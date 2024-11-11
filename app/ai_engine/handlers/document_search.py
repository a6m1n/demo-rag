from typing import List, Optional

from injector import Inject
from pydantic import BaseModel, Field
from pydiator_core.interfaces import BaseRequest, BaseHandler

from app.ai_engine.ports import TextEmbedderPort
from app.core.infrastructure.milvus.milvus_connection_provider import (
    MilvusConnectionProvider,
)
from app.core.infrastructure.psql.psq_connection_provider import PSQLConnectionProvider
from app.core.ports import DbConnectionPort


class DocumentSearchRequest(BaseModel, BaseRequest):
    query: str
    filename: Optional[str] = Field(None, title="Search only from that file")


class EntityModel(BaseModel):
    page_content: str
    filename: Optional[str] = Field(None)
    page_number: Optional[int] = Field(None)


class DataItemModel(BaseModel):
    id: Optional[int] = Field(None)
    distance: Optional[float] = Field(None)
    entity: EntityModel


class DocumentSearchResponse(BaseModel, BaseRequest):
    data: List[DataItemModel]


class DocumentSearcherHandler(BaseHandler):
    def __init__(
        self,
        text_embedder: Inject[TextEmbedderPort],
        db_client: Inject[DbConnectionPort],
    ):
        self.text_embedder = text_embedder
        self.db_client = db_client

    def handle_milvus_search(
        self, req: DocumentSearchRequest
    ) -> DocumentSearchResponse:
        embed_text = self.text_embedder.embed_text(req.query)
        res = self.db_client.search_data(embed_text, filename=req.filename)
        return DocumentSearchResponse(data=[DataItemModel(**i) for i in res[0]])

    def handle_pg_search(self, req: DocumentSearchRequest) -> DocumentSearchResponse:
        res = self.db_client.search_data(req.query)
        return DocumentSearchResponse(
            data=[
                DataItemModel(
                    entity=EntityModel(
                        page_content=i.page_content,
                        page_number=i.metadata["page"],
                        filename=i.metadata["source"],
                    )
                )
                for i in res
            ]
        )

    async def handle(self, req: DocumentSearchRequest) -> DocumentSearchResponse:
        data_dict = {
            MilvusConnectionProvider: self.handle_milvus_search,
            PSQLConnectionProvider: self.handle_pg_search,
        }

        return data_dict.get(type(self.db_client))(req)
