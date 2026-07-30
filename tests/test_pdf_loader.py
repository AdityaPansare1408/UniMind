from pathlib import Path

from src.loaders.pdf_loader import PDFLoader

loader = PDFLoader()

documents = loader.load(Path("data/raw/sample.pdf"))

print(f"Total pages loaded: {len(documents)}")

print("\nFirst page metadata:")
print(documents[0].metadata)

print("\nFirst 300 characters:")
print(documents[0].page_content[:300])