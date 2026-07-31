from dataclasses import dataclass

from langchain_core.documents import Document


@dataclass
class RAGResponse:
    """
    Represents the response returned by the RAG pipeline.
    """

    answer: str
    documents: list[Document]