from pathlib import Path
import csv

from langchain_core.documents import Document as LangChainDocument

from src.loaders.base_loader import BaseLoader


class CSVLoader(BaseLoader):
    """
    Loads CSV documents.

    Each row becomes one LangChain Document.
    """

    def load(self, file_path: Path):

        documents = []

        with open(
            file_path,
            newline="",
            encoding="utf-8",
        ) as csv_file:

            reader = csv.DictReader(csv_file)

            for index, row in enumerate(reader, start=1):

                text = "\n".join(
                    f"{key}: {value}"
                    for key, value in row.items()
                )

                documents.append(
                    LangChainDocument(
                        page_content=text,
                        metadata={
                            "source": file_path.name,
                            "page": index,
                            "file_type": "csv",
                        },
                    )
                )

        return documents