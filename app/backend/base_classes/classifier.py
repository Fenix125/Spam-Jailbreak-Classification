from abc import ABC, abstractmethod

class Classifier(ABC):
    @abstractmethod
    def classify(self, text: str) -> str:
        """
        Classify given text
        """
        pass
