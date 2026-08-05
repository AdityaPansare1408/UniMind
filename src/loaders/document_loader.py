from pathlib import Path

from src.loaders.csv_loader import CSVLoader
from src.loaders.docx_loader import DOCXLoader
from src.loaders.md_loader import MarkdownLoader
from src.loaders.pdf_loader import PDFLoader
from src.loaders.pptx_loader import PPTXLoader
from src.loaders.txt_loader import TXTLoader


class DocumentLoaderFactory:
    """
    Factory responsible for returning the correct loader
    based on the uploaded document type.
    """

    def __init__(self):

        self.loaders = {
            ".pdf": PDFLoader(),
            ".docx": DOCXLoader(),
            ".txt": TXTLoader(),
            ".md": MarkdownLoader(),
            ".csv": CSVLoader(),
            ".pptx": PPTXLoader(),
        }

    def get_loader(self, file_path: Path):

        extension = file_path.suffix.lower()

        loader = self.loaders.get(extension)

        if loader is None:
            raise ValueError(
                f"Unsupported document type: {extension}"
            )

        return loader