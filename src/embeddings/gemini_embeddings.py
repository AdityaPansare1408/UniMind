from langchain_google_genai import GoogleGenerativeAIEmbeddings

from src.config.settings import GOOGLE_API_KEY


class GeminiEmbeddings:
    """
    Initializes and returns the Gemini embedding model.
    """

    def __init__(self):
        self.embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=GOOGLE_API_KEY,
        )

    def get_embedding_model(self):
        """
        Returns the initialized embedding model.
        """
        return self.embedding_model