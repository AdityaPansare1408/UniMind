from pathlib import Path

from src.loaders.pdf_loader import PDFLoader
from src.processing.text_splitter import TextChunker


loader = PDFLoader()

documents = loader.load(Path("data/raw/sample.pdf"))

chunker = TextChunker()

chunks = chunker.split(documents)

print(f"Original pages : {len(documents)}")
print(f"Chunks created : {len(chunks)}")

print("\nFirst chunk metadata:")
print(chunks[0].metadata)

print("\nFirst 500 characters:")
print(chunks[0].page_content[:500])