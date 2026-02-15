# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import init_db, SessionLocal
from scheduler import start_scheduler
from models import Student, Mess

# Routers
from routers.auth import router as auth_router
from routers.booking import router as booking_router
from routers.scan import router as scan_router
from routers.dashboard import router as dashboard_router
from models import Student, Mess

def seed_demo_data(db):
    if db.query(Student).count() == 0:
        students = [
            Student(id=1, name="Rahul", year=1, hostel="H1"),
            Student(id=2, name="Aman", year=1, hostel="H1"),
            Student(id=3, name="Priya", year=2, hostel="H2"),
            Student(id=4, name="Karan", year=2, hostel="H2"),
            Student(id=5, name="Sneha", year=3, hostel="H3"),
        ]
        db.add_all(students)

    if db.query(Mess).count() == 0:
        messes = [
            Mess(name="H1 Mess", year=1, capacity=3),
            Mess(name="H2 Mess", year=2, capacity=3),
            Mess(name="H3 Mess", year=3, capacity=3),
        ]
        db.add_all(messes)

    db.commit()


# ---------------------------------------------------------
# CREATE APP
# ---------------------------------------------------------

app = FastAPI(title="Smart Mess QR System")


# ---------------------------------------------------------
# ENABLE CORS (For Frontend Integration)
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# DATABASE INIT + DEMO SEEDING
# ---------------------------------------------------------

def seed_demo_data():
    """
    Creates demo students and messes if DB is empty.
    """

    db: Session = SessionLocal()

    try:
        if db.query(Student).count() == 0:

            students = [
                Student(id=1, name="Rahul", year=1, hostel="H1"),
                Student(id=2, name="Ankit", year=1, hostel="H1"),
                Student(id=3, name="Priya", year=1, hostel="H2"),
                Student(id=4, name="Sahil", year=2, hostel="H3"),
                Student(id=5, name="Neha", year=2, hostel="H3"),
            ]

            db.add_all(students)
            db.commit()

        if db.query(Mess).count() == 0:

            messes = [
                Mess(id=1, name="H1 Mess", allowed_year=1, max_capacity=3),
                Mess(id=2, name="H2 Mess", allowed_year=1, max_capacity=2),
                Mess(id=3, name="H3 Mess", allowed_year=2, max_capacity=3),
            ]

            db.add_all(messes)
            db.commit()

    finally:
        db.close()


# ---------------------------------------------------------
# STARTUP EVENT
# ---------------------------------------------------------

@app.on_event("startup")
def startup_event():
    init_db()
    seed_demo_data()
    start_scheduler()
    print("Smart Mess System Started Successfully 🚀")


# ---------------------------------------------------------
# INCLUDE ROUTERS
# ---------------------------------------------------------

app.include_router(auth_router)
app.include_router(booking_router)
app.include_router(scan_router)
app.include_router(dashboard_router)


# ---------------------------------------------------------
# ROOT CHECK
# ---------------------------------------------------------

@app.get("/")
def root():
    return {"message": "Smart Mess QR System is Running 🚀"}
