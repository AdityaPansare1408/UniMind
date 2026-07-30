from langchain_chroma import Chroma
from src.embeddings.gemini_embeddings import GeminiEmbeddings


class ChromaVectorStore:
    """
    Handles storing and retrieving document embeddings
    using ChromaDB.
    """

    def __init__(self, persist_directory="data/chroma_db"):
        embedding_model = GeminiEmbeddings().get_embedding_model()

        self.vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding_model,
        )

    def add_documents(self, documents):
        self.vectorstore.add_documents(documents)

    def similarity_search(self, query, k=4):
        return self.vectorstore.similarity_search(query, k=k)

    def reset(self):
        """
        Deletes all documents from the vector database.
        Useful during testing.
        """
        self.vectorstore.delete_collection()

        embedding_model = GeminiEmbeddings().get_embedding_model()

        self.vectorstore = Chroma(
            persist_directory="data/chroma_db",
            embedding_function=embedding_model,
        )