from injector import Inject
from pymilvus import MilvusClient

from app.core.ports import MilvusConnectionPort
from app.core.settings import Settings


class MilvusConnectionProvider(MilvusConnectionPort):
    def __init__(
        self,
        settings: Inject[Settings],
    ):
        self.uri = settings.MILVUS_URL
        self.client = None

    def connect(self):
        # TODO: Move to single ton
        print("Connec1ted", self.client)
        if not self.client:
            self.client = MilvusClient(uri=self.uri)
            # Create collection during first connection if connection is not exists
            if "quick_setup" not in self.client.list_collections():
                self.client.create_collection(
                    collection_name="quick_setup", dimension=5
                )
        return self.client

    def close(self):
        if self.client:
            self.client = None
