from typing import List, Union

import numpy as np
from injector import Inject
from pymilvus import MilvusClient, FieldSchema, CollectionSchema, DataType

from app.core.ports import MilvusConnectionPort
from app.core.settings import Settings


class MilvusConnectionProvider(MilvusConnectionPort):
    collection_name = "document_embeddings"
    client = None

    def __init__(
        self,
        settings: Inject[Settings],
    ):
        self.uri = settings.MILVUS_URL
        self._initialize_client()


    def _create_index(self):
        """
        Create index if not exists
        """
        index_params = MilvusClient.prepare_index_params()

        field_names = ["embedding"]

        for field_name in field_names:
            index_name = f"{field_name}_index"

            if index_name not in self.client.list_indexes(self.collection_name):
                index_params.add_index(
                    metric_type="L2",
                    index_type="IVF_FLAT",
                    params={"nlist": 1024},
                    field_name=field_name,
                    index_name=index_name,
                )

        if len(index_params._indexes) > 0:
            self.client.create_index(
                collection_name=self.collection_name, index_params=index_params
            )

    def _initialize_client(self):
        self.client = MilvusClient(uri=self.uri)

        # for dev only
        # self.client.drop_collection(collection_name=self.collection_name)

        self._initialize_collection()
        self._create_index()
        self.client.load_collection(collection_name=self.collection_name)

    def _initialize_collection(self):
        """
        Creates a collection in Milvus if it does not already exist.
        """
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
            FieldSchema(name="page_content", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="page_number", dtype=DataType.INT64),
            FieldSchema(name="filename", dtype=DataType.VARCHAR, max_length=255),
        ]

        schema = CollectionSchema(fields=fields, description="Document embeddings")

        if self.collection_name not in self.client.list_collections():
            self.client.create_collection(
                collection_name=self.collection_name,
                schema=schema,
                dimension=384,
            )

    def close(self):
        if self.client:
            self.client = None

    def insert_embedding(self, embed_data, filename):
        """Insert data to db"""
        data = [
            {
                "embedding": embed_obj["embeddings"],
                "page_content": embed_obj["page_content"],
                "filename": filename,
                "page_number": embed_obj["page_number"],
            }
            for embed_obj in embed_data
        ]

        return self.client.insert(data=data, collection_name=self.collection_name)

    def search_data(
        self,
        query_vectors: np.ndarray,
        limit: int = 2,
        output_fields: Union[List, None] = None,
        filename: str = None,
    ):
        """Search data by embedding"""
        if output_fields is None:
            output_fields = ["page_content", "filename", "page_number"]

        _filter = None
        if filename:
            _filter = f"filename == '{filename}'"

        return self.client.search(
            collection_name=self.collection_name,
            data=[query_vectors],
            limit=limit,
            filter=_filter,
            output_fields=output_fields,
        )
