# services/validation.py

from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import Student, Mess, MealIntent, BookingStatus, MealType
from services.capacity import enforce_capacity
from core.time_utils import (
    get_current_meal_type,
    is_before_cutoff,
    is_within_meal_window,
    get_today_date
)


# ---------------------------------------------------------
# VALIDATE STUDENT
# ---------------------------------------------------------

def validate_student(db: Session, student_id: int) -> Student:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# ---------------------------------------------------------
# VALIDATE MESS
# ---------------------------------------------------------

def validate_mess(db: Session, mess_id: int) -> Mess:
    mess = db.query(Mess).filter(Mess.id == mess_id).first()
    if not mess:
        raise HTTPException(status_code=404, detail="Mess not found")
    return mess


# ---------------------------------------------------------
# VALIDATE YEAR ELIGIBILITY
# ---------------------------------------------------------

def validate_year(student: Student, mess: Mess):
    if student.year != mess.allowed_year:
        raise HTTPException(
            status_code=400,
            detail="You are not allowed to book this mess."
        )


# ---------------------------------------------------------
# VALIDATE BOOKING FLOW
# ---------------------------------------------------------

def validate_booking(db: Session, student: Student, mess: Mess):

    meal_type = get_current_meal_type()
    today = get_today_date()

    # Cutoff check
    # if not is_before_cutoff(meal_type):
    #     raise HTTPException(
    #         status_code=400,
    #         detail=f"Booking closed for {meal_type.value}."
    #     )

    # Duplicate booking check
    existing = db.query(MealIntent).filter(
        MealIntent.student_id == student.id,
        MealIntent.meal_type == meal_type,
        MealIntent.date == today
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="You have already booked this meal."
        )

    # Year validation
    validate_year(student, mess)

    # Capacity enforcement (delegated to capacity service)
    enforce_capacity(db, mess, meal_type)

    return meal_type


# ---------------------------------------------------------
# VALIDATE SCAN FLOW
# ---------------------------------------------------------

# def validate_scan(db: Session, student_id: int, mess_id: int):

#     meal_type = get_current_meal_type()
#     today = get_today_date()

#     booking = db.query(MealIntent).filter(
#         MealIntent.student_id == student_id,
#         MealIntent.date == today,
#         MealIntent.meal_type == meal_type
#     ).first()

#     # if not booking:
#     #     raise HTTPException(
#     #         status_code=400,
#     #         detail="No booking found for this meal."
#     #     )
#     # 🔥 DEMO MODE: Auto-create booking if missing
#     if not booking:
#         from models import MealIntent, BookingStatus
#         booking = MealIntent(
#             student_id=student_id,
#             mess_id=mess_id,
#             date=today,
#             meal_type=meal_type,
#             status=BookingStatus.booked
#         )
#         db.add(booking)
#         db.commit()
#         db.refresh(booking)


#     if booking.mess_id != mess_id:
#         raise HTTPException(
#             status_code=400,
#             detail="You did not book this mess."
#         )

#     if booking.status == BookingStatus.attended:
#         raise HTTPException(
#             status_code=400,
#             detail="Already marked as attended."
#         )

#     # Check if meal window active
#     # if not is_within_meal_window(meal_type):
#     #     raise HTTPException(
#     #         status_code=400,
#     #         detail="Meal window closed."
#     #     )

#     return booking, meal_type
def validate_scan(db: Session, student_id: int, mess_id: int):

    meal_type = get_current_meal_type()
    today = get_today_date()

    booking = db.query(MealIntent).filter(
        MealIntent.student_id == student_id,
        MealIntent.date == today,
        MealIntent.meal_type == meal_type
    ).first()

    # DEMO MODE — Auto create booking if missing
    if not booking:
        booking = MealIntent(
            student_id=student_id,
            mess_id=mess_id,
            date=today,
            meal_type=meal_type,
            status=BookingStatus.booked
        )
        db.add(booking)
        db.commit()
        db.refresh(booking)

    # Prevent double attendance
    if booking.status == BookingStatus.attended:
        raise HTTPException(
            status_code=400,
            detail="Already marked as attended."
        )

    return booking, meal_type
