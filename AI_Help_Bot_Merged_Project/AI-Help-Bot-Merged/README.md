# MOSDAC AI Help Bot

An intelligent assistant to answer queries from the MOSDAC portal using HuggingFace-based RAG pipeline.

## Features
- Fully local, OpenAI-free
- HuggingFace models for embedding and generation
- FastAPI backend + Streamlit UI
- Modular design with knowledge graph support

## Quickstart
```bash
uvicorn backend.app:app --reload
streamlit run ui/streamlit_app.py
```