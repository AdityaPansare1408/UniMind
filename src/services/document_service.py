from pathlib import Path
from datetime import datetime

from src.loaders.document_loader import DocumentLoaderFactory
from src.models.document_info import DocumentInfo
from src.processing.text_splitter import TextChunker
from src.services.document_registry import DocumentRegistry
from src.utils.document_utils import generate_document_id
from src.vectorstore.chroma_store import ChromaVectorStore


class DocumentService:
    """
    Handles document upload, indexing, listing and deletion.
    """

    def __init__(self):

        self.raw_dir = Path("data/raw")
        self.raw_dir.mkdir(parents=True, exist_ok=True)

        self.loader_factory = DocumentLoaderFactory()
        self.chunker = TextChunker()
        self.vectorstore = ChromaVectorStore()
        self.registry = DocumentRegistry()

    # --------------------------------------------------
    # Upload
    # --------------------------------------------------

    def save_uploaded_file(self, uploaded_file):

        file_path = self.raw_dir / uploaded_file.name

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        return file_path

    # --------------------------------------------------
    # Index
    # --------------------------------------------------

    def index_document(self, file_path: Path):

        document_id = generate_document_id()

        loader = self.loader_factory.get_loader(file_path)

        documents = loader.load(file_path)

        for document in documents:
            document.metadata["document_id"] = document_id
            document.metadata["filename"] = file_path.name

        chunks = self.chunker.split(documents)

        self.vectorstore.add_documents(chunks)

        document_info = DocumentInfo(
            document_id=document_id,
            filename=file_path.name,
            upload_time=datetime.now().isoformat(timespec="seconds"),
            chunk_count=len(chunks),
        )

        self.registry.add(document_info)

        return len(chunks)

    # --------------------------------------------------
    # List
    # --------------------------------------------------

    def list_documents(self):

        return self.registry.get_all()

    # --------------------------------------------------
    # Delete
    # --------------------------------------------------

    def delete_document(
        self,
        document_id: str,
    ) -> bool:
        """
        Delete an indexed document completely.
        """

        document = self.registry.get_by_id(document_id)

        if document is None:
            return False

        # Delete embeddings
        self.vectorstore.delete_document(document_id)

        # Delete file
        file_path = self.raw_dir / document.filename

        if file_path.exists():
            file_path.unlink()

        # Delete registry entry
        self.registry.delete(document_id)

        return True