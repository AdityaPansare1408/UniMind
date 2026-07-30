from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document

from src.loaders.base_loader import BaseLoader


class PDFLoader(BaseLoader):
    """
    Loads PDF documents and converts each page
    into a LangChain Document.
    """

    def load(self, file_path: Path) -> list[Document]:
        """
        Load a PDF document.

        Args:
            file_path: Path to the PDF file.

        Returns:
            List of LangChain Document objects.
        """

        documents = []

        reader = PdfReader(file_path)

        for page_number, page in enumerate(reader.pages, start=1):

            text = page.extract_text()

            if not text:
                continue

            document = Document(
                page_content=text,
                metadata={
                    "source": file_path.name,
                    "page": page_number,
                    "file_type": "pdf",
                },
            )

            documents.append(document)

        return documents