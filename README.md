# LLM-Powered Autonomous Data Insight Generator

### An intelligent, agent-based Streamlit application that analyzes structured datasets (CSV, Excel, JSON), generates insights, and enables natural language conversations with your data — just like a senior data scientist.

---

## Features

### AI-Powered Insight Generation

- Automatically identifies important columns in your dataset
- Suggests the most relevant insights
- Categorizes insights (performance, behavioral, demographic, statistical, etc.)
- Generates advanced statistical observations from user-selected columns

### Continuous Chat Interface

- WhatsApp-style chat with scrolling memory
- Ask any natural language question about your dataset
- Generates charts, plots, and text insights
- Keeps chat history per session
- Follow-up question suggestions
- Chat logs saved in `chat_logs/` folder
- One-click download of the entire conversation

### Chart Support

- Auto-generates `Plotly` visualizations from LLM outputs
- Supports bar, line, pie, and more
- Intelligent chart recommendations based on user queries

---

## Tech Stack

| Component       | Technology                           |
| --------------- | ------------------------------------ |
| Frontend        | `Streamlit`                        |
| LLM Integration | `Ollama` (local), `Groq` (cloud) |
| Agent Framework | `LangChain`                        |
| Visualization   | `Plotly , Matplotlib`              |
| Environment     | `Python 3.9+`                      |
| File Formats    | `.csv`, `.xlsx`, `.json`       |

---
