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

    # --------------------------------------------------
    # Add Documents
    # --------------------------------------------------

    def add_documents(
        self,
        documents: list[Document],
    ) -> None:

        self.vectorstore.add_documents(documents)

    # --------------------------------------------------
    # Similarity Search
    # --------------------------------------------------

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        document_id: str | None = None,
    ) -> list[Document]:
        """
        Retrieve relevant document chunks.

        If document_id is provided,
        search only inside that document.
        """

        if document_id:

            return self.vectorstore.similarity_search(
                query=query,
                k=k,
                filter={
                    "document_id": document_id,
                },
            )

        return self.vectorstore.similarity_search(
            query=query,
            k=k,
        )

    # --------------------------------------------------
    # Delete Document
    # --------------------------------------------------

    def delete_document(
        self,
        document_id: str,
    ) -> None:

        self.vectorstore._collection.delete(
            where={
                "document_id": document_id,
            }
        )

    # --------------------------------------------------
    # Reset Database
    # --------------------------------------------------

    def reset(self) -> None:

        self.vectorstore.delete_collection()

        embedding_model = LocalEmbeddings().get_model()

        self.vectorstore = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=embedding_model,
        )