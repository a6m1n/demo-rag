import injector

from app.ai_engine.ports import DocumentLoaderPort, TextEmbedderPort
from app.ai_engine.services.document_loader import DocumentLoader
from app.ai_engine.services.text_embedder import TextEmbedder
from app.core.settings import Settings


class AiEngineModule(injector.Module):
    @injector.provider
    @injector.singleton
    def get_document_loader(self) -> DocumentLoaderPort:
        return DocumentLoader()

    @injector.provider
    @injector.singleton
    def get_text_embedder(self, settings: Settings) -> TextEmbedderPort:
        return TextEmbedder(settings)
