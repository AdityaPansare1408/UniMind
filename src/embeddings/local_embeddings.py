from langchain_huggingface import HuggingFaceEmbeddings


class LocalEmbeddings:
    """
    Local embedding model using HuggingFace.

    Uses BAAI/bge-small-en-v1.5, which is fast,
    accurate for retrieval, and works completely offline
    after the first download.
    """

    def __init__(self):
        self.model = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    def embed_query(self, text: str):
        return self.model.embed_query(text)

    def embed_documents(self, texts: list[str]):
        return self.model.embed_documents(texts)

    def get_model(self):
        """
        Returns the underlying LangChain embedding model.
        Used by ChromaDB.
        """
        return self.model