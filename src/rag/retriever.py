from src.vectorstore.chroma_store import ChromaVectorStore


class Retriever:
    """
    Retrieves the most relevant document chunks from ChromaDB.
    """

    def __init__(self):
        self.vectorstore = ChromaVectorStore()

    def retrieve(
        self,
        query: str,
        k: int = 4,
        document_id: str | None = None,
    ):
        """
        Retrieve top-k relevant chunks.

        Args:
            query: User question
            k: Number of chunks
            document_id: Restrict search to one document

        Returns:
            List of LangChain Documents
        """

        return self.vectorstore.similarity_search(
            query=query,
            k=k,
            document_id=document_id,
        )