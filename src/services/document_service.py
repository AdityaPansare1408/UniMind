from pathlib import Path

from src.loaders.pdf_loader import PDFLoader
from src.processing.text_splitter import TextChunker
from src.vectorstore.chroma_store import ChromaVectorStore


class DocumentService:
    """
    Handles document upload, indexing, and listing.
    """

    def __init__(self):

        self.raw_dir = Path("data/raw")
        self.raw_dir.mkdir(parents=True, exist_ok=True)

        self.loader = PDFLoader()
        self.chunker = TextChunker()
        self.vectorstore = ChromaVectorStore()

    def save_uploaded_file(self, uploaded_file):
        """
        Save an uploaded PDF into data/raw.
        """

        file_path = self.raw_dir / uploaded_file.name

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        return file_path

    def index_pdf(self, pdf_path):
        """
        Load, split, and index a PDF.
        """

        documents = self.loader.load(pdf_path)

        chunks = self.chunker.split(documents)

        self.vectorstore.add_documents(chunks)

        return len(chunks)

    def list_documents(self):
        """
        Return all uploaded PDFs.
        """

        return sorted(self.raw_dir.glob("*.pdf"))