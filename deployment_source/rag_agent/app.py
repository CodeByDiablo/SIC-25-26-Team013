import gradio as gr
import os
import PyPDF2
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferWindowMemory

# -- CONFIGURATION --
MODEL_ID = "llama-3.3-70b-versatile"

class ResearchAgent:
    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            api_key = "Missing_Key" 

        # 1. Initialize Groq LLM
        self.llm = ChatGroq(
            groq_api_key=api_key,
            model_name=MODEL_ID,
            temperature=0.2,
            max_tokens=2048
        )
        
        # 2. Initialize Embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        self.vector_store = None
        self.agent = None
        
        # 3. Memory
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            k=5,
            return_messages=True
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    
    def process_pdfs(self, files):
        if not files:
            return "⚠️ No files uploaded."
        
        all_docs = []
        doc_names = []
        
        for file in files:
            try:
                reader = PyPDF2.PdfReader(file.name)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                
                chunks = self.text_splitter.create_documents(
                    [text], 
                    metadatas=[{"source": os.path.basename(file.name)}]
                )
                all_docs.extend(chunks)
                doc_names.append(os.path.basename(file.name))
            except Exception as e:
                return f"❌ Error reading {file.name}: {e}"
        
        if all_docs:
            self.vector_store = FAISS.from_documents(all_docs, self.embeddings)
            
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(search_kwargs={"k": 5}),
            )
            
            tools = [
                Tool(
                    name="Academic_Knowledge_Base",
                    func=lambda q: qa_chain.invoke({"query": q})["result"],
                    description="ALWAYS use this tool to answer questions based on the uploaded research papers."
                )
            ]
            
            self.agent = initialize_agent(
                tools=tools,
                llm=self.llm,
                agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                memory=self.memory,
                verbose=True,
                handle_parsing_errors=True
            )
            
            return f"✅ Indexed {len(all_docs)} chunks from: {', '.join(doc_names)}"
        else:
            return "❌ No text found in documents."

    def chat(self, message, history):
        if not self.agent:
            return "⚠️ System Offline. Please upload research papers to initialize the Knowledge Base."
        
        try:
            return self.agent.run(message)
        except Exception as e:
            return f"Analysis Error: {str(e)}"

# -- UI SETUP --
bot = ResearchAgent()

# CSS for styling (Fixed to allow API visibility)
CUSTOM_CSS = """
.container {max-width: 900px; margin: auto; padding-top: 20px;}
footer {visibility: hidden}
.custom-footer {text-align: center; color: #666; margin-top: 20px;}
"""

# Build the Interface
with gr.Blocks(theme="soft", title="SIC Team 013 Research Agent", css=CUSTOM_CSS) as demo:
    gr.HTML("<h1 style='text-align: center'>🤖 AI Research Agent (SIC Team 013)</h1>")
    gr.Markdown("<p style='text-align: center'>Upload private technical documents and ask complex queries.</p>")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📂 Knowledge Base")
            file_input = gr.File(label="Upload PDFs", file_count="multiple", file_types=[".pdf"])
            upload_btn = gr.Button("Build Vector Index", variant="primary")
            status = gr.Textbox(label="System Status", interactive=False)
            
        with gr.Column(scale=2):
            gr.Markdown("### 💬 Research Interface")
            chatbot = gr.ChatInterface(
                fn=bot.chat,
                chatbot=gr.Chatbot(height=500),
                textbox=gr.Textbox(placeholder="Ask a specific question about the papers...", container=False)
            )

    # API ENDPOINT 1: UPLOAD KNOWLEDGE (Registers the name '/upload_knowledge')
    upload_btn.click(
        bot.process_pdfs, 
        inputs=[file_input], 
        outputs=[status],
        api_name="upload_knowledge" 
    )
    
    # API ENDPOINT 2: Chat is handled automatically by ChatInterface as '/chat'
    
    gr.HTML("<div class='custom-footer'>SIC Phase 1 Complete (Live API)</div>")

if __name__ == "__main__":
    demo.launch()
