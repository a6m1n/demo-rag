from abc import abstractmethod
from typing import runtime_checkable, Protocol, List, Union

import numpy as np


@runtime_checkable
class MilvusConnectionPort(Protocol):
    @abstractmethod
    def close(self):
        ...

    @abstractmethod
    def insert_embedding(self, embed_data, filename):
        ...

    @abstractmethod
    def search_data(
        self,
        query_vectors: np.ndarray,
        limit: int = 2,
        output_fields: Union[List, None] = None,
        filename: str = None,
    ):
        ...
