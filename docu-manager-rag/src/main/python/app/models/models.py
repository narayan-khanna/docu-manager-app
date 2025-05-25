from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True) 
    uploaded_at = Column(DateTime, default=func.now())
    uploader_email = Column(String)

class QALog(Base):
    __tablename__ = "qa_logs"
    id = Column(Integer, primary_key=True)
    asked_at = Column(DateTime, default=func.now())
    user_email = Column(String)
    question = Column(String)
    referred_docs = Column(String)
