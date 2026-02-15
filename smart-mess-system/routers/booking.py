# routers/booking.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import BookingCreate, BookingResponse
from services.validation import (
    validate_student,
    validate_mess,
    validate_booking
)
from services.meal_logic import create_booking


router = APIRouter(prefix="/booking", tags=["Booking"])


# ---------------------------------------------------------
# BOOK MEAL ENDPOINT
# ---------------------------------------------------------

@router.post("/book", response_model=BookingResponse)
def book_meal(request: BookingCreate, db: Session = Depends(get_db)):

    try:
        # 1️⃣ Validate student
        student = validate_student(db, request.student_id)

        # 2️⃣ Validate mess
        mess = validate_mess(db, request.mess_id)

        # 3️⃣ Validate booking rules (cutoff, duplicate, capacity, year)
        meal_type = validate_booking(db, student, mess)

        # 4️⃣ Create booking record
        new_booking = create_booking(
            db=db,
            student_id=student.id,
            mess_id=mess.id,
            meal_type=meal_type
        )

        return new_booking

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error."
        )
