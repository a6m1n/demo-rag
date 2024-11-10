from injector import Inject
from pydantic import BaseModel
from pydiator_core.interfaces import BaseRequest, BaseHandler

from app.core.ports import MilvusConnectionPort


class DataLoderRootRequest(BaseModel, BaseRequest):
    ...


class DataLoderRootResponse(BaseModel, BaseRequest):
    message: str


class DataLoderRouteHandler(BaseHandler):
    def __init__(
        self,
        milvus_client: Inject[MilvusConnectionPort],
    ):
        self.milvus_client = milvus_client

    async def handle(self, req: DataLoderRootRequest) -> DataLoderRootResponse:
        print("milvus_client", self.milvus_client.connect())
        return DataLoderRootResponse(message="FastAPI And Milvus works well")
