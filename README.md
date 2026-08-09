# 🤖 Document Q&A Bot (RAG)

A Retrieval-Augmented Generation (RAG) powered chatbot that lets you upload documents and ask questions about their content. Built with Streamlit, LangChain, and Google Gemini.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.61+-red?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1.3+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## How It Works

```
📄 Upload Document → ✂️ Chunk Text → 🧮 Generate Embeddings → 💾 Store in Vector DB → 🔍 Retrieve + 🤖 Generate Answer
```

1. **Upload** a PDF or TXT document.
2. **Chunking** — The document is split into smaller pieces using `RecursiveCharacterTextSplitter`.
3. **Embeddings** — Each chunk is converted into a vector using Google's `gemini-embedding-001` model.
4. **Vector Store** — Vectors are stored in an in-memory ChromaDB instance for fast similarity search.
5. **Retrieve + Generate** — When you ask a question, the most relevant chunks are retrieved and fed to `gemini-3.6-flash` to generate an accurate, context-grounded answer.

## Tech Stack

| Component          | Technology                     |
|--------------------|--------------------------------|
| Frontend / UI      | Streamlit                      |
| RAG Orchestration  | LangChain (LCEL)               |
| LLM                | Google Gemini 3.6 Flash        |
| Embeddings         | Google Gemini Embedding 001    |
| Vector Database    | ChromaDB (in-memory)           |
| Document Parsing   | PyPDF                          |

## Getting Started

### Prerequisites
- Python 3.11+
- A [Google AI Studio](https://aistudio.google.com/) API Key

### Installation

```bash
# Clone the repository
git clone https://github.com/reevchris100/document-qa-bot.git
cd document-qa-bot

# Create and activate virtual environment
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running Locally

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

### Usage
1. Paste your **Gemini API Key** in the sidebar.
2. Upload a `.pdf` or `.txt` file.
3. Click **Process Document** and wait for it to finish.
4. Ask questions in the chat box!

## Project Structure

```
├── app.py              # Streamlit frontend UI
├── rag_pipeline.py     # RAG backend (loading, chunking, embedding, retrieval)
├── requirements.txt    # Python dependencies
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml      # GitHub Actions CI pipeline
└── README.md
```

## License

This project is licensed under the MIT License.
