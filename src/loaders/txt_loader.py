from pathlib import Path

from langchain_core.documents import Document as LangChainDocument

from src.loaders.base_loader import BaseLoader


class TXTLoader(BaseLoader):
    """
    Loads plain text (.txt) documents.
    """

    def load(self, file_path: Path):
        text = file_path.read_text(encoding="utf-8")

        return [
            LangChainDocument(
                page_content=text,
                metadata={
                    "source": file_path.name,
                    "page": 1,
                },
            )
        ]