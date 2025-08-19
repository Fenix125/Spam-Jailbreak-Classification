from pydantic import BaseModel, Field
from langchain.tools import tool


from web_app.base_classes.classifier import Classifier
from web_app.base_classes.rag import DocumentSearch


class ClassifyArgs(BaseModel):
    text: str = Field(description="Text needed for spam/ham classification")

class SearchInfoArgs(BaseModel):
    query: str = Field(description="Customized query consisting of keywords from the info question about Mykhailo Ivasiuk")


def make_classify_tool(classifier: Classifier):
    @tool("classify_spam_ham", args_schema=ClassifyArgs) 
    def classify_spam_ham(text: str) -> str:
        """
        Classifies the given message as "spam" or "ham".
        """
        return classifier.classify(text)
    return classify_spam_ham

def make_bio_tool(searcher: DocumentSearch):
    @tool("search_info_about_Mykhailo_Ivasiuk", args_schema=SearchInfoArgs)
    def search_info(query: str) -> str:
        """
        Searches for the biography of Mykhailo Ivasiuk and returns relevant text.
        Returns empty string if nothing found.
        """
        return searcher.search(query)
    return search_info
