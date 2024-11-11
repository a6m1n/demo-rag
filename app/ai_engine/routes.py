from fastapi import APIRouter, Depends
from pydiator_core.mediatr import pydiator

from app.ai_engine.handlers.ai_dialog_handler import (
    AiQuestionRequest,
    AiQuestionResponse,
)
from app.ai_engine.handlers.document_loader_handler import (
    DocumentLoaderRequest,
    DocumentLoaderResponse,
)
from app.ai_engine.handlers.document_search_handler import (
    DocumentSearchRequest,
    DocumentSearchResponse,
)

ai_router = APIRouter()


@ai_router.post("/load")
async def load_document_route(
    req: DocumentLoaderRequest = Depends(DocumentLoaderRequest),
) -> DocumentLoaderResponse:
    # TODO: 1. move to background
    # TODO: 2. Post MVP: Add notification as optional functionality
    return await pydiator.send(req=req)


@ai_router.get("/search")
async def search_route(
    req: DocumentSearchRequest = Depends(DocumentSearchRequest),
) -> DocumentSearchResponse:
    return await pydiator.send(req=req)


@ai_router.get("/ask-ai")
async def ask_ai_route(
    req: AiQuestionRequest = Depends(AiQuestionRequest),
) -> AiQuestionResponse:
    # TODO: After MVP add auth
    return await pydiator.send(req=req)
