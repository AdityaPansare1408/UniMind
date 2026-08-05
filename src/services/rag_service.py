from langchain_core.documents import Document

from src.llm.gemini_llm import GeminiLLM
from src.models.rag_response import RAGResponse
from src.prompts.rag_prompt import RAG_PROMPT
from src.rag.retriever import Retriever


class RAGService:
    """
    Handles the complete Retrieval-Augmented Generation (RAG) pipeline.
    """

    def __init__(self):
        self.llm = GeminiLLM()
        self.retriever = Retriever()

    # --------------------------------------------------
    # Build Context
    # --------------------------------------------------

    def build_context(
        self,
        documents: list[Document],
    ) -> str:

        context_parts = []

        for index, document in enumerate(
            documents,
            start=1,
        ):

            metadata = document.metadata or {}

            source = metadata.get(
                "source",
                "Unknown",
            )

            source = source.split("\\")[-1].split("/")[-1]

            page = metadata.get("page")

            if page is not None:
                page += 1

            context_parts.append(
                f"""
Document {index}
Source: {source}
Page: {page if page is not None else "Unknown"}

--------------------
{document.page_content}
--------------------
"""
            )

        return "\n".join(context_parts)

    # --------------------------------------------------
    # Prompt
    # --------------------------------------------------

    def build_prompt(
        self,
        question: str,
        context: str,
    ) -> str:

        return RAG_PROMPT.format(
            question=question,
            context=context,
        )

    # --------------------------------------------------
    # Ask
    # --------------------------------------------------

    def ask(
        self,
        question: str,
        document_id: str | None = None,
        k: int = 4,
    ) -> RAGResponse:

        if not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        documents = self.retriever.retrieve(
            query=question,
            k=k,
            document_id=document_id,
        )

        if not documents:

            return RAGResponse(
                answer=(
                    "I couldn't find any relevant information "
                    "in the selected document(s)."
                ),
                documents=[],
            )

        context = self.build_context(
            documents
        )

        prompt = self.build_prompt(
            question=question,
            context=context,
        )

        answer = self.llm.invoke(
            prompt
        )

        return RAGResponse(
            answer=answer,
            documents=documents,
        )