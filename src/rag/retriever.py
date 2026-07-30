from src.vectorstore.chroma_store import ChromaVectorStore


class Retriever:
    """
    Retrieves the most relevant document chunks from ChromaDB.
    """

    def __init__(self):
        self.vectorstore = ChromaVectorStore()

    def retrieve(self, query: str, k: int = 4):
        """
        Retrieve top-k relevant chunks.

        Args:
            query: User question
            k: Number of chunks

        Returns:
            List of LangChain Documents
        """
        return self.vectorstore.similarity_search(query, k=k)