from app.core.logger import get_logger
from app.db.vector_store import VectorStore
from typing import List

logger = get_logger("embedding_service")

class EmbeddingService:
    def __init__(self):
        self.vector_store = VectorStore()

    def generate_embedding(self, doc_id: str, text: str) -> List[float]:
        try:
            logger.info("Embedding + storing document...")
            self.vector_store.add_document(doc_id, text)
            return self.vector_store.embedding_model.embed_query(text)
        except Exception as e:
            logger.error(f"Embedding failed: {str(e)}")
            raise
