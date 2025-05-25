from pydantic import BaseModel
from typing import Optional,List


class DocumentIngestRequest(BaseModel):
    doc_id: str
    content: str

class QARequest(BaseModel):
    # user_id: str
    question: str
    top_k: Optional[int] = 3


class DocumentSelectionRequest(BaseModel):
    user_id: str
    doc_ids: List[str]

