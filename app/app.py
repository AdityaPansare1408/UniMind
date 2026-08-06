import sys
from pathlib import Path
import time
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.services.document_service import DocumentService
from src.services.document_registry import DocumentRegistry
from src.services.rag_service import RAGService
from src.ui.document_card import render_document_card
from src.memory.conversation_memory import ConversationMemory

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="🧠 UniMind",
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
# Load Documents
# --------------------------------------------------

documents = registry.get_all()

search_options = {
    "All Documents": None,
}

for document in documents:
    search_options[document.filename] = document.document_id

# --------------------------------------------------
# Conversation Memory
# --------------------------------------------------

if "memory" not in st.session_state:
    st.session_state.memory = ConversationMemory()

# --------------------------------------------------
# Chat UI History
# --------------------------------------------------

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# --------------------------------------------------
# Helper Functions
# --------------------------------------------------

def render_sources(documents):
    if not documents:
        return
        
    with st.expander("📚 Sources"):
        shown = set()
        for doc in documents:
            source = Path(doc.get("source", "Unknown")).name
            page = doc.get("page")
                
            key = (source, page)
            if key in shown:
                continue
                
            shown.add(key)
            if page is None:
                st.markdown(f"• **{source}**")
            else:
                st.markdown(f"• **{source}** — Page {page}")

def render_debug(documents):
    if not documents:
        return
        
    with st.expander("🔍 Retrieved Chunks (Debug)"):
        st.markdown(f"**Chunks Retrieved:** `{len(documents)}`")
        st.write("") # Small visual spacer
        
        for index, doc in enumerate(documents, start=1):
            source = Path(doc.get("source", "Unknown")).name
            page = doc.get("page")
                
            if page is None:
                st.markdown(
                    f"**Chunk {index}** | `{source}`"
                )
            else:
                st.markdown(
                    f"**Chunk {index}** | `{source}` (Page {page})"
                )
            
            st.code(doc.get("page_content", ""), language="text")

def render_assistant_message(message):
    with st.chat_message("assistant"):
        st.markdown(message["content"])
        
        # Adding a slight vertical space before expanders for a cleaner look
        if "documents" in message and message["documents"]:
            st.write("") 
            render_sources(message["documents"])
            render_debug(message["documents"])

def render_user_message(message):
    with st.chat_message("user"):
        st.markdown(message["content"])

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    st.header("📄 Documents")

    uploaded_file = st.file_uploader(
        "Upload Document",
        type=["pdf", "docx", "txt", "md", "csv", "pptx"],
    )

    if uploaded_file:
        if st.button("Index Document", use_container_width=True):
            with st.spinner("Indexing document..."):
                file_path = document_service.save_uploaded_file(uploaded_file)
                chunks = document_service.index_document(file_path)

            st.success("✅ Document indexed successfully!")
            st.markdown(f"""
**File**
`{uploaded_file.name}`

**Chunks Created**
`{chunks}`
""")
            time.sleep(1)
            st.rerun()

    st.divider()

    # --------------------------------------------------
    # Indexed Documents
    # --------------------------------------------------
    st.subheader("Indexed Documents")

    if documents:
        for document in documents:
            if render_document_card(document):
                deleted = document_service.delete_document(document.document_id)
                if deleted:
                    st.success(f"✅ '{document.filename}' deleted successfully.")
                    st.rerun()
                else:
                    st.error("Failed to delete the document.")
    else:
        st.info("No documents indexed yet.")

# --------------------------------------------------
# Header
# --------------------------------------------------

# Reduced unnecessary spacing by removing the divider under the header
st.title("🧠 UniMind")
st.caption("Ask questions about your indexed university documents.")

# --------------------------------------------------
# Chat History (Single Renderer)
# --------------------------------------------------

for message in st.session_state.chat_messages:
    if message["role"] == "user":
        render_user_message(message)
    elif message["role"] == "assistant":
        render_assistant_message(message)

# --------------------------------------------------
# Chat Footer Controls
# --------------------------------------------------

# Removed the top divider to let the chat seamlessly transition to the controls
st.write("") 
footer_left, footer_right = st.columns([4, 1])

with footer_left:
    selected_document = st.selectbox(
        "Search Scope",
        options=list(search_options.keys()),
        index=0,
        label_visibility="collapsed",
    )

selected_document_id = search_options[selected_document]

with footer_right:
    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.memory.clear()
        st.session_state.chat_messages.clear()
        st.rerun()

# --------------------------------------------------
# Chat Input & Processing
# --------------------------------------------------

question = st.chat_input("Ask UniMind...")

if question:
    with st.spinner("Searching documents..."):
        # Retrieve answer
        conversation_history = st.session_state.memory.build_history()
        
        response = rag.ask(
            question=question,
            conversation_history=conversation_history,
            document_id=selected_document_id,
        )

    # Convert complex Document objects into lightweight dictionaries 
    # to avoid bloat and serialization issues in Streamlit session_state
    lightweight_docs = []
    if response.documents:
        for doc in response.documents:
            metadata = getattr(doc, 'metadata', {})
            lightweight_docs.append({
                "source": metadata.get("source", "Unknown"),
                "page": metadata.get("page"),
                "page_content": getattr(doc, 'page_content', "")
            })

    # Save to memory
    st.session_state.memory.add_exchange(
        question,
        response.answer,
    )

    # Save to UI history state completely
    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": question,
        }
    )
    
    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": response.answer,
            "documents": lightweight_docs,
        }
    )

    # Trigger a clean, single re-render of the entire conversation
    st.rerun()