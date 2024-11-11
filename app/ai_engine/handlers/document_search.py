from typing import List, Optional

from injector import Inject
from pydantic import BaseModel, Field
from pydiator_core.interfaces import BaseRequest, BaseHandler

from app.ai_engine.ports import TextEmbedderPort
from app.core.ports import MilvusConnectionPort


class DocumentSearchRequest(BaseModel, BaseRequest):
    query: str
    filename: Optional[str] = Field(None, title="Search only from that file")


class EntityModel(BaseModel):
    page_content: str
    filename: Optional[str]
    page_number: Optional[int]


class DataItemModel(BaseModel):
    id: int
    distance: float
    entity: EntityModel


class DocumentSearchResponse(BaseModel, BaseRequest):
    data: List[DataItemModel]


class DocumentSearcherHandler(BaseHandler):
    def __init__(
        self,
        text_embedder: Inject[TextEmbedderPort],
        milvus_client: Inject[MilvusConnectionPort],
    ):
        self.text_embedder = text_embedder
        self.milvus_client = milvus_client

    async def handle(self, req: DocumentSearchRequest) -> DocumentSearchResponse:
        embed_text = self.text_embedder.embed_text(req.query)
        res = self.milvus_client.search_data(embed_text, filename=req.filename)
        return DocumentSearchResponse(data=[DataItemModel(**i) for i in res[0]])
