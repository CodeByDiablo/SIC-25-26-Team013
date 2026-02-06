# SIC Capstone: Dual-AI Solutions Suite (Team 013)

> **Team ID:** SIC/25-26/Team013
> **Project 1 (Primary):** AI Research Agent (RAG)
> **Project 2 (Module):** Intelligent Resume Screener
> **Status:** Phase 1 Complete (Dual-Deployment Live)

## 🚀 Live Deployments (Interactive Demos)
We have deployed our solutions as microservices for maximum scalability.

| Project | Frontend (UI) | Backend (API) | Status |
| :--- | :--- | :--- | :--- |
| **🤖 AI Research Agent** | [**Click to Chat**](https://huggingface.co/spaces/CodeByDiablo/RAG-Agent) | *Hosted on HF Spaces* | 🟢 Live (Agentic RAG) |
| **📄 Resume Screener** | [**Click to Rank**](https://huggingface.co/spaces/CodeByDiablo/Resume-Screener) | *Hosted on HF Spaces* | 🟢 Live (Llama-3 Powered) |

---

## 👥 Team 013 Members & Contributions

| Member Name | Email ID | Role | Key Contributions |
| :--- | :--- | :--- | :--- |
| **Vasamsetti Naga Bala (Swamy)** | balaswamyvasamsetti@gmail.com | Team Leader | • Project oversight & Scope definition |
| **Devesh Panwar** | devesh10v@gmail.com | Presentation & Docs | • **Architecture Lead:** RAG & GenAI Logic<br>• Frontend UI/UX Design |
| **Dhadi Eswar** | 907dhadieswar@gmail.com | Data Lead | • Data Pipeline & Private Dataset Collection<br>• Exploratory Data Analysis (EDA) |
| **Kovvuri PC Durga Reddy** | durgareddy5548p@gmail.com | Model Builder | • RAG Architecture Optimization<br>• Baseline Model Testing |
| **Sakshi** | sakshi01526@gmail.com | Research | • Research on Retrieval Strategies<br>• Validation against technical benchmarks |

---

## 🔌 API Integration (Headless Architecture)
Both solutions expose RESTful API endpoints, allowing integration with external frontends (e.g., Vercel/React). 

**Example: Integrating RAG Agent into a Web App**
```javascript
import { client } from "@gradio/client";

// 1. Initialize Connection
const app = await client("CodeByDiablo/RAG-Agent");

// 2. Upload Knowledge Base (PDFs)
const uploadResult = await app.predict("/process_pdfs", [fileBlob]);

// 3. Query the Agent
const chatResult = await app.predict("/chat", ["What is the conclusion of the paper?", []]);
console.log(chatResult.data);
```

## 📂 Repository Structure
This repository serves as the central submission hub containing code and data for both projects.

- **`data/`**: Contains separated datasets.
  - `rag_documents/`: Technical Research Papers for the AI Agent.
  - `resumes_dataset/`: Sample CVs for the Resume Screener.
- **`notebook/`**: Exploratory Data Analysis (EDA) and core logic scripts.
  - `rag_research_lab.ipynb`: PDF Ingestion and Chunking logic.
- **`deployment_source/`**: Full source code archives for the live apps.
  - `rag_backend/`: LangChain + FAISS implementation (Agentic Workflow).
  - `resume_screener_gradio/`: Llama-3 + Groq implementation.
- **`submission_templates/`**: Mandatory SIC Phase 1 Reports and Project Action Plans.

---

## 📜 Project Descriptions & Roadmap

### 🔹 Primary: AI Research Agent (SIC/AI/013)
An intelligent chatbot designed to query private technical documentation.
* **Tech Stack:** LangChain, FAISS (In-Memory), Hugging Face Hub.
* **v0.5 Update:** Migrated from ChromaDB to **FAISS** to solve persistent storage conflicts on serverless deployments, resulting in 40% faster retrieval.
* **Agentic Workflow:** Uses `AgentType.CONVERSATIONAL_REACT_DESCRIPTION` to reason about when to search documents versus general knowledge.

### 🔹 Module: Intelligent Resume Screener (GenAI Powered)
A Generative AI tool that automates candidate shortlisting. Unlike traditional ATS scanners that look for exact keyword matches, this tool uses **Llama 3.3 (70B)** to "reason" about a candidate's experience.
* **Features:** Match Scoring (0-100%), Missing Keyword Detection, and **Interview Question Generation**.
* **Tech Stack:** Gradio, Groq API (Llama 3.3), PyPDF2.

---

Submitted by Team 013 for the Samsung Innovation Campus Capstone Project.
