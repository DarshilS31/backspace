# routers/dashboard.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Mess, Student, DietLog, MealType
from schemas import (
    MessCountResponse,
    StudentSummaryResponse,
    NoShowResponse
)

from services.capacity import (
    get_booked_count,
    get_attended_count,
    get_remaining_capacity
)

from core.time_utils import get_current_meal_type, get_today_date


router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# ---------------------------------------------------------
# MESS COUNTS (FOR CURRENT MEAL)
# ---------------------------------------------------------

@router.get("/mess-counts", response_model=list[MessCountResponse])
def get_mess_counts(db: Session = Depends(get_db)):

    try:
        meal_type = get_current_meal_type()
        results = []

        mess_list = db.query(Mess).all()

        for mess in mess_list:

            booked = get_booked_count(db, mess.id, meal_type)
            attended = get_attended_count(db, mess.id, meal_type)
            remaining = get_remaining_capacity(db, mess, meal_type)

            results.append(
                MessCountResponse(
                    mess_id=mess.id,
                    mess_name=mess.name,
                    booked=booked,
                    attended=attended,
                    remaining_capacity=remaining
                )
            )

        return results

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch mess counts.")


# ---------------------------------------------------------
# STUDENT SUMMARY
# ---------------------------------------------------------

@router.get("/student-summary/{student_id}", response_model=StudentSummaryResponse)
def get_student_summary(student_id: int, db: Session = Depends(get_db)):

    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    total_meals = db.query(DietLog).filter(
        DietLog.student_id == student_id
    ).count()

    breakfast_count = db.query(DietLog).filter(
        DietLog.student_id == student_id,
        DietLog.meal_type == MealType.breakfast
    ).count()

    lunch_count = db.query(DietLog).filter(
        DietLog.student_id == student_id,
        DietLog.meal_type == MealType.lunch
    ).count()

    dinner_count = db.query(DietLog).filter(
        DietLog.student_id == student_id,
        DietLog.meal_type == MealType.dinner
    ).count()

    return StudentSummaryResponse(
        student_id=student_id,
        total_meals=total_meals,
        breakfast_count=breakfast_count,
        lunch_count=lunch_count,
        dinner_count=dinner_count
    )


# ---------------------------------------------------------
# NO SHOW LIST
# ---------------------------------------------------------

@router.get("/no-shows", response_model=list[NoShowResponse])
def get_no_shows(db: Session = Depends(get_db)):

    today = get_today_date()
    meal_type = get_current_meal_type()

    from models import MealIntent, BookingStatus

    records = db.query(MealIntent).filter(
        MealIntent.date == today,
        MealIntent.meal_type == meal_type,
        MealIntent.status == BookingStatus.no_show
    ).all()

    results = []

    for record in records:
        results.append(
            NoShowResponse(
                student_id=record.student_id,
                student_name=record.student.name,
                meal_type=record.meal_type,
                date=record.date
            )
        )

    return results
