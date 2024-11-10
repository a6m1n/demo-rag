from fastapi import APIRouter, Depends
from pydiator_core.mediatr import pydiator

from app.ai_engine.handlers.root_handler import (
    DataLoderRootRequest,
    DataLoderRootResponse,
)

ai_router = APIRouter()


@ai_router.get("/")
# TODO: Refactor; It is an EXAMPLE!
async def root(
    req: DataLoderRootRequest = Depends(DataLoderRootRequest),
) -> DataLoderRootResponse:
    return await pydiator.send(req=req)


@ai_router.post("/load_document")
async def load_document():
    # TODO: Connect it
    ...
