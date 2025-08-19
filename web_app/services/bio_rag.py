from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from web_app.base_classes.rag import DocumentSearch

class BioSearch(DocumentSearch):
    def __init__(self, file_path: str, embed_model_path: str, chunk_size: int = 300, chunk_overlap: int = 40, top_k: int = 5) -> None:
        Settings.embed_model = HuggingFaceEmbedding(embed_model_path)
        Settings.node_parser = SentenceSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        self._docs = SimpleDirectoryReader(input_files=[file_path]).load_data()
        self._index = VectorStoreIndex.from_documents(self._docs)
        self._retriever = self._index.as_retriever(similarity_top_k=top_k)

    def search(self, query: str) -> str:
        nodes = self._retriever.retrieve(query)
        if not nodes:
            return "No information found"
        return "\n\n".join(n.node.get_content() for n in nodes)
 