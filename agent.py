import sys
import os
import torch


from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

from langchain.memory import ConversationBufferWindowMemory

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from pydantic import BaseModel, Field
from dotenv import load_dotenv



use_gpu = torch.cuda.is_available()
device = 0 if use_gpu else -1

load_dotenv()

#print(sys.executable)

open_ai_key = os.getenv("OPEN_AI_KEY")

gen_model_path = "gpt-4o-mini"
llm = ChatOpenAI(
    model=gen_model_path,
    temperature=0.2,
    api_key=open_ai_key
)


classifier_path = "bert-spam-ham-classifier-full_dataset/checkpoint-13086"
cls_model = AutoModelForSequenceClassification.from_pretrained(classifier_path)
cls_tokenizer = AutoTokenizer.from_pretrained(classifier_path)

clf = pipeline("text-classification", 
               model=cls_model, 
               tokenizer=cls_tokenizer,
               device=device
              )


class ClassifyArgs(BaseModel):
    text: str = Field(description="text needed for classification")

@tool("classify_spam_ham", args_schema=ClassifyArgs)
def classify_spam_ham(text: str) -> str:
    """
    This tool classifies the given message as spam or ham.
    """
    pred = clf(text)[0]["label"]
    return "spam" if pred == "LABEL_1" else "ham"


Settings.embed_model = HuggingFaceEmbedding("sentence-transformers/all-MiniLM-L6-v2")
Settings.node_parser = SentenceSplitter(chunk_size=300, chunk_overlap=40)
file_path = "student_bio.txt"

docs = SimpleDirectoryReader(input_files=[file_path]).load_data()
index = VectorStoreIndex.from_documents(docs)
retriever = index.as_retriever(similarity_top_k=5)

class SearchInfoArgs(BaseModel):
    query: str = Field(description="a query of user for looking down the information about Mykhailo")

@tool("search_info_about_Mykhailo_Ivasiuk", args_schema=SearchInfoArgs)
def search_info(query: str) -> str:
    """
    This tool searches for the biography of Mykhailo Ivasiuk and returns relevant information.
    Returns concatenated text of all matching documents, or an empty string if no results found.
    """
    nodes = retriever.retrieve(query)
    if not nodes:
        return "No information found."
    context = "\n\n".join(n.node.get_content() for n in nodes)
    return context


tools = [classify_spam_ham, search_info]


system = """
You are a helpful terminal assistant.

RULES:
- Call the "classify_spam_ham" tool if the user EXPLICITLY asks to classify spam or ham,
    OR they use trigger phrases like: "classify", "is this spam", "spam or ham",
    "label this", "check for spam", or the input starts with "Classify this:" or "Classify:".
    When you do call this tool, after it returns, output EXACTLY the tool's result
    in lowercase ("spam" or "ham"), with some extra words saying its a spam or ham
- If the user asks anything related to Mykhailo Ivasiuk's biography, for example queries like:
    "Who is Mykhailo Ivasiuk?", "Tell me about Mykhailo Ivasiuk", "What does Mykhailo study?",
    call the "search_info_about_Mykhailo_Ivasiuk" tool to with the given query to fetch his biography details,
    process them to look more natural and human, and return the result.
- If the user sends a greeting or small talk (e.g., "hello", "hi"), DO NOT call any tool.
- If a user asks a general question that doesn't match either tool, provide a neutral response.
"""



prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    MessagesPlaceholder("chat_history"),      
    ("human", "{input}"),                     
    MessagesPlaceholder("agent_scratchpad"),
])

memory = ConversationBufferWindowMemory(
    k=20,
    return_messages=True,
    memory_key="chat_history",
    output_key="output"
)


def get_agent(debug):
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_exec = AgentExecutor(agent=agent, 
                           tools=tools,
                           memory=memory,
                           verbose=debug,
                           memory_key="chat_history",
                           return_intermediate_steps=True)
    return agent_exec

