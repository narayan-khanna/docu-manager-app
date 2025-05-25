from fastapi import APIRouter, HTTPException
from app.models.schema import DocumentSelectionRequest
from app.services.selected_docs import SelectedDocsManager
from app.core.logger import get_logger

router = APIRouter()
logger = get_logger("doc_api")
doc_manager = SelectedDocsManager()

@router.post("/select-docs")
def select_documents(payload: DocumentSelectionRequest):
    try:
        valid_ids, invalid_ids = doc_manager.validate_docs(payload.doc_ids)
        doc_manager.set_user_docs(payload.user_id, valid_ids)

        return {
            "user_id": payload.user_id,
            "accepted_doc_ids": valid_ids,
            "invalid_doc_ids": invalid_ids
        }
    except Exception as e:
        logger.error(f"Document selection failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to select docs")
