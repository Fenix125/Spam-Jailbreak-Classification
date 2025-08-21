import httpx

from pydantic import BaseModel, Field
from langchain.tools import tool


class ClassifyArgs(BaseModel):
    text: str = Field(description="Text needed for spam/ham classification")

class SearchInfoArgs(BaseModel):
    query: str = Field(description="Customized query consisting of keywords from the info question about Mykhailo Ivasiuk")


def make_classify_tool_https(base_url):
    @tool("classify_spam_ham", args_schema=ClassifyArgs) 
    def classify_spam_ham(text: str) -> str:
        """
        Classifies the given message as "spam" or "ham".
        """
        r = httpx.post(f"{base_url}/spam_ham_classifier", params={"text": text})
        r.raise_for_status()
        return r.json()

    return classify_spam_ham

def make_bio_tool_https(base_url):
    @tool("search_info_about_Mykhailo_Ivasiuk", args_schema=SearchInfoArgs)
    def search_info(query: str) -> str:
        """
        Searches for the biography of Mykhailo Ivasiuk and returns relevant text.
        Returns empty string if nothing found.
        """
        r = httpx.post(f"{base_url}/bio_search", params={"query": query})
        r.raise_for_status()
        return r.json()
    
    return search_info
