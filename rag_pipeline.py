import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

class RAGPipeline:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Gemini API Key is required")
        
        self.api_key = api_key
        
        # Initialize Gemini LLM and Embeddings using the provided key
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.6-flash",
            temperature=0,
            google_api_key=api_key
        )
        
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=api_key
        )
        
        # Text splitter to break document into manageable chunks
        # Increased chunk size to 10000 to reduce the number of chunks and API calls (Free Tier limits)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=10000,
            chunk_overlap=1000
        )
        
        self.vectorstore = None
        self.retriever = None
        self.qa_chain = None

    def process_document(self, file_path: str, file_name: str) -> None:
        """Loads a document, chunks it, and creates the vector store."""
        # Determine loader based on extension
        if file_name.lower().endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file_name.lower().endswith('.txt'):
            loader = TextLoader(file_path, encoding='utf-8')
        else:
            raise ValueError(f"Unsupported file type: {file_name}")
            
        # Load and split
        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)
        
        # Initialize in-memory Chroma db
        # Note: In a production app you might want to persist the DB
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings
        )
        
        # Create retriever
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )
        
        # Setup the Q&A Chain
        system_prompt = (
            "You are a helpful assistant for document question-answering tasks. "
            "Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, just say that you don't know, don't try to make up an answer. "
            "Keep the answer concise and relevant."
            "\n\n"
            "{context}"
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        self.qa_chain = (
            {"context": self.retriever | format_docs, "input": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def ask_question(self, question: str) -> str:
        """Answers a question based on the loaded document."""
        if not self.qa_chain:
            raise ValueError("Please process a document first.")
            
        response = self.qa_chain.invoke(question)
        return response
