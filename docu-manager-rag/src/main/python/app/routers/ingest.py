from fastapi import APIRouter, HTTPException, Depends,UploadFile, File
from app.models.schema import DocumentIngestRequest
from app.services.embedding_service import EmbeddingService
from app.core.logger import get_logger
from app.core.auth import get_current_user
from app.services.text_extraction import extract_text_from_file
from uuid import uuid4
from datetime import datetime
from app.db.vector_store import VectorStore
from app.db.db import get_db
from sqlalchemy.orm import Session
from app.models.models import Document

router = APIRouter()
logger = get_logger("ingest_api")
embedder = EmbeddingService()

@router.post("/ingest")
async def ingest_file(file: UploadFile = File(...), user=Depends(get_current_user), db: Session = Depends(get_db)):
    doc_id = str(uuid4())
    try:
        content = await extract_text_from_file(file)
        if not content.strip():
            raise HTTPException(status_code=400, detail="Empty or unreadable file content")

        embedding = embedder.generate_embedding(doc_id, content)
        db.add(Document(id=doc_id, uploader_email=user["email"]))
        db.commit()
        return {"doc_id": doc_id, "embedding_dim": len(embedding)}
    except Exception as e:
        logger.error(f"File ingestion failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to process file")

@router.get("/documents")
def list_documents():
    try:
        vs = VectorStore()
        doc_ids = vs.list_all_doc_ids()
        docs = [
            {"doc_id": doc_id, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "status": "Ingested"}
            for doc_id in doc_ids
        ]
        return docs
    except Exception as e:
        logger.error(f"Failed to list documents: {e}")
        return []
