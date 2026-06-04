import streamlit as st
import hashlib
from pathlib import Path
from io import BytesIO
import re

st.set_page_config(
    page_title="ExamForge AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

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

css_file = Path("assets/styles.css")

if css_file.exists():
    st.markdown(
        f"<style>{css_file.read_text()}</style>",
        unsafe_allow_html=True
    )

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

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontSize=20,
        leading=24,
        alignment=1,
        textColor=colors.darkblue,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        textColor=colors.darkblue,
        spaceBefore=10,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=11,
        leading=16,
        spaceAfter=6
    )

    content = [
        Paragraph("SPPU AI Exam Assistant - Answer Sheet", title_style),
        Spacer(1, 12)
    ]

    parts = re.split(r"(```(?:mermaid)?[\s\S]*?```)", text)

    for part in parts:

        part = part.strip()

        if not part:
            continue

        if part.startswith("```"):

            diagram_text = part.replace("```mermaid", "")
            diagram_text = diagram_text.replace("```", "")
            diagram_text = diagram_text.strip()

            content.append(
                Paragraph("Diagram / Flowchart", heading_style)
            )

            content.append(
                Preformatted(diagram_text, body_style)
            )

            content.append(
                Spacer(1, 8)
            )

        else:

            lines = part.split("\n")

            for line in lines:

                line = line.strip()

                if not line:
                    continue

                line = (
                    line.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                )
                line = line.replace("**", "")
                line = line.replace("__", "")

                if line.startswith("#"):

                    content.append(
                        Paragraph(
                            line.lstrip("#").strip(),
                            heading_style
                        )
                    )

                elif ":" in line and len(line) < 60:

                    content.append(
                        Paragraph(
                            line.strip(),
                            heading_style
                        )
                    )

                elif line.startswith("* "):

                    content.append(
                        Paragraph(
                            f"• {line[2:]}",
                            body_style
                        )
                    )

                else:

                    content.append(
                        Paragraph(line, body_style)
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

def delete_document(file_name):

    try:

        results = collection.get(
            where={"file_name": file_name}
        )

        ids = results.get("ids", [])

        if ids:
            collection.delete(ids=ids)

        return True

    except Exception as e:

        st.error(f"Failed to delete {file_name}: {e}")

        return False


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

        st.markdown("#### Document Management")

        selected_doc = st.selectbox(
            "Select document to delete",
            options=documents,
            key="selected_doc_delete"
        )

        if st.button(
            "🗑️ Delete Selected Document",
            use_container_width=True
        ):

            if delete_document(selected_doc):

                st.success(f"Deleted {selected_doc}")

                st.session_state.documents_processed = False

                st.rerun()

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


st.markdown("""
<div style="display:flex;align-items:center;gap:18px;margin-top:0;margin-bottom:18px;">

<div style="
width:58px;
height:58px;
background:#2563eb;
clip-path:polygon(25% 6%,75% 6%,100% 50%,75% 94%,25% 94%,0% 50%);
display:flex;
align-items:center;
justify-content:center;
color:white;
font-weight:800;
font-size:22px;">
EF
</div>

<div>
<div style="font-size:42px;font-weight:800;color:white;line-height:1;">
ExamForge AI
</div>

<div style="font-size:18px;color:#cbd5e1;margin-top:6px;">
SPPU AI Exam Assistant
</div>
</div>

</div>
""", unsafe_allow_html=True)



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

if uploaded_files:

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

    for idx, chat in enumerate(st.session_state.chat_history):

        with st.chat_message("user"):

            st.markdown(
                f"""
                <div style="
                    font-size:24px;
                    font-weight:700;
                    color:white;
                    margin-bottom:12px;
                    line-height:1.5;
                ">
                    {chat['question']}
                </div>
                """,
                unsafe_allow_html=True
            )

        with st.chat_message("assistant"):

            cleaned_answer = chat["answer"]
            cleaned_answer = cleaned_answer.replace("```ascii", "```")
            cleaned_answer = cleaned_answer.replace("```text", "```")

            cleaned_answer = re.sub(
                r"\*\*(Definition|Explanation|Characteristics|Applications|Advantages|Disadvantages|Features|Important Points|Conclusion|Process State Transition Diagram|Detailed Components|Types|Working|Architecture):\*\*",
                r"## \1",
                cleaned_answer
            )

            cleaned_answer = cleaned_answer.replace("**", "")

            st.markdown(
                f"""
                <style>
                .answer-container h1 {{
                    font-size: 34px;
                    font-weight: 800;
                    margin-top: 20px;
                    margin-bottom: 14px;
                    color: white;
                }}

                .answer-container h2 {{
                    font-size: 28px;
                    font-weight: 700;
                    margin-top: 18px;
                    margin-bottom: 12px;
                    color: white;
                }}

                .answer-container h3 {{
                    font-size: 22px;
                    font-weight: 700;
                    margin-top: 16px;
                    margin-bottom: 10px;
                    color: white;
                }}

                .answer-container p,
                .answer-container li {{
                    font-size: 17px;
                    line-height: 1.8;
                    color: #f3f4f6;
                }}
                </style>

                <div class="answer-container">
                {cleaned_answer}
                </div>
                """,
                unsafe_allow_html=True
            )

            pdf_buffer = create_pdf(chat["answer"])

            st.download_button(
                "📄 Export PDF",
                pdf_buffer,
                file_name=f"sppu_ai_answer_{idx + 1}.pdf",
                mime="application/pdf",
                key=f"pdf_export_{idx}"
            )

            with st.expander("View Sources"):
                st.caption(
                    "Answer generated from uploaded knowledge base documents."
                )