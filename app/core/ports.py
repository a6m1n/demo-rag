from abc import abstractmethod
from typing import runtime_checkable, Protocol, List, Union

import numpy as np


@runtime_checkable
class DbConnectionPort(Protocol):
    collection_name = "document_embeddings"
    client = None

    @abstractmethod
    def close(self): ...

    @abstractmethod
    def insert_embedding(self, *args, **kwargs): ...

    @abstractmethod
    def search_data(self, *args, **kwargs): ...
