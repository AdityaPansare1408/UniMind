from langchain_huggingface import HuggingFaceEmbeddings


class LocalEmbeddings:
    """
    Singleton wrapper around the HuggingFace embedding model.
    """

    _model = None

    def __init__(self):

        if LocalEmbeddings._model is None:

            print("Loading embedding model...")

            LocalEmbeddings._model = HuggingFaceEmbeddings(
                model_name="BAAI/bge-small-en-v1.5",
                model_kwargs={"device": "cpu"},
                encode_kwargs={
                    "normalize_embeddings": True,
                },
            )

    def embed_query(self, text: str):

        return LocalEmbeddings._model.embed_query(text)

    def embed_documents(self, texts: list[str]):

        return LocalEmbeddings._model.embed_documents(texts)

    def get_model(self):

        return LocalEmbeddings._model