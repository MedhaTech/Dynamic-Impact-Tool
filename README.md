# LLM-Powered Autonomous Data Insight Generator

An interactive Streamlit-based web application that acts like a **Senior Data Scientist Agent** to generate advanced data insights, visualizations, and answer questions — powered by **Gemma (via Ollama locally)** and **Groq (cloud)**.

---

## Features

- Upload structured data (`.csv`, `.xlsx`, `.json`, `.xml`)
- Auto-generates insights across 7 categories:
  - Performance & Accuracy Insights
  - Question-Specific Insights
  - Attempt & Behavioral Insights
  - Comparative & Demographic Insights
  - Question Design & Learning Insights
  - Advanced Statistical Insights
  - Actionable Recommendations
- Advanced auto visualizations using Plotly
- Intelligent Q&A on your dataset
- Dual-model integration:
  - `Gemma` (offline via Ollama)
  - `Groq` (cloud-based, faster inference)

---



## Folder Structure

GenAI/

│

├── app.py                          # Streamlit app

├── prompts/

│   └── system_prompts.txt          # LLM system instructions

├── models/

│   └── local_model.py              # Model interface

├── utils/

│   ├──  **init** .py

│   ├── chat_handler.py             # Handles chat with LLM

│   ├── data_cleaner.py             # Cleaning utilities

│   ├── file_loader.py              # File parsing

│   ├── groq_handler.py             # Groq-based inference

│   ├── insight_generator.py        # Prompt and generate insights

│   ├── ollama_handler.py           # Gemma (local model) handler

│   ├── prompt_engine.py            # Prompt formatter

│   ├── rag_engine.py               # 🔄 Future integration (RAG)

│   └── visualizer.py               # Plotting functions
