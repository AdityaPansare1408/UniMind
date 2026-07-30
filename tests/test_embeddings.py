from src.embeddings.gemini_embeddings import GeminiEmbeddings

embedding_model = GeminiEmbeddings().get_embedding_model()

vector = embedding_model.embed_query(
    "Hello, this is my first embedding test."
)

print(f"Embedding generated successfully!")
print(f"Vector dimensions: {len(vector)}")
print(f"First 10 values:\n{vector[:10]}")