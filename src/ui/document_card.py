import streamlit as st


def render_document_card(document):
    """
    Render a document card.

    Returns
    -------
    bool
        True only after the user confirms deletion.
    """

    delete_key = f"delete_confirm_{document.document_id}"

    with st.expander(
        f"📄 {document.filename}",
        expanded=False,
    ):

        st.caption(f"🧩 {document.chunk_count} chunks")
        st.caption(f"🕒 {document.upload_time}")

        # -------------------------
        # First Click
        # -------------------------

        if not st.session_state.get(delete_key, False):

            if st.button(
                "🗑 Delete",
                key=f"delete_btn_{document.document_id}",
                use_container_width=True,
            ):
                st.session_state[delete_key] = True
                st.rerun()

        # -------------------------
        # Confirmation
        # -------------------------

        else:

            st.warning(
                "Are you sure you want to delete this document?"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "✅ Yes",
                    key=f"yes_{document.document_id}",
                    use_container_width=True,
                ):
                    del st.session_state[delete_key]
                    return True

            with col2:

                if st.button(
                    "❌ Cancel",
                    key=f"cancel_{document.document_id}",
                    use_container_width=True,
                ):
                    del st.session_state[delete_key]
                    st.rerun()

    return False