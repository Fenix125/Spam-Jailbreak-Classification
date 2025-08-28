from typing import Dict
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory, BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from app.backend.services.spam_ham_classifier import SpamHamClassifier
from app.backend.services.bio_rag import BioSearch
from app.backend.settings.config import settings
from app.backend.services.llm import build_llm
from app.backend.agent.prompts import SYSTEM_PROMPT
from app.backend.agent.tools import make_bio_tool, make_classify_tool
from app.backend.agent.tools_https import make_bio_tool_https, make_classify_tool_https


HISTORY_STORE: Dict[str, BaseChatMessageHistory] = {}

def get_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in HISTORY_STORE:
        HISTORY_STORE[session_id] = InMemoryChatMessageHistory()
    return HISTORY_STORE[session_id]


def build_agent(debug: bool = False) -> RunnableWithMessageHistory:
    if settings.run_mode == "cli":
        classifier = SpamHamClassifier(settings.classifier_model)
        bio_search = BioSearch(
            file_path=settings.file_path,
            embed_model_path=settings.embed_model,
            open_api_key=settings.openai_api_key
        )
        tools = [make_classify_tool(classifier), make_bio_tool(bio_search)]
    else:
        tools = [make_classify_tool_https(settings.backend_adress), make_bio_tool_https(settings.backend_adress)]
 
    llm = build_llm(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )
    agent = create_tool_calling_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=debug,
        return_intermediate_steps=True,
    )
    agent_executor_history = RunnableWithMessageHistory(
        agent_executor,
        get_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="output"
    )

    return agent_executor_history
