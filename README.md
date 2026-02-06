# 🚀 Nova AI Ecosystem: Dual-AI Solutions Suite (Team 013)

> **Samsung Innovation Campus (SIC) Capstone Project**
> *Automating Recruitment and Technical Research with Generative AI & Microservices.*

![Project Status](https://img.shields.io/badge/Status-Completed-success)
![Team](https://img.shields.io/badge/Team-Nova%20(013)-blueviolet)
![Stack](https://img.shields.io/badge/Stack-Llama3%20|%20LangChain%20|%20FAISS%20|%20Gradio-orange)

## 📖 Overview
The **Nova AI Ecosystem** is a unified "Headless Microservices" platform designed to solve efficiency bottlenecks in two critical domains:

1.  **Recruitment Automation:** An Intelligent Resume Screener that acts as a strict Application Tracking System (ATS). It contextually scores candidates, identifies missing skills, and drafts cover letters.
2.  **Research Efficiency:** An Agentic RAG (Retrieval-Augmented Generation) system that allows researchers to query dense technical PDF documents using natural language.

---

## 🚀 Live Deployments (Interactive Demos)
We have deployed our solutions as independent microservices aggregated by a unified Vercel frontend.

| Platform | Type | Link | Status |
| :--- | :--- | :--- | :--- |
| **Vercel** | **Unified Dashboard** | [**🚀 Launch App**](https://sic-team013-frontend.vercel.app/) | 🟢 Live |
| **Hugging Face** | **AI Agent Backend** | [🤖 View Space](https://huggingface.co/spaces/CodeByDiablo/RAG-Agent) | 🟢 Live (API) |
| **Hugging Face** | **Resume Screener Backend** | [📄 View Space](https://huggingface.co/spaces/CodeByDiablo/Resume-Screener) | 🟢 Live (API) |

---

## 👥 Team 013 Members (Team Nova)

| Member Name | Email ID | Role | Key Responsibilities |
| :--- | :--- | :--- | :--- |
| **Vasamsetti Naga Bala (Swamy)** | balaswamyvasamsetti@gmail.com | **Team Leader** | • Project Management & Scope Definition<br>• "Dual-AI" Architecture Planning |
| **Devesh Panwar** | devesh10v@gmail.com | **Presentation & Docs** | • **Architecture Lead:** Headless UI Integration<br>• Frontend Dashboard (Vercel/Gradio) |
| **Dhadi Eswar** | 907dhadieswar@gmail.com | **Data Lead** | • Dataset Curation (50+ Resumes, 20+ Papers)<br>• PDF Text Extraction & Cleaning |
| **Kovvuri PC Durga Reddy** | durgareddy5548p@gmail.com | **Model Builder** | • **Core AI Logic:** RAG Pipeline & Llama 3<br>• Vector Database Optimization (FAISS) |
| **Sakshi** | sakshi01526@gmail.com | **Research** | • QA Testing & Prompt Engineering<br>• Validation of Retrieval Accuracy |

---

## 🛠️ Tech Stack & Architecture

### 🔹 Primary: AI Research Agent (RAG)
An intelligent chatbot designed to query private technical documentation.
* **Model:** Llama 3.3 (70B) via Groq Cloud.
* **Vector Store:** **FAISS** (In-Memory) for sub-millisecond retrieval.
* **Orchestration:** LangChain for document splitting (Chunk Size: 1000) and context injection.

### 🔹 Module: Intelligent Resume Screener
A Generative AI tool that automates candidate shortlisting. Unlike traditional ATS scanners that look for exact keyword matches, this tool uses LLMs to "reason" about a candidate's experience.
* **Features:** Match Scoring (0-100%), Missing Keyword Detection, and Automated Cover Letter drafting.
* **Integration:** Exposes a REST API consumed by the Vercel frontend.

---

## 🔌 API Usage (Headless Architecture)
Both solutions expose RESTful API endpoints, allowing integration with external frontends.

**Example: querying the RAG Agent**
```javascript
import { client } from "@gradio/client";

// 1. Initialize Connection
const app = await client("CodeByDiablo/RAG-Agent");

// 2. Query the Agent with a PDF context
const chatResult = await app.predict("/chat", ["What is the conclusion of the paper?", []]);
console.log(chatResult.data);
```
📂 Repository Structure
```
nova-ai-ecosystem/
├── data/
│   ├── rag_documents/       # PDF Research Papers (Knowledge Base)
│   └── resumes_dataset/     # Anonymized Professional CVs (Test Set)
├── deployment_source/
│   ├── rag_backend/         # LangChain + FAISS Agent implementation
│   └── resume_screener/     # Llama 3 + Groq implementation
├── notebook/
│   └── rag_research_lab.ipynb # EDA, Prototyping, and Chunking logic
├── submission_templates/
│   ├── 1 Project Action Plan.docx
│   ├── 2 WBS Worksheet.xlsx
│   └── 3 Final Project Report.docx
├── requirements.txt         # Project dependencies
└── README.md                # Project Documentation
```
---
Samsung Innovation Campus Capstone Project Submitted by Team 013
