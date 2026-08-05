import json
from dataclasses import asdict
from pathlib import Path

from src.models.document_info import DocumentInfo


class DocumentRegistry:
    """
    Stores information about indexed documents in a JSON file.
    """

    def __init__(self):

        self.registry_path = Path("data/document_registry.json")

        if not self.registry_path.exists():
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            self._save([])

    # --------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------

    def _load(self) -> list[DocumentInfo]:

        with open(self.registry_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return [DocumentInfo(**item) for item in data]

    def _save(
        self,
        documents: list[DocumentInfo],
    ) -> None:

        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(
                [asdict(doc) for doc in documents],
                f,
                indent=4,
            )

    # --------------------------------------------------
    # Public Methods
    # --------------------------------------------------

    def get_all(self) -> list[DocumentInfo]:
        """
        Return all registered documents.
        """

        return self._load()

    def add(
        self,
        document: DocumentInfo,
    ) -> None:
        """
        Add a new document.
        """

        documents = self._load()
        documents.append(document)
        self._save(documents)

    def get_by_id(
        self,
        document_id: str,
    ) -> DocumentInfo | None:
        """
        Find a document using its document ID.
        """

        for document in self._load():

            if document.document_id == document_id:
                return document

        return None

    def get_by_filename(
        self,
        filename: str,
    ) -> DocumentInfo | None:
        """
        Find a document using its filename.
        """

        for document in self._load():

            if document.filename == filename:
                return document

        return None

    def delete(
        self,
        document_id: str,
    ) -> bool:
        """
        Delete a document from the registry.

        Returns
        -------
        True
            Document deleted successfully.

        False
            Document not found.
        """

        documents = self._load()

        updated_documents = [
            document
            for document in documents
            if document.document_id != document_id
        ]

        if len(updated_documents) == len(documents):
            return False

        self._save(updated_documents)

        return True