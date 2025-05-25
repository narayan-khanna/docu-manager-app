from typing import Dict, Set, List
from app.core.logger import get_logger
from app.db.vector_store import VectorStore

logger = get_logger("selected_docs")

class SelectedDocsManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SelectedDocsManager, cls).__new__(cls)
            cls._instance.user_doc_selection = {}
            cls._instance.vector_store = VectorStore()
        return cls._instance

    def validate_docs(self, doc_ids: List[str]) -> (List[str], List[str]):
        existing_docs = set(map(str, self.vector_store.list_all_doc_ids()))
        doc_ids_str = set(map(str, doc_ids))

        valid = list(doc_ids_str & existing_docs)
        invalid = list(doc_ids_str - existing_docs)
        return valid, invalid


    def set_user_docs(self, user_id: str, doc_ids: List[str]):
        self.user_doc_selection[user_id] = set(doc_ids)
        logger.info(f"User {user_id} selected docs: {doc_ids}")

    def get_user_docs(self, user_id: str) -> Set[str]:
        return self.user_doc_selection.get(user_id, set())
