# services/capacity.py

from sqlalchemy.orm import Session
from datetime import date

from models import MealIntent, BookingStatus, Mess, MealType
from config import ALLOW_BUFFER, BUFFER_PERCENTAGE


# ---------------------------------------------------------
# GET TOTAL BOOKED COUNT
# ---------------------------------------------------------

def get_booked_count(
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
# GET ATTENDED COUNT
# ---------------------------------------------------------

def get_attended_count(
    db: Session,
    mess_id: int,
    meal_type: MealType
) -> int:

    today = date.today()

    return db.query(MealIntent).filter(
        MealIntent.mess_id == mess_id,
        MealIntent.meal_type == meal_type,
        MealIntent.date == today,
        MealIntent.status == BookingStatus.attended
    ).count()


# ---------------------------------------------------------
# CALCULATE MAX CAPACITY (WITH OPTIONAL BUFFER)
# ---------------------------------------------------------

def get_effective_capacity(mess: Mess) -> int:
    """
    Returns effective capacity.
    Applies buffer if enabled.
    """

    if ALLOW_BUFFER:
        buffer = int(mess.max_capacity * BUFFER_PERCENTAGE)
        return mess.max_capacity + buffer

    return mess.max_capacity


# ---------------------------------------------------------
# GET REMAINING CAPACITY
# ---------------------------------------------------------

def get_remaining_capacity(
    db: Session,
    mess: Mess,
    meal_type: MealType
) -> int:

    booked = get_booked_count(db, mess.id, meal_type)
    effective_capacity = get_effective_capacity(mess)

    return effective_capacity - booked


# ---------------------------------------------------------
# ENFORCE CAPACITY LIMIT
# ---------------------------------------------------------

def enforce_capacity(
    db: Session,
    mess: Mess,
    meal_type: MealType
):
    """
    Raises exception if capacity reached.
    """

    remaining = get_remaining_capacity(db, mess, meal_type)

    if remaining <= 0:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=400,
            detail="Mess capacity reached."
        )
