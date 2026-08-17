import streamlit as st
import os
import tempfile
from rag_pipeline import RAGPipeline

st.set_page_config(page_title="Document Q&A Bot", page_icon="🤖", layout="wide")

st.title("🤖 Document Q&A Bot")
st.markdown("Upload a document and ask questions about its content!")

# Sidebar for configuration and upload
with st.sidebar:
    st.header("Configuration")
    
    api_key = st.text_input("Gemini API Key", type="password", help="Get your API key from Google AI Studio")
    
    st.header("Document Upload")
    uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])
    
    process_btn = st.button("Process Document")

# Initialize session state for chat history and pipeline
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "rag_pipeline" not in st.session_state:
    st.session_state.rag_pipeline = None

# Handle document processing
if process_btn:
    if not api_key:
        st.error("Please enter your Gemini API Key first.")
    elif not uploaded_file:
        st.error("Please upload a document.")
    else:
        with st.spinner("Processing document (this may take a moment)..."):
            try:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                # Initialize and run pipeline
                pipeline = RAGPipeline(api_key=api_key)
                pipeline.process_document(tmp_file_path, uploaded_file.name)
                
                # Store in session state
                st.session_state.rag_pipeline = pipeline
                
                # Clean up temp file
                os.remove(tmp_file_path)
                
                st.success("Document processed successfully! You can now ask questions.")
            except Exception as e:
                st.error(f"Error processing document: {str(e)}")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about your document..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Generate response
    with st.chat_message("assistant"):
        if st.session_state.rag_pipeline is None:
            error_msg = "Please upload and process a document first."
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
        else:
            with st.spinner("Thinking..."):
                try:
                    answer = st.session_state.rag_pipeline.ask_question(prompt)
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    error_msg = f"Error generating answer: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
