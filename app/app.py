import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.services.document_service import DocumentService
from src.services.document_registry import DocumentRegistry
from src.services.rag_service import RAGService
from src.ui.document_card import render_document_card

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="UniMind",
    page_icon="🧠",
    layout="wide",
)

@st.cache_resource
def get_rag_service():
    return RAGService()


@st.cache_resource
def get_document_service():
    return DocumentService()


@st.cache_resource
def get_registry():
    return DocumentRegistry()


rag = get_rag_service()
document_service = get_document_service()
registry = get_registry()

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🧠 UniMind")
st.caption("Ask questions about your indexed university documents.")

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("📄 Documents")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
    )

    if uploaded_file:

        if st.button(
            "Index Document",
            use_container_width=True,
        ):

            with st.spinner("Indexing document..."):

                pdf_path = document_service.save_uploaded_file(
                    uploaded_file
                )

                chunks = document_service.index_pdf(
                    pdf_path
                )

            st.success("✅ Document indexed successfully!")

            st.markdown(f"""
**File**

`{uploaded_file.name}`

**Chunks Created**

`{chunks}`
""")

    st.divider()

    # --------------------------------------------------
    # Indexed Documents
    # --------------------------------------------------

    st.subheader("Indexed Documents")

    documents = registry.get_all()

    if documents:

        for document in documents:

            if render_document_card(document):

                deleted = document_service.delete_document(
                    document.document_id
                )

                if deleted:

                    st.success(
                        f"✅ '{document.filename}' deleted successfully."
                    )

                    st.rerun()

                else:

                    st.error(
                        "Failed to delete the document."
                    )

    else:

        st.info("No documents indexed yet.")

# --------------------------------------------------
# Question
# --------------------------------------------------

question = st.text_input(
    "Enter your question"
)

if st.button(
    "Ask",
):

    if question.strip():

        with st.spinner(
            "Searching documents..."
        ):

            response = rag.ask(question)

        # --------------------------------------------------

        st.subheader("Answer")

        st.markdown(response.answer)

        # --------------------------------------------------
        # Sources
        # --------------------------------------------------

        st.subheader("📚 Sources Used")

        sources_seen = set()

        for doc in response.documents:

            metadata = doc.metadata or {}

            source = Path(
                metadata.get(
                    "source",
                    "Unknown",
                )
            ).name

            page = metadata.get("page")

            if page is not None:
                page += 1

            key = (source, page)

            if key in sources_seen:
                continue

            sources_seen.add(key)

            st.markdown(
                f"- **{source}** (Page {page})"
            )

        # --------------------------------------------------
        # Debug
        # --------------------------------------------------

        with st.expander(
            "🔍 Show Retrieved Chunks (Debug)"
        ):

            st.write(
                f"Chunks Retrieved: {len(response.documents)}"
            )

            for index, doc in enumerate(
                response.documents,
                start=1,
            ):

                metadata = doc.metadata or {}

                source = Path(
                    metadata.get(
                        "source",
                        "Unknown",
                    )
                ).name

                page = metadata.get("page")

                if page is not None:
                    page += 1

                st.markdown(
                    f"## Chunk {index}"
                )

                st.markdown(
                    f"**Document ID:** `{metadata.get('document_id', 'N/A')}`"
                )

                st.markdown(
                    f"**Filename:** `{metadata.get('filename', 'N/A')}`"
                )

                st.markdown(
                    f"**Source:** `{source}`"
                )

                st.markdown(
                    f"**Page:** `{page}`"
                )

                st.markdown(
                    f"**Chunk Length:** `{len(doc.page_content)} characters`"
                )

                st.code(
                    doc.page_content,
                    language="text",
                )

                st.divider()