# Legal Document Analyzer

![AI](https://img.shields.io/badge/AI-Powered-purple)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Next.js](https://img.shields.io/badge/Next.js-Frontend-black)


**AI-powered legal document analysis system for contracts and agreements**

---

## 📌 Overview
 
Legal Document Analyzer is an end-to-end AI system that analyzes legal documents such as contracts, NDAs, rental agreements, and employment agreements.  
It provides **clause extraction, risk identification, and plain-English explanations** using a hybrid AI architecture.

This project focuses on **applied NLP, system design, and full-stack engineering**

---

## ✨ Key Features

- 📄 Upload PDF / DOCX / TXT documents  
- 🔍 Automatic clause extraction and classification  
- ⚠️ AI-assisted risk and issue detection  
- 💬 Ask questions using a document-aware AI chatbot  
- 🌐 Web interface with REST APIs for real-time analysis  

---

## 🏗️ Architecture (High Level)

- **Frontend**: Next.js + React  
- **Backend**: FastAPI (Python)  
- **AI / NLP**: InLegalBERT (768-dim embeddings), Groq LLM, CUAD-calibrated risk scoring  
- **Design**: Hybrid system combining ML inference and rule-based logic  

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Groq API key

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev



