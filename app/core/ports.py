from abc import abstractmethod
from typing import runtime_checkable, Protocol


@runtime_checkable
class MilvusConnectionPort(Protocol):
    @abstractmethod
    def connect(self):
        ...

    @abstractmethod
    def close(self):
        ...
