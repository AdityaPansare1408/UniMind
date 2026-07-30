from pathlib import Path

from src.loaders.pdf_loader import PDFLoader
from src.processing.text_splitter import TextChunker
from src.vectorstore.chroma_store import ChromaVectorStore


loader = PDFLoader()
documents = loader.load(Path("data/raw/sample.pdf"))

chunker = TextChunker()
chunks = chunker.split(documents)

store = ChromaVectorStore()

store.reset()

store.add_documents(chunks)

print(f"Stored {len(chunks)} chunks.")

results = store.similarity_search(
    "Mechanical Engineering",
    k=3
)

print("\nRetrieved Documents:\n")

for i, doc in enumerate(results, start=1):
    print(f"Result {i}")
    print(doc.page_content[:250])
    print(doc.metadata)
    print("-" * 50)