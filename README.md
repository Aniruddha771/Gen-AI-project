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
