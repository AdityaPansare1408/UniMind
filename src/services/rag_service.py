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

    def build_context(
        self,
        documents: list[Document],
    ) -> str:
        """
        Combine retrieved document chunks into a formatted context string.
        """

        context_parts = []

        for index, document in enumerate(documents, start=1):
            context_parts.append(
                f"""Document {index}
--------------------
{document.page_content}
"""
            )

        return "\n\n".join(context_parts)

    def build_prompt(
        self,
        question: str,
        context: str,
    ) -> str:
        """
        Build the final prompt for the language model.
        """

        return RAG_PROMPT.format(
            question=question,
            context=context,
        )

    def ask(
        self,
        question: str,
        k: int = 4,
    ) -> RAGResponse:
        """
        Execute the complete RAG pipeline.
        """

        if not question.strip():
            raise ValueError("Question cannot be empty.")

        documents = self.retriever.retrieve(
            query=question,
            k=k,
        )

        if not documents:
            return RAGResponse(
                answer=(
                    "I couldn't find any relevant information "
                    "in the uploaded documents."
                ),
                documents=[],
            )

        context = self.build_context(documents)

        prompt = self.build_prompt(
            question=question,
            context=context,
        )

        answer = self.llm.invoke(prompt)

        return RAGResponse(
            answer=answer,
            documents=documents,
        )