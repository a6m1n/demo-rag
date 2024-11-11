from injector import Inject
from langchain_core.vectorstores import VectorStoreRetriever
from pydantic import BaseModel
from pydiator_core.interfaces import BaseRequest, BaseHandler
from app.core.infrastructure.psql.psq_connection_provider import PSQLConnectionProvider

from app.ai_engine.services.ai_dialog_service import AIDialogService
from app.core.ports import DbConnectionPort


class AiQuestionRequest(BaseModel, BaseRequest):
    query: str


class AiQuestionResponse(BaseModel, BaseRequest):
    message: str


class AiDialogHandler(BaseHandler):
    def __init__(
        self,
        ai_dialog_service: Inject[AIDialogService],
        db_client: Inject[DbConnectionPort],
    ):
        self.ai_dialog_service = ai_dialog_service
        self.db_client = db_client

    def get_retriever(self) -> VectorStoreRetriever:
        if type(self.db_client) == PSQLConnectionProvider:
            return self.db_client.client.as_retriever()
            # TODO: Connect Milvus
        else:
            raise Exception("unknown database provider")

    async def handle(self, req: AiQuestionRequest) -> AiQuestionResponse:
        message = self.ai_dialog_service.get_answer(
            retriever_db=self.get_retriever(), question=req.query
        )
        return AiQuestionResponse(message=message.content)
