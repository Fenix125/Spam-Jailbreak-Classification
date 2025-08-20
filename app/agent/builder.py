from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.services.spam_ham_classifier import SpamHamClassifier
from app.services.bio_rag import BioSearch
from app.config import settings
from app.services.llm import build_llm
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tools import make_bio_tool, make_classify_tool
from app.agent.tools_https import make_bio_tool_https, make_classify_tool_https

def build_agent(debug: bool = False) -> AgentExecutor:
    if settings.run_mode == "cli":
        classifier = SpamHamClassifier(settings.classifier_model)
        bio_search = BioSearch(
            file_path=settings.file_path,
            embed_model_path=settings.embed_model,
            open_api_key=settings.openai_api_key
        )
        tools = [make_classify_tool(classifier), make_bio_tool(bio_search)]
    else:
        tools = [make_classify_tool_https(settings.base_url), make_bio_tool_https(settings.base_url)]
 
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

    memory = ConversationBufferWindowMemory(
        k=20,
        memory_key="chat_history",
        output_key="output",
        return_messages=True
    )

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=debug,
        memory_key="chat_history",
        return_intermediate_steps=True,
    )
    return agent_executor