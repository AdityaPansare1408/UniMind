import uuid


def generate_document_id() -> str:
    """
    Generate a unique identifier for an uploaded document.
    """

    return str(uuid.uuid4())