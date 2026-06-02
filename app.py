import streamlit as st
import hashlib
from pathlib import Path
from io import BytesIO
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

from rag.chunker import chunk_text

from rag.document_loader import load_document

from rag.embedder import get_embeddings

from rag.retriever import (
    store_chunks,
    retrieve,
    document_exists,
    collection
)

from rag.generator import generate_answer

def create_pdf(text):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    body_style = styles["BodyText"]

    content = [
        Paragraph("SPPU AI Exam Assistant", title_style),
        Spacer(1, 12)
    ]

    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        line = (
            line.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        content.append(
            Paragraph(line, body_style)
        )

        content.append(
            Spacer(1, 4)
        )

    doc.build(content)

    buffer.seek(0)

    return buffer

def get_documents():

    try:

        results = collection.get()

        if not results.get("metadatas"):
            return []

        docs = list(
            set(
                metadata["file_name"]
                for metadata in results["metadatas"]
                if metadata and "file_name" in metadata
            )
        )

        return sorted(docs)

    except Exception:

        return []


with st.sidebar:

    st.markdown(
        """
        <div style='display:flex;align-items:center;gap:10px;margin-bottom:12px;'>
            <div style='width:42px;height:42px;background:#2563eb;
            clip-path:polygon(25% 6%,75% 6%,100% 50%,75% 94%,25% 94%,0% 50%);
            display:flex;align-items:center;justify-content:center;
            color:white;font-weight:800;font-size:16px;'>EF</div>
            <div style='font-size:20px;font-weight:700;'>ExamForge AI</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Uploaded Documents")

    documents = get_documents()

    if documents:

        for doc in documents:
            st.caption(f"• {doc}")

        st.divider()
        st.markdown("#### Chat Controls")

        if st.button("New Chat"):
            st.session_state.chat_history = []
            st.rerun()

        if st.button("Refresh"):
            st.rerun()

        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

        st.divider()
        st.markdown(
            "<p style='margin-bottom:0px;'>Created by Shivraj Patil with 💛</p>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='margin-top:0px;'><a href='mailto:theshivrajpatil@gmail.com' style='color:#60a5fa;text-decoration:none;'>📧 theshivrajpatil@gmail.com</a></p>",
            unsafe_allow_html=True
        )

    else:
        st.info("No documents stored yet.")

col1, col2 = st.columns([1, 10])

with col1:
    st.markdown(
        """
        <div style='width:60px;height:60px;background:#2563eb;
        clip-path:polygon(25% 6%,75% 6%,100% 50%,75% 94%,25% 94%,0% 50%);
        display:flex;align-items:center;justify-content:center;
        color:white;font-weight:800;font-size:22px;margin-top:10px;'>EF</div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown("# ExamForge AI")
    st.markdown("### SPPU AI Exam Assistant")



css_file = Path("assets/styles.css")

if css_file.exists():
    st.markdown(
        f"<style>{css_file.read_text()}</style>",
        unsafe_allow_html=True
    )

if "documents_processed" not in st.session_state:
    st.session_state.documents_processed = False

if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_files = st.file_uploader(
    "Upload Documents",
    type=["pdf", "txt", "md", "csv", "json", "docx", "pptx", "xlsx", "png", "jpg", "jpeg", "webp"],
    accept_multiple_files=True
)

if uploaded_files and not st.session_state.documents_processed:

    total_chunks = 0

    for uploaded_file in uploaded_files:

        file_bytes = uploaded_file.getvalue()
        file_hash = hashlib.sha256(file_bytes).hexdigest()

        if document_exists(file_hash):
            st.info(f"{uploaded_file.name} already exists in database.")
            continue

        text = load_document(uploaded_file)

        chunks = chunk_text(text)

        embeddings = get_embeddings(chunks)

        store_chunks(
            chunks,
            embeddings,
            file_hash,
            uploaded_file.name
        )

        total_chunks += len(chunks)

    st.session_state.documents_processed = True

    st.success(
        f"Processed {len(uploaded_files)} files and {total_chunks} chunks successfully!"
    )

st.markdown("### Response Type")

answer_type = st.radio(
    "Response Type",
    [
        "2 Marks",
        "5 Marks",
        "10 Marks",
        "Important Questions"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

if not st.session_state.chat_history:

    st.markdown(
        "Get accurate, document-aware answers from your notes, PDFs, and study materials."
    )

st.divider()

question = st.chat_input(
    "Ask the question"
)

if question:

    query_embedding = get_embeddings(
        [question]
    )[0]

    docs, sources = retrieve(query_embedding)

    flattened_docs = []

    for doc in docs:
        if isinstance(doc, list):
            flattened_docs.extend(doc)
        else:
            flattened_docs.append(doc)

    context = "\n".join(
        str(doc)
        for doc in flattened_docs
    )

    if st.session_state.chat_history:

        recent_chats = st.session_state.chat_history[-3:]

        conversation_context = "\n\n".join(
            [
                f"User: {chat['question']}\nAssistant: {chat['answer']}"
                for chat in recent_chats
            ]
        )

        context = (
            f"Previous Conversation:\n{conversation_context}\n\n"
            f"Retrieved Context:\n{context}"
        )

    with st.spinner(
        "Thinking and searching documents..."
    ):

        answer = generate_answer(
            question,
            context,
            answer_type
        )

    st.session_state.chat_history.append(
        {
            "question": question,
            "answer": answer
        }
    )

if st.session_state.chat_history:

    st.subheader("Conversation")

    for chat in st.session_state.chat_history:

        with st.chat_message("user"):
            st.markdown(chat["question"])

        with st.chat_message("assistant"):
            st.markdown(chat["answer"])

            pdf_buffer = create_pdf(chat["answer"])

            st.download_button(
                "📄 Export PDF",
                pdf_buffer,
                file_name="sppu_ai_answer.pdf",
                mime="application/pdf",
                key=f"pdf_{hash(chat['question'])}"
            )

            with st.expander("View Sources"):
                st.caption("Answer generated from uploaded knowledge base documents.")