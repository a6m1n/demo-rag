import injector

from app.core.infrastructure.milvus.milvus_connection_provider import (
    MilvusConnectionProvider,
)
from app.core.infrastructure.psql.psq_connection_provider import PSQLConnectionProvider
from app.core.ports import DbConnectionPort
from app.core.settings import Settings, DatabaseType


class CoreModule(injector.Module):
    @injector.provider
    @injector.singleton
    def get_db_connection_provider(self, settings: Settings) -> DbConnectionPort:
        if settings.DB_TYPE == DatabaseType.MILVUS:
            return MilvusConnectionProvider(settings)
        elif settings.DB_TYPE == DatabaseType.POSTGRES:
            return PSQLConnectionProvider(settings)
        else:
            raise Exception("Unknown database type")
