# scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime, date

from database import SessionLocal
from models import MealIntent, BookingStatus, MealType
from config import MEAL_WINDOWS, NO_SHOW_CHECK_INTERVAL


# ---------------------------------------------------------
# HELPER: CHECK IF MEAL WINDOW HAS ENDED
# ---------------------------------------------------------

def has_meal_window_ended(meal_type: MealType) -> bool:
    """
    Returns True if current time is past the end of meal window.
    """
    now = datetime.now().time()
    window_end = MEAL_WINDOWS[meal_type.value]["end"]
    return now > window_end


# ---------------------------------------------------------
# NO-SHOW UPDATE JOB
# ---------------------------------------------------------

def update_no_shows():
    """
    Background task:
    Marks all 'booked' entries as 'no_show'
    if meal window has passed and they didn't attend.
    """

    db: Session = SessionLocal()

    try:
        today = date.today()

        # Get all bookings still marked as 'booked'
        bookings = db.query(MealIntent).filter(
            MealIntent.date == today,
            MealIntent.status == BookingStatus.booked
        ).all()

        for booking in bookings:
            if has_meal_window_ended(booking.meal_type):
                booking.status = BookingStatus.no_show

        db.commit()

    except Exception as e:
        print("Scheduler error:", e)

    finally:
        db.close()


# ---------------------------------------------------------
# START SCHEDULER
# ---------------------------------------------------------

scheduler = BackgroundScheduler()

def start_scheduler():
    """
    Starts the background scheduler.
    Should be called once from main.py
    """
    scheduler.add_job(
        update_no_shows,
        "interval",
        seconds=NO_SHOW_CHECK_INTERVAL
    )
    scheduler.start()
