from langchain_chroma import Chroma
from langchain_core.documents import Document

from src.config.settings import CHROMA_DB_PATH
from src.embeddings.local_embeddings import LocalEmbeddings


class ChromaVectorStore:
    """
    Wrapper around ChromaDB.

    Handles:
    - storing document embeddings
    - similarity search
    - deleting document embeddings
    - resetting the database
    """

    def __init__(
        self,
        persist_directory: str = CHROMA_DB_PATH,
    ):

        embedding_model = LocalEmbeddings().get_model()

        self.vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding_model,
        )

    def add_documents(
        self,
        documents: list[Document],
    ) -> None:
        """
        Add documents to the vector database.
        """

        self.vectorstore.add_documents(documents)

    def similarity_search(
        self,
        query: str,
        k: int = 4,
    ) -> list[Document]:
        """
        Retrieve the most relevant document chunks.
        """

        return self.vectorstore.similarity_search(
            query=query,
            k=k,
        )

    def delete_document(
        self,
        document_id: str,
    ) -> None:
        """
        Delete every chunk belonging to a document.
        """

        self.vectorstore._collection.delete(
            where={
                "document_id": document_id,
            }
        )

    def reset(self) -> None:
        """
        Delete the entire Chroma collection.
        Useful during testing.
        """

        self.vectorstore.delete_collection()

        embedding_model = LocalEmbeddings().get_model()

        self.vectorstore = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=embedding_model,
        )