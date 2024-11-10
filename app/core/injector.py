import injector

from app.core.infrastructure.milvus.milvus_connection_provider import (
    MilvusConnectionProvider,
)
from app.core.ports import MilvusConnectionPort
from app.core.settings import Settings


class CoreModule(injector.Module):
    @injector.provider
    @injector.singleton
    def get_milvus_connection_provider(
        self, settings: Settings
    ) -> MilvusConnectionPort:
        return MilvusConnectionProvider(settings)
