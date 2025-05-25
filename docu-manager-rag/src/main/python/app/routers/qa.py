from fastapi import APIRouter, HTTPException, Depends
from app.models.schema import QARequest
from app.services.qa_service import QAService
from app.core.logger import get_logger
from app.core.auth import get_current_user

router = APIRouter()
logger = get_logger("qa_api")
qa_service = QAService()

@router.post("/qa")
def run_qa(payload: QARequest, user=Depends(get_current_user)):
    try:
        return qa_service.answer_question(payload.question, user["user_id"])
    except Exception as e:
        logger.error(f"Q&A failed: {e}")
        raise HTTPException(status_code=500, detail="Q&A failed")

