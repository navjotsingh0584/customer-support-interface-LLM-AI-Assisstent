# Customer Support Interface Using LLM

An AI-powered customer support system that uses Large Language Models, Retrieval-Augmented Generation (RAG), document processing, OCR, computer vision, and a React-based frontend to provide intelligent responses to user queries.

## Project Overview

This project is designed to provide an intelligent customer support interface where users can ask questions and receive answers using information from uploaded documents and knowledge-base files.

The system combines a FastAPI backend with a React frontend and integrates local AI/LLM components for document-based question answering.

## What I Developed

- AI-powered customer support chatbot
- LLM-based response generation
- Retrieval-Augmented Generation (RAG)
- PDF and document processing
- Knowledge-base document ingestion
- OCR for extracting text from images and documents
- Image and document analysis
- Computer vision based processing
- User authentication and session management
- React-based frontend interface
- FastAPI backend APIs
- Vector database integration using ChromaDB
- Local LLM integration using Ollama

## Main Workflow

User Query
↓
React Frontend
↓
FastAPI Backend
↓
Query Processing
↓
RAG / Knowledge Retrieval
↓
LLM Response Generation
↓
Response
↓
Frontend

### Document Processing Workflow

Document
↓
Document Processing
↓
Text Extraction / OCR
↓
Chunking
↓
Vector Embeddings
↓
ChromaDB
↓
Relevant Context Retrieval
↓
LLM
↓
Final Answer

## Technologies Used

### Backend

- Python
- FastAPI
- REST APIs

### Frontend

- React
- JavaScript
- HTML
- CSS
- Vite

### AI / LLM

- Large Language Models
- Ollama
- Retrieval-Augmented Generation (RAG)

### Document Processing

- PDF processing
- OCR
- Text extraction
- Document ingestion

### Database / Storage

- ChromaDB
- SQLite

### Computer Vision

- Image processing
- Image classification
- Document analysis

## Project Structure

```text
customer-support-interface-LLM-AI-Assisstent/
│
├── app/
│   ├── auth/
│   ├── routes/
│   ├── services/
│   ├── knowledge/
│   └── main.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── vision_router_v2/
│   └── vision/
│
├── requirements.txt
├── package.json
├── package-lock.json
├── rebuild_index.py
├── create_user.py
└── .gitignore