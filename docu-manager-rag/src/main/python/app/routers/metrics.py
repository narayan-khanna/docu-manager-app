from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.db.db import get_db
from app.models.models import Document, QALog

router = APIRouter()

@router.get("/dashboard/metrics")
def get_dashboard_metrics(db: Session = Depends(get_db)):
    now = datetime.utcnow()

    def count_recent(model, field, days):
        since = now - timedelta(days=days)
        return db.query(func.count()).filter(field >= since).scalar()

    # Document uploads
    uploads_today = count_recent(Document, Document.uploaded_at, 1)
    uploads_month = count_recent(Document, Document.uploaded_at, 30)
    uploads_year = count_recent(Document, Document.uploaded_at, 365)

    # QAs
    qa_today = count_recent(QALog, QALog.asked_at, 1)
    qa_month = count_recent(QALog, QALog.asked_at, 30)
    qa_year = count_recent(QALog, QALog.asked_at, 365)

    # Doc referrals
    doc_ref_counts = {}
    logs = db.query(QALog.referred_docs).all()
    for (doc_str,) in logs:
        for doc_id in (doc_str or "").split(","):
            if doc_id:
                doc_ref_counts[doc_id] = doc_ref_counts.get(doc_id, 0) + 1

    return {
        "documents_uploaded": {
            "today": uploads_today,
            "month": uploads_month,
            "year": uploads_year
        },
        "questions_asked": {
            "today": qa_today,
            "month": qa_month,
            "year": qa_year
        },
        "documents_referred": doc_ref_counts
    }
