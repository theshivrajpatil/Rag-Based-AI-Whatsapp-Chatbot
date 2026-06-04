---
title: SPPU AI Exam Assistant
emoji: 🎓
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# SPPU AI Exam Assistant

AI-powered exam preparation assistant using:

- Gemini AI
- ChromaDB
- RAG (Retrieval-Augmented Generation)
- Multi-document support
- PDF, PPTX, DOCX, Images

Built for SPPU students.
---
title: ExamForge AI
emoji: 🎓
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# 🎓 ExamForge AI

An AI-powered RAG (Retrieval-Augmented Generation) exam preparation assistant designed for SPPU students.

ExamForge AI allows students to upload PDFs, PPTs, DOCX files, Excel sheets, images, and study materials, then ask questions and receive exam-oriented answers generated using Gemini AI.

---

# ✨ Features

- AI-powered question answering using Gemini
- Retrieval-Augmented Generation (RAG)
- Multi-document support
- PDF, DOCX, PPTX, XLSX support
- Image support (PNG, JPG, JPEG, WEBP)
- ChromaDB vector database
- Follow-up questions and chat history
- PDF answer export
- Exam-oriented 2, 5, and 10 mark answers
- Document deduplication using file hashing
- Persistent knowledge base
- Cross-platform support

---

# 🛠 Tech Stack

- Python 3.10+
- Streamlit
- Google Gemini API
- ChromaDB
- Sentence Transformers
- ReportLab
- PyPDF
- Python DOCX
- Python PPTX
- OpenPyXL

---

# 📂 Project Structure

```text
examforge-ai/
│
├── app.py
├── requirements.txt
├── README.md
│
├── rag/
│   ├── chunker.py
│   ├── document_loader.py
│   ├── embedder.py
│   ├── retriever.py
│   └── generator.py
│
├── uploads/
├── chroma_db/
└── assets/
```

---

# 🔑 Prerequisites

Before running the project:

1. Install Python 3.10 or later.
2. Create a Gemini API Key.
3. Clone this repository.

Gemini API Key:

https://aistudio.google.com

Create a `.env` file:

```env
GOOGLE_API_KEY=your_api_key_here
```

---

# 🚀 Installation (Windows)

## 1. Clone Repository

```cmd
git clone <repository-url>
cd examforge-ai
```

## 2. Create Virtual Environment

```cmd
python -m venv venv
```

## 3. Activate Virtual Environment

```cmd
venv\Scripts\activate
```

## 4. Install Dependencies

```cmd
pip install -r requirements.txt
```

## 5. Run Application

```cmd
streamlit run app.py
```

---

# 🍏 Installation (macOS)

## 1. Clone Repository

```bash
git clone <repository-url>
cd examforge-ai
```

## 2. Create Virtual Environment

```bash
python3 -m venv venv
```

## 3. Activate Virtual Environment

```bash
source venv/bin/activate
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## 5. Run Application

```bash
streamlit run app.py
```

---

# 🐧 Installation (Linux)

## Ubuntu/Debian

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip -y
```

```bash
git clone <repository-url>
cd examforge-ai
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

# 🌐 Access Application

After starting Streamlit:

```text
http://localhost:8501
```

---

# 📄 Supported File Types

| Type | Supported |
|--------|--------|
| PDF | ✅ |
| DOCX | ✅ |
| PPTX | ✅ |
| XLSX | ✅ |
| TXT | ✅ |
| CSV | ✅ |
| JSON | ✅ |
| PNG | ✅ |
| JPG | ✅ |
| JPEG | ✅ |
| WEBP | ✅ |

---

# 🧹 Troubleshooting

## ChromaDB Dimension Error

Delete:

```text
chroma_db/
```

Then re-upload documents.

## Missing Module Error

```bash
pip install -r requirements.txt
```

## Virtual Environment Issues

Delete and recreate:

```bash
rm -rf venv
```

Then reinstall dependencies.

---

# 👨‍💻 Author

Shivraj Patil
📧 theshivrajpatil@gmail.com
Built with ❤️ .