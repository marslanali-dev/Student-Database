from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Please create a .env file with your Neon database connection string.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Database Model
class StudentResult(Base):
    __tablename__ = "student_results"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, index=True)
    subject = Column(String, index=True)
    score = Column(Float)
    grade = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models for API
class StudentResultCreate(BaseModel):
    student_name: str
    subject: str
    score: float
    grade: str

class StudentResultResponse(BaseModel):
    id: int
    student_name: str
    subject: str
    score: float
    grade: str

    class Config:
        from_attributes = True

# FastAPI app
app = FastAPI(title="Student Results API", description="API for managing student results in Neon database")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/results/", response_model=StudentResultResponse)
def create_result(result: StudentResultCreate, db: Session = Depends(get_db)):
    db_result = StudentResult(**result.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

@app.get("/results/", response_model=list[StudentResultResponse])
def read_results(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    results = db.query(StudentResult).offset(skip).limit(limit).all()
    return results

@app.get("/results/{result_id}", response_model=StudentResultResponse)
def read_result(result_id: int, db: Session = Depends(get_db)):
    result = db.query(StudentResult).filter(StudentResult.id == result_id).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Result not found")
    return result

@app.put("/results/{result_id}", response_model=StudentResultResponse)
def update_result(result_id: int, result: StudentResultCreate, db: Session = Depends(get_db)):
    db_result = db.query(StudentResult).filter(StudentResult.id == result_id).first()
    if db_result is None:
        raise HTTPException(status_code=404, detail="Result not found")
    for key, value in result.dict().items():
        setattr(db_result, key, value)
    db.commit()
    db.refresh(db_result)
    return db_result

@app.delete("/results/{result_id}")
def delete_result(result_id: int, db: Session = Depends(get_db)):
    result = db.query(StudentResult).filter(StudentResult.id == result_id).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Result not found")
    db.delete(result)
    db.commit()
    return {"message": "Result deleted successfully"}

@app.get("/")
def read_root():
    return {"message": "Welcome to Student Results API"}