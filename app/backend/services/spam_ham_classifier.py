import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from app.backend.base_classes.classifier import Classifier

class SpamHamClassifier(Classifier):
    def __init__(self, model_path: str) -> None:
        self._device = 0 if torch.cuda.is_available() else -1
        self._tokenizer = AutoTokenizer.from_pretrained(model_path)
        self._model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self._pipe = pipeline(
            "text-classification",
            model=self._model,
            tokenizer=self._tokenizer,
            device=self._device
        )
    def classify(self, text: str) -> str:
        return self._pipe(text)[0]["label"]
