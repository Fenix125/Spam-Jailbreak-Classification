from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.backend.logging_conf import configure_logging
from app.backend.agent.builder import build_agent
from app.backend.services.spam_ham_classifier import SpamHamClassifier
from app.backend.services.bio_rag import BioSearch
from app.backend.config import settings

configure_logging()

agent_executor = build_agent()


classifier = SpamHamClassifier(settings.classifier_model)
bio_searcher = BioSearch(
    file_path=settings.file_path,
    embed_model_path=settings.embed_model,
    open_api_key=settings.openai_api_key
)

app = FastAPI()


#origins = [settings.base_url]
origins = ["http://localhost:8001"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/agent")
def agent(prompt: str):
    res = agent_executor.invoke({"input": prompt})
    return res["output"]


@app.post("/spam_ham_classifier")
def spam_ham_classifier(text: str):
    return classifier.classify(text)


@app.post("/bio_search")
def bio_search(query: str):
    return bio_searcher.search(query)
