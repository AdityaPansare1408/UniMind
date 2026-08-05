from dataclasses import dataclass


@dataclass
class DocumentInfo:
    """
    Stores metadata about an indexed document.
    """

    document_id: str
    filename: str
    upload_time: str
    chunk_count: int