# core/time_utils.py

from datetime import datetime, date, time
from typing import Optional

from config import MEAL_WINDOWS, BOOKING_CUTOFF, ENABLE_TIME_OVERRIDE, SIMULATED_TIME
from models import MealType


# ---------------------------------------------------------
# CURRENT DATETIME HANDLER (Supports Demo Override)
# ---------------------------------------------------------

def get_current_datetime() -> datetime:
    """
    Returns current datetime.
    Uses simulated time if override enabled.
    """

    if ENABLE_TIME_OVERRIDE and SIMULATED_TIME:
        return SIMULATED_TIME

    return datetime.now()


# ---------------------------------------------------------
# GET CURRENT MEAL TYPE
# ---------------------------------------------------------

def get_current_meal_type() -> MealType:
    """
    Determines current or upcoming meal type.
    """

    now = get_current_datetime().time()

    # Check active meal window first
    for meal, window in MEAL_WINDOWS.items():
        if window["start"] <= now <= window["end"]:
            return MealType(meal)

    # If not active, check upcoming based on cutoff
    for meal, cutoff in BOOKING_CUTOFF.items():
        if now <= cutoff:
            return MealType(meal)

    raise ValueError("No active or upcoming meal window.")


# ---------------------------------------------------------
# CHECK IF WITHIN MEAL WINDOW (ENTRY VALIDATION)
# ---------------------------------------------------------

def is_within_meal_window(meal_type: MealType) -> bool:
    now = get_current_datetime().time()
    window = MEAL_WINDOWS[meal_type.value]

    return window["start"] <= now <= window["end"]


# ---------------------------------------------------------
# CHECK IF BOOKING ALLOWED (CUTOFF VALIDATION)
# ---------------------------------------------------------

def is_before_cutoff(meal_type: MealType) -> bool:
    now = get_current_datetime().time()
    cutoff = BOOKING_CUTOFF[meal_type.value]

    return now <= cutoff


# ---------------------------------------------------------
# CHECK IF MEAL WINDOW HAS ENDED (FOR NO-SHOW)
# ---------------------------------------------------------

def has_meal_window_ended(meal_type: MealType) -> bool:
    now = get_current_datetime().time()
    window_end = MEAL_WINDOWS[meal_type.value]["end"]

    return now > window_end


# ---------------------------------------------------------
# GET TODAY DATE (CENTRALIZED)
# ---------------------------------------------------------

def get_today_date() -> date:
    return get_current_datetime().date()
