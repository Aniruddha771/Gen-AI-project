# 🧠 Agentic AI-Based Risk Management System

## 📌 Overview
This project implements a **multi-agent AI system** for analyzing project risks using **local LLMs (Ollama)**.  
It combines **internal project data** and **external market signals** to generate **risk scores and actionable reports**.

The system follows an **agentic AI architecture**, where multiple specialized agents collaborate to perform different tasks.

---

## 🤖 Agentic AI Architecture

The system consists of the following agents:

### 🟢 Project Tracking Agent
- Analyzes internal project data  
- Detects:
  - Delays  
  - Budget overruns  

### 🔵 Market Analysis Agent
- Processes external market data (news/API)  
- Identifies:
  - Supply chain issues  
  - Inflation trends  
  - External risks  

### 🟡 Risk Scoring Agent
- Combines outputs from project & market agents  
- Generates:
  - Final risk score  
  - Risk level (Low/Medium/High)  
  - Key contributing factors  

### 🔴 Orchestrator (Risk Manager)
- Controls workflow between agents  
- Executes agents in sequence  
- Aggregates results  

### 🟣 Reporting Agent
- Converts structured outputs into **human-readable insights**  
- Provides:
  - Summary  
  - Recommendations  

---

## 🔄 Workflow

Input Data → Project Agent + Market Agent  
           → Risk Agent (Decision Engine)  
           → Reporting Agent  
           → Final Output (Streamlit UI)  

---

## 🛠️ Tech Stack

- Python  
- Ollama (Llama3 / Phi3) – Local LLM  
- Streamlit – Frontend UI  
- FastAPI (optional) – API layer  
- Requests – API handling  
- JSON – Data storage  

---

## 📊 Features

- Multi-agent AI architecture  
- Local LLM (runs offline)  
- Combines internal + external data  
- Automated risk scoring  
- AI-generated reports  
- Interactive Streamlit UI  

---

## ▶️ How to Run the Project

1. Clone the repository  
   git clone <your-repo-link>  
   cd <project-folder>  

2. Install dependencies  
   pip install -r requirements.txt  

3. Start Ollama  
   ollama serve  

4. Pull model (recommended)  
   ollama pull phi3  

5. Run Streamlit App  
   streamlit run streamlit_app.py  

6. Open in browser  
   http://localhost:8501  

---

## 📁 Project Structure

ai-risk-system/  
│  
├── agents/              # AI agents  
├── core/                # Orchestrator & utilities  
├── data/                # Datasets  
├── streamlit_app.py     # UI  
├── app.py               # API (optional)  
├── requirements.txt  
└── README.md  

---

## 🚀 Future Improvements

- Real-time market API integration  
- Dashboard with visuals  
- Chatbot interface  
- Historical risk tracking  

---

## 🎯 Conclusion

This project demonstrates how Agentic AI systems can:  
- Analyze structured + unstructured data  
- Combine multiple intelligent agents  
- Generate actionable insights in real time  
