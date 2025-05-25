from typing import List
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import OllamaEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from app.core.logger import get_logger

logger = get_logger("qdrant")

COLLECTION_NAME = "document-manager-collection"

class VectorStore:
    def __init__(self):
        self.client = QdrantClient(
            host="qdrant",
            port=6333
        )
        self.embedding_model = OllamaEmbeddings(model="nomic-embed-text")

        self._ensure_collection()

        self.qdrant = Qdrant(
            client=self.client,
            collection_name=COLLECTION_NAME,
            embeddings=self.embedding_model
        )

    def _ensure_collection(self):
        if not self.client.collection_exists(collection_name=COLLECTION_NAME):
            logger.info("Creating new Qdrant collection...")
            self.client.recreate_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE),
            )

    def add_document(self, doc_id: str, text: str):
        logger.info(f"Adding doc {doc_id} to vector DB")
        self.qdrant.add_texts([text], metadatas=[{"doc_id": doc_id}])

    def list_all_doc_ids(self) -> List[str]:
        try:
            scroll_result, _ = self.client.scroll(
                collection_name=COLLECTION_NAME,
                with_payload=True,
                limit=10000
            )
            logger.info(f"Scroll result from Qdrant: {scroll_result}")
            return [
              str(point.payload["metadata"]["doc_id"])
              for point in scroll_result
              if point.payload and "metadata" in point.payload and "doc_id" in point.payload["metadata"]
            ]
        except Exception as e:
            logger.error(f"Failed to list doc_ids from Qdrant: {e}")
            return []



