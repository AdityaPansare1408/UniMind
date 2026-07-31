from langchain_google_genai import GoogleGenerativeAIEmbeddings

from src.config.settings import (
    GOOGLE_API_KEY,
    GOOGLE_EMBEDDING_MODEL,
)


class GeminiEmbeddings:
    """
    Wrapper around the Gemini embedding model.
    """

    def __init__(self):

        self.model = GoogleGenerativeAIEmbeddings(
            model=GOOGLE_EMBEDDING_MODEL,
            google_api_key=GOOGLE_API_KEY,
        )

    def embed_query(self, text: str):
        """
        Generate an embedding for a single query.
        """
        return self.model.embed_query(text)

    def embed_documents(self, texts: list[str]):
        """
        Generate embeddings for multiple documents.
        """
        return self.model.embed_documents(texts)

    def get_model(self):
        """
        Returns the underlying LangChain embedding model.
        Useful for Chroma and other vector stores.
        """
        return self.model