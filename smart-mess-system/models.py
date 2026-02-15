# models.py

from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from database import Base


# ---------------------------------------------------------
# ENUMS
# ---------------------------------------------------------

class MealType(str, enum.Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"


class BookingStatus(str, enum.Enum):
    booked = "booked"
    attended = "attended"
    no_show = "no_show"


# ---------------------------------------------------------
# STUDENT TABLE
# ---------------------------------------------------------

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    hostel = Column(String, nullable=False)

    # Relationships
    bookings = relationship("MealIntent", back_populates="student", cascade="all, delete")
    diet_logs = relationship("DietLog", back_populates="student", cascade="all, delete")


# ---------------------------------------------------------
# MESS TABLE
# ---------------------------------------------------------

class Mess(Base):
    __tablename__ = "mess"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    allowed_year = Column(Integer, nullable=False)
    max_capacity = Column(Integer, nullable=False)

    # Relationships
    bookings = relationship("MealIntent", back_populates="mess", cascade="all, delete")
    diet_logs = relationship("DietLog", back_populates="mess", cascade="all, delete")


# ---------------------------------------------------------
# MEAL INTENT (PRE-BOOKING TABLE)
# ---------------------------------------------------------

class MealIntent(Base):
    __tablename__ = "meal_intent"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    mess_id = Column(Integer, ForeignKey("mess.id"), nullable=False)

    meal_type = Column(Enum(MealType), nullable=False)
    date = Column(Date, nullable=False)

    status = Column(Enum(BookingStatus), default=BookingStatus.booked, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Prevent duplicate booking for same student + date + meal_type
    __table_args__ = (
        UniqueConstraint("student_id", "meal_type", "date", name="unique_student_meal_per_day"),
    )

    # Relationships
    student = relationship("Student", back_populates="bookings")
    mess = relationship("Mess", back_populates="bookings")


# ---------------------------------------------------------
# DIET LOGS (ACTUAL ENTRY RECORD)
# ---------------------------------------------------------

class DietLog(Base):
    __tablename__ = "diet_logs"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    mess_id = Column(Integer, ForeignKey("mess.id"), nullable=False)

    meal_type = Column(Enum(MealType), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="diet_logs")
    mess = relationship("Mess", back_populates="diet_logs")
