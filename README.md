# 📚 DocuManager: RAG-Based Document QA System

A full-stack production-ready system for **Document Uploading**, **Ingestion**, and **RAG-based Q&A**, using:

- 🧠 **RAG Engine** (`docu-manager-rag`) – Embedding, vector storage, and document retrieval
- 🔐 **Authentication Service** (`docu-manager-auth`) – User signup/login with JWT auth
- 🌐 **Frontend** (`docu-manager-fe`) – React UI for document management and Q&A
- 🗃️ PostgreSQL, Qdrant, Ollama for persistent, vectorized, and LLM-based responses

---

## 🚀 Repositories Overview

### 🧠 `docu-manager-rag` (RAG Service)

- FastAPI app built with PyBuilder
- Ingests documents, generates embeddings, stores them in Qdrant
- Exposes `/qa` endpoint to answer user questions based on selected documents

### 🔐 `docu-manager-auth` (Auth Service)

- FastAPI app with PyBuilder
- Handles user registration, login, JWT generation
- Stores users in PostgreSQL

### 🌐 `docu-manager-fe` (Frontend)

- React + MUI interface
- Supports file upload, ingestion, document selection, Q&A
- Auth integration + token management
- Chart dashboard for usage analytics

---

## 📦 Services & APIs

---

### 🔐 `docu-manager-auth` API

**Base URL**: `http://localhost:8001`

#### POST `/auth/register`

Registers a new user.

**Request:**

```json
{
  "email": "admin@rag.ai",
  "password": "admin123",
  "role": "admin"
}
```

#### POST `/auth/login`

Logs in an existing user.

Request:

```json
{
  "email": "admin@rag.ai",
  "password": "admin123"
}
```

Response:

```json
{
  "token": "eyJhbGciOi..."
}
```

### 🧠 docu-manager-rag API

**Base URL**: `http://localhost:8000`

`All endpoints require Authorization: Bearer <token>`

#### POST `/ingest`

Uploads and ingests a document file.

Request: multipart/form-data

```json
file: <pdf/docx/txt/csv/json>
```

Response

```json
Always show details

{
  "doc_id": "bfa4b1c8-...",
  "embedding_dim": 768
}
```

#### `GET /documents`

Fetches all document IDs and timestamps.

Response:

```json
[
  {
    "doc_id": "doc001",
    "timestamp": "2025-05-25 08:00",
    "status": "Ingested"
  }
]
```

#### POST `/select-docs`

Sets active documents for current user to be used in Q&A.

Request:

```json
{
  "doc_ids": ["doc001", "doc003"]
}
```

Response:

```json
{
  "accepted_doc_ids": ["doc001", "doc003"],
  "invalid_doc_ids": []
}
```

#### POST `/qa`

Answers a question using RAG on selected documents.

Request

```json
{
  "question": "What does LangChain do?"
}
```

Response

```json
{
  "answer": "LangChain is a Python framework...",
  "sources": ["doc001", "doc003"]
}
```
#### GET `/dashboard/metrics`

Returns aggregated dashboard metrics.

Response:
```json
{
  "documents_uploaded": {
    "today": 3,
    "month": 20,
    "year": 310
  },
  "questions_asked": {
    "today": 7,
    "month": 40,
    "year": 90
  },
  "documents_referred": {
    "doc001": 5,
    "doc002": 2
  }
}

```


#### 🧠 Tech Stack

* Backend: FastAPI, PyBuilder, PostgreSQL, Qdrant, Ollama

* Frontend: React + TypeScript, MUI, Recharts

* Infra: Docker Compose, JWT, RESTful APIs

* Build: PyBuilder (for backend services)

