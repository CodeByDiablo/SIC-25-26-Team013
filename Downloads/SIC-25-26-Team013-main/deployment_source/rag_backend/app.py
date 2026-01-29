# SIC Team 013 - AI Research Agent (RAG Backend)
# Framework: LangChain + Hugging Face Embeddings

import os
import gradio as gr
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import HuggingFaceHub
from langchain.chains import RetrievalQA

# 1. SETUP & CONFIGURATION
# Note: You would set these in your deployment environment variables
HF_TOKEN = os.environ.get("HF_TOKEN") 
MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
LLM_REPO = "google/flan-t5-large" # Faster for CPU-only spaces

print("🤖 Initializing AI Research Agent...")

# 2. GLOBAL STATE (In-Memory Vector Store)
vector_store = None

def process_pdfs(files):
    """Ingests uploaded PDFs and builds the Vector Index"""
    global vector_store
    
    documents = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    
    for file in files:
        loader = PyPDFLoader(file.name)
        docs = loader.load()
        documents.extend(docs)
    
    chunks = text_splitter.split_documents(documents)
    
    # Create Embeddings
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_ID)
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    return f"✅ Knowledge Base Ready! Processed {len(chunks)} chunks from {len(files)} files."

def answer_query(message, history):
    """Retrieves context and generates an answer"""
    if vector_store is None:
        return "⚠️ Please upload a PDF first."
    
    # Setup Retriever
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    
    # Setup LLM (Using free HF Inference API)
    llm = HuggingFaceHub(
        repo_id=LLM_REPO, 
        model_kwargs={"temperature": 0.5, "max_length": 512},
        huggingfacehub_api_token=HF_TOKEN
    )
    
    # Setup Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    
    # Run Query
    response = qa_chain.invoke({"query": message})
    return response['result']

# 3. UI INTERFACE
with gr.Blocks(theme="soft") as demo:
    gr.Markdown("# 🤖 AI Research Agent (SIC Team 013)")
    
    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(label="Upload Research Papers (PDF)", file_count="multiple")
            upload_btn = gr.Button("Build Knowledge Base", variant="primary")
            status_output = gr.Textbox(label="System Status", interactive=False)
            
        with gr.Column(scale=2):
            chatbot = gr.ChatInterface(
                fn=answer_query,
                chatbot=gr.Chatbot(height=400),
                textbox=gr.Textbox(placeholder="Ask a question about the papers...", container=False),
                title=None,
                description=None,
                theme="soft",
            )

    upload_btn.click(process_pdfs, inputs=[file_input], outputs=[status_output])

if __name__ == "__main__":
    demo.launch()