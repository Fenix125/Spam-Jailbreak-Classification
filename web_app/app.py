from fastapi import FastAPI
from web_app.logging_conf import configure_logging
from web_app.agent.builder import build_agent
from web_app.services.spam_ham_classifier import SpamHamClassifier
from web_app.services.bio_rag import BioSearch
from web_app.config import settings

configure_logging()

agent_executor = build_agent()


classifier = SpamHamClassifier(settings.classifier_model)
bio_searcher = BioSearch(
    file_path=settings.file_path,
    embed_model_path=settings.embed_model
)

app = FastAPI()

@app.post("/agent/")
def agent(prompt: str):
    res = agent_executor.invoke({"input": prompt})

    return res["output"]

@app.post("/spam_ham_classifier")
def spam_ham_classifier(text: str):
    return classifier.classify(text)


@app.post("/bio_search")
def bio_search(query: str):
    return bio_searcher.search(query)

