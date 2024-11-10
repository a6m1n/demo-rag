from abc import ABC, abstractmethod


class DocumentLoaderBase(ABC):
    @abstractmethod
    def load(self, path_or_text: str):
        pass


# TODO: Add more loaders
class PdfLoader(DocumentLoaderBase):
    def load(self, path_or_text: str):
        ...
