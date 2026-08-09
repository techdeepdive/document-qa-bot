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
4. **Vector Store** — Vectors are stored in an isolated, ephemeral ChromaDB instance (unique per user session) for fast similarity search.
5. **Retrieve + Generate** — When you ask a question, the most relevant chunks are retrieved and fed to `gemini-3.6-flash` to generate an accurate, context-grounded answer.

> **🔒 Session Isolation:** Each user session gets its own ephemeral ChromaDB client with a unique collection name, ensuring complete data isolation between users. No document data is shared or persisted across sessions.

## Tech Stack

| Component          | Technology                     |
|--------------------|--------------------------------|
| Frontend / UI      | Streamlit                      |
| RAG Orchestration  | LangChain (LCEL)               |
| LLM                | Google Gemini 3.6 Flash        |
| Embeddings         | Google Gemini Embedding 001    |
| Vector Database    | ChromaDB (ephemeral, per-session) |
| Document Parsing   | PyPDF                          |

## Getting Started

### Prerequisites
- Python 3.11+
- A [Google AI Studio](https://aistudio.google.com/) API Key

### Installation

```bash
# Clone the repository
git clone https://github.com/techdeepdive/document-qa-bot.git
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
1. Paste your **Gemini API Key** in the sidebar (or configure it via Streamlit secrets — see below).
2. Upload a `.pdf` or `.txt` file.
3. Click **Process Document** and wait for it to finish.
4. Ask questions in the chat box!

## Deployment (Streamlit Community Cloud)

This app is designed to be deployed for free on [Streamlit Community Cloud](https://share.streamlit.io).

1. Push the repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **"New app"** → select your repo, branch `main`, and file `app.py`.
4. Click **Deploy!**

### Configuring Secrets

To avoid entering your API key every time:

1. In your deployed app, click the **⋮ menu** (bottom-right) → **Settings** → **Secrets**.
2. Add the following:
   ```toml
   GEMINI_API_KEY = "your-gemini-api-key-here"
   ```
3. Click **Save**. The app will restart with the key pre-loaded.

For local development, create a `.streamlit/secrets.toml` file in the project root:
```toml
GEMINI_API_KEY = "your-gemini-api-key-here"
```

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
