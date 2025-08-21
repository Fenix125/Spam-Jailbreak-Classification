from abc import ABC, abstractmethod

class DocumentSearch(ABC):
    @abstractmethod
    def search(self, query: str) -> str:
        """
        Search for the relevant document based on the query.
        """
        pass