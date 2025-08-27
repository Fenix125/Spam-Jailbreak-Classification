from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import FastMCP
from fastmcp.server.openapi import RouteMap, MCPType
from app.backend.logging_conf import configure_logging
from app.backend.agent.builder import build_agent
from app.backend.services.spam_ham_classifier import SpamHamClassifier
from app.backend.services.bio_rag import BioSearch
from app.backend.config import settings
from app.backend.base_classes.request_models import AgentIn, SpamIn, BioIn
from app.backend.base_classes.response_models import AgentOut, SpamOut, BioOut

configure_logging()

agent_executor = build_agent()


classifier = SpamHamClassifier(settings.classifier_model)
bio_searcher = BioSearch(
    file_path=settings.file_path,
    embed_model_path=settings.embed_model,
    open_api_key=settings.openai_api_key
)

app = FastAPI(title="SpamHamClassifierAPI")

api = APIRouter(prefix="/api")


origins = [settings.frontend_adress]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api.post("/agent", operation_id="call_agent", response_model=AgentOut)
def agent(req: AgentIn):
    res = agent_executor.invoke({"input": req.prompt})
    return AgentOut(output=res["output"])


@api.post("/spam_ham_classifier", 
            operation_id="classify_text",
            summary="Classify text as spam or ham",
            description="Returns 'spam' or 'ham' for the given text.",
            tags=["mcp"],
            response_model=SpamOut)
def spam_ham_classifier(req: SpamIn):
    label = classifier.classify(req.text)
    return SpamOut(label=label)


@api.post("/bio_search",
            operation_id="search_bio",
            summary="Search in Mykhailo Ivasiuk biography corpus",
            description="Returns the top relevant passages for the query.",
            tags=["mcp"],
            response_model=BioOut)
def bio_search(req: BioIn):
    result = bio_searcher.search(req.query)
    return BioOut(result=result)


app.include_router(api)

mcp = FastMCP.from_fastapi(
    app=app,
    name="SpamHamClassifier-MCP",
    route_maps=[
        RouteMap(tags={"mcp"}, mcp_type=MCPType.TOOL),
        RouteMap(mcp_type=MCPType.EXCLUDE),
    ],
)
mcp_app = mcp.http_app(path="/mcp")

app.router.lifespan_context = mcp_app.lifespan

app.mount("/external", mcp_app)
