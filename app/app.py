import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.services.document_service import DocumentService
from src.services.rag_service import RAGService

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="UniMind",
    page_icon="🧠",
    layout="wide",
)

rag = RAGService()
document_service = DocumentService()

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

                pdf_path = document_service.save_uploaded_file(uploaded_file)

                chunks = document_service.index_pdf(pdf_path)

            st.success("✅ Document indexed successfully!")

            st.markdown(f"""
**File**

`{uploaded_file.name}`

**Chunks Created**

`{chunks}`
""")

    st.divider()

    st.subheader("Indexed PDFs")

    pdfs = document_service.list_documents()

    if pdfs:

        for pdf in pdfs:

            st.markdown(f"📄 {pdf.name}")

    else:

        st.info("No PDFs indexed yet.")

# --------------------------------------------------
# Question
# --------------------------------------------------

question = st.text_input(
    "Enter your question"
)

if st.button(
    "Ask",
    use_container_width=False,
):

    if question.strip():

        with st.spinner("Searching documents..."):

            response = rag.ask(question)

        # ------------------------------------------

        st.subheader("Answer")

        st.markdown(response.answer)

        # ------------------------------------------
        # Sources
        # ------------------------------------------

        st.subheader("📚 Sources Used")

        sources_seen = set()

        for doc in response.documents:

            metadata = doc.metadata or {}

            source = metadata.get("source", "Unknown")

            source = Path(source).name

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

        # ------------------------------------------
        # Debug
        # ------------------------------------------

        with st.expander("🔍 Show Retrieved Chunks (Debug)"):

            st.write(
                f"Chunks Retrieved: {len(response.documents)}"
            )

            for index, doc in enumerate(response.documents, start=1):

                metadata = doc.metadata or {}

                source = Path(
                    metadata.get("source", "Unknown")
                ).name

                page = metadata.get("page")

                if page is not None:
                    page += 1

                st.markdown(
                    f"### Chunk {index}"
                )

                st.markdown(
                    f"**Source:** {source}"
                )

                st.markdown(
                    f"**Page:** {page}"
                )

                st.code(
                    doc.page_content,
                    language="text",
                )