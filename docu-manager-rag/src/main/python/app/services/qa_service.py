from app.core.logger import get_logger
from app.db.vector_store import VectorStore
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from app.services.selected_docs import SelectedDocsManager
from app.db.db import get_db
from sqlalchemy.orm import Session
from app.models.models import QALog

logger = get_logger("qa_service")

class QAService:
    def __init__(self):
        self.vector_store = VectorStore()
        self.llm = Ollama(model="mistral")
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vector_store.qdrant.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True
        )
        self.selected_docs_manager = SelectedDocsManager()

    def answer_question(self, query: str, user_id: str):
        selected_docs = list(self.selected_docs_manager.get_user_docs(user_id))
        logger.info(f"User {user_id} selected docs: {selected_docs}")

        retriever = self.vector_store.qdrant.as_retriever(
            search_kwargs={
                "k": 3,
                "filter": {"doc_id": {"$in": selected_docs}} if selected_docs else {}
            }
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=retriever,
            return_source_documents=True
        )

        result = qa_chain({"query": query})
        db: Session = next(get_db())
        doc_ids = [doc.metadata.get("doc_id", "unknown") for doc in result.get("source_documents", [])]
        referred = ",".join(doc_ids)
        db.add(QALog(user_email=user_id, question=query, referred_docs=referred))
        db.commit()

        return {
            "question": query,
            "answer": result["result"],
            "sources": [
                doc.metadata.get("doc_id", "unknown")
                for doc in result.get("source_documents", [])
            ]
        }
