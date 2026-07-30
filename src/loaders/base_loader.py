from abc import ABC, abstractmethod
from pathlib import Path
from langchain_core.documents import Document


class BaseLoader(ABC):
    """
    Abstract base class for all document loaders.

    Every loader must implement the load() method and return
    a list of LangChain Document objects.
    """

    @abstractmethod
    def load(self, file_path: Path) -> list[Document]:
        """
        Load a document and return its contents.

        Args:
            file_path (Path): Path to the document.

        Returns:
            list[Document]: List of LangChain Document objects.
        """
        pass