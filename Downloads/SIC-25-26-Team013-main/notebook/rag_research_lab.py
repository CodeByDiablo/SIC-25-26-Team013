# RAG Research Lab - SIC Team 013
# Purpose: To test PDF ingestion and Chunking Logic before deployment

import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Configuration
DATA_PATH = "../data/rag_documents/"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

print(f"🔬 Starting Research Lab...")
print(f"📂 Looking for documents in: {DATA_PATH}")

# 2. Ingestion Logic
def load_pdfs(directory):
    documents = []
    if not os.path.exists(directory):
        print("⚠️ Data directory not found!")
        return []
        
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(directory, filename)
            try:
                reader = PdfReader(pdf_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                documents.append({"source": filename, "text": text})
                print(f"   ✅ Loaded: {filename} (Length: {len(text)} chars)")
            except Exception as e:
                print(f"   ❌ Error loading {filename}: {e}")
    return documents

# 3. Processing
raw_docs = load_pdfs(DATA_PATH)

if raw_docs:
    # Split text into chunks (RAG Standard)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_chunks = []
    for doc in raw_docs:
        chunks = text_splitter.split_text(doc["text"])
        all_chunks.extend(chunks)
    
    print(f"\n🧩 Splitting Complete.")
    print(f"   Total Source Docs: {len(raw_docs)}")
    print(f"   Total Vector Chunks: {len(all_chunks)}")
    
    print(f"\n🚀 Ready for Vector Embedding ({MODEL_NAME})")
    # Note: Actual embedding is handled in the deployed app to save local resources.
else:
    print("\n No documents found. Please add PDFs to data/rag_documents/")