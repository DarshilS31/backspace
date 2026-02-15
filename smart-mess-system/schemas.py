# schemas.py

from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List
from enum import Enum


# ---------------------------------------------------------
# ENUMS (Must match models.py exactly)
# ---------------------------------------------------------

class MealType(str, Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"


class BookingStatus(str, Enum):
    booked = "booked"
    attended = "attended"
    no_show = "no_show"


# ---------------------------------------------------------
# STUDENT SCHEMAS
# ---------------------------------------------------------

class StudentBase(BaseModel):
    name: str
    year: int
    hostel: str


class StudentCreate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True


# ---------------------------------------------------------
# MESS SCHEMAS
# ---------------------------------------------------------

class MessBase(BaseModel):
    name: str
    allowed_year: int
    max_capacity: int


class MessCreate(MessBase):
    pass


class MessResponse(MessBase):
    id: int

    class Config:
        from_attributes = True


# ---------------------------------------------------------
# MEAL BOOKING (INTENT) SCHEMAS
# ---------------------------------------------------------

class BookingCreate(BaseModel):
    student_id: int
    mess_id: int


class BookingResponse(BaseModel):
    id: int
    student_id: int
    mess_id: int
    meal_type: MealType
    date: date
    status: BookingStatus
    created_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------
# QR SCAN ENTRY SCHEMAS
# ---------------------------------------------------------

class ScanRequest(BaseModel):
    student_id: int
    mess_id: int


class ScanResponse(BaseModel):
    message: str
    status: BookingStatus
    meal_type: MealType
    timestamp: datetime


# ---------------------------------------------------------
# DASHBOARD SCHEMAS
# ---------------------------------------------------------

class MessCountResponse(BaseModel):
    mess_id: int
    mess_name: str
    booked: int
    attended: int
    remaining_capacity: int


class StudentSummaryResponse(BaseModel):
    student_id: int
    total_meals: int
    breakfast_count: int
    lunch_count: int
    dinner_count: int


class NoShowResponse(BaseModel):
    student_id: int
    student_name: str
    meal_type: MealType
    date: date
