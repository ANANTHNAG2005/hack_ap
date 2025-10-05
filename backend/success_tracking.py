from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

router = APIRouter()
Base = declarative_base()

# Database setup
DB_URL = "sqlite:///success_logs.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# SQLAlchemy model
class SuccessLogDB(Base):
    __tablename__ = "success_logs"
    id = Column(Integer, primary_key=True, index=True)
    disease = Column(String, nullable=False)
    remedy = Column(Text, nullable=False)
    result = Column(String, nullable=False)  # success/failure
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# Pydantic model
class SuccessLog(BaseModel):
    disease: str
    remedy: str
    result: str  # success/failure

@router.post("/success_log")
async def log_success(entry: SuccessLog):
    db_entry = SuccessLogDB(
        disease=entry.disease,
        remedy=entry.remedy,
        result=entry.result
    )
    session.add(db_entry)
    session.commit()
    session.refresh(db_entry)
    return {"message": "Success log added.", "entry": {
        "id": db_entry.id,
        "disease": db_entry.disease,
        "remedy": db_entry.remedy,
        "result": db_entry.result,
        "timestamp": db_entry.timestamp
    }}

@router.get("/success_logs")
async def get_success_logs():
    logs = session.query(SuccessLogDB).order_by(SuccessLogDB.timestamp.desc()).all()
    return {"logs": [
        {
            "id": log.id,
            "disease": log.disease,
            "remedy": log.remedy,
            "result": log.result,
            "timestamp": log.timestamp
        }
        for log in logs
    ]}
