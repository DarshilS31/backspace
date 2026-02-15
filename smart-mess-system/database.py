# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool

# ---------------------------------------------------------
# DATABASE CONFIGURATION
# ---------------------------------------------------------

# SQLite database file
DATABASE_URL = "sqlite:///./mess.db"

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite
    poolclass=StaticPool  # Ensures single connection in hackathon setup
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()


# ---------------------------------------------------------
# DEPENDENCY FOR FASTAPI ROUTES
# ---------------------------------------------------------

def get_db():
    """
    FastAPI dependency to get DB session.
    Ensures proper opening and closing of DB session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------
# DATABASE INITIALIZATION
# ---------------------------------------------------------


def init_db():
    """
    Call this once in main.py to create tables.
    """

    Base.metadata.create_all(bind=engine)

    from models import Student, Mess, MealIntent, BookingStatus, MealType
    from datetime import date, timedelta

    db = SessionLocal()

    # ---------- DEMO STUDENTS ----------
    if not db.query(Student).first():

        student1 = Student(id=1, name="Rahul Kumar",hostel="Hostel A", year=2)
        student2 = Student(id=2, name="Aman Singh",hostel="Hostel B", year=2)
        student3 = Student(id=3, name="Priya Sharma", hostel="Hostel C", year=2)
        student4 = Student(id=4, name="Karan Mehta", hostel="Hostel A", year=2)
        student5 = Student(id=5, name="Neha Verma", hostel="Hostel B", year=2)
        student6 = Student(id=6, name="Arjun Patel", hostel="Hostel C", year=2)

        db.add_all([
        student1, 
        student2,
        student3,
        student4,
        student5,
        student6])
        db.commit()

    # ---------- DEMO MESSES ----------
    if not db.query(Mess).first():
        mess1 = Mess(id=1, name="Hostel A", allowed_year=2, max_capacity=200)
        mess2 = Mess(id=2, name="Hostel B", allowed_year=2, max_capacity=180)
        mess3 = Mess(id=3, name="Hostel C", allowed_year=2, max_capacity=150)


        db.add_all([mess1, mess2, mess3])
        db.commit()

    # ---------- DEMO HISTORY ----------
    if not db.query(MealIntent).first():

        for i in range(7):
            demo_entry = MealIntent(
                student_id=1,
                mess_id=1,
                date=date.today() - timedelta(days=i),
                meal_type=MealType.lunch,
                status=BookingStatus.attended
            )
            db.add(demo_entry)

        db.commit()

    db.close()

