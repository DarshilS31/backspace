# routers/auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Student
from schemas import StudentResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ---------------------------------------------------------
# STUDENT LOGIN (Simple ID-Based)
# ---------------------------------------------------------

@router.post("/login", response_model=StudentResponse)
def login(student_id: int, db: Session = Depends(get_db)):
    """
    Simple login using student ID.
    No password for hackathon simplicity.
    """

    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


# ---------------------------------------------------------
# GET STUDENT PROFILE
# ---------------------------------------------------------

@router.get("/student/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):

    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student
