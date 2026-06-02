# ExamForge AI

### AI-Powered RAG Exam Assistant for Students

ExamForge AI is a Retrieval-Augmented Generation (RAG) based exam preparation assistant designed to help students generate accurate, exam-oriented answers directly from their study materials.

The application allows users to upload PDFs, notes, presentations, documents, and images, then ask questions in natural language. The system retrieves relevant content from the uploaded knowledge base and generates structured answers tailored for academic examinations.

---

## Features

### Document-Aware Question Answering
- Upload study materials and receive context-aware answers.
- Answers are grounded in uploaded documents using RAG.

### Multiple Answer Formats
- 2 Marks
- 5 Marks
- 10 Marks
- Important Questions

### Multi-Format Document Support
Supported formats:
- PDF
- TXT
- Markdown
- CSV
- JSON
- DOCX
- PPTX
- XLSX
- PNG
- JPG
- WEBP

### PDF Export
Export generated answers into PDF format for revision and offline study.

### Conversation Memory
Maintains chat history for follow-up questions and improved context.

### Professional UI
Modern AI chatbot interface built with Streamlit.

---

## Tech Stack

### Frontend
- Streamlit
- HTML
- CSS

### AI & RAG
- Google Gemini
- ChromaDB
- Vector Embeddings
- Retrieval-Augmented Generation (RAG)

### Backend
- Python

---

## Project Architecture

```text
User Query
     ↓
Document Retrieval
     ↓
Vector Search (ChromaDB)
     ↓
Relevant Context Extraction
     ↓
Google Gemini
     ↓
Exam-Oriented Answer
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/examforge-ai.git
cd examforge-ai
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

macOS / Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create .env File

```env
GOOGLE_API_KEY=YOUR_API_KEY
```

### Run Application

```bash
streamlit run app.py
```

---

## Future Enhancements

- Google Login
- Cloud Storage Integration
- Multi-User Support
- Mobile Responsive Layout
- Voice-Based Queries
- Personalized Study Recommendations

---

## Author

**Shivraj Patil**

📧 theshivrajpatil@gmail.com

Built with ❤️ for students preparing for academic examinations.

---

## License

MIT License
