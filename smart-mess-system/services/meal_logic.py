# services/meal_logic.py

from sqlalchemy.orm import Session
from datetime import date, datetime

from models import MealIntent, DietLog, BookingStatus, MealType


# ---------------------------------------------------------
# CREATE BOOKING RECORD
# ---------------------------------------------------------

def create_booking(
    db: Session,
    student_id: int,
    mess_id: int,
    meal_type: MealType
) -> MealIntent:

    today = date.today()

    new_booking = MealIntent(
        student_id=student_id,
        mess_id=mess_id,
        meal_type=meal_type,
        date=today,
        status=BookingStatus.booked
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking


# ---------------------------------------------------------
# MARK ATTENDANCE (SCAN SUCCESS)
# ---------------------------------------------------------

def mark_attendance(
    db: Session,
    booking: MealIntent,
    meal_type: MealType
):

    # Update booking status
    booking.status = BookingStatus.attended

    # Insert diet log
    new_log = DietLog(
        student_id=booking.student_id,
        mess_id=booking.mess_id,
        meal_type=meal_type,
        timestamp=datetime.utcnow()
    )

    db.add(new_log)
    db.commit()
    db.refresh(booking)

    return {
        "message": "Attendance marked successfully.",
        "status": booking.status,
        "meal_type": meal_type,
        "timestamp": new_log.timestamp
    }


# ---------------------------------------------------------
# GET MESS BOOKING COUNT
# ---------------------------------------------------------

def get_mess_booking_count(
    db: Session,
    mess_id: int,
    meal_type: MealType
) -> int:

    today = date.today()

    return db.query(MealIntent).filter(
        MealIntent.mess_id == mess_id,
        MealIntent.meal_type == meal_type,
        MealIntent.date == today,
        MealIntent.status == BookingStatus.booked
    ).count()


# ---------------------------------------------------------
# MARK NO-SHOW MANUALLY (Optional Utility)
# ---------------------------------------------------------

def mark_no_show(db: Session, booking: MealIntent):
    booking.status = BookingStatus.no_show
    db.commit()
    db.refresh(booking)
    return booking
