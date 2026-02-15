# routers/scan.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import ScanRequest, ScanResponse
from services.validation import validate_scan
from services.meal_logic import mark_attendance


router = APIRouter(prefix="/scan", tags=["Scan"])


# ---------------------------------------------------------
# QR SCAN ENTRY ENDPOINT
# ---------------------------------------------------------

@router.post("/entry", response_model=ScanResponse)
def scan_entry(request: ScanRequest, db: Session = Depends(get_db)):

    try:
        # 1️⃣ Validate scan (booking exists, correct mess, not duplicate, window active)
        booking, meal_type = validate_scan(
            db=db,
            student_id=request.student_id,
            mess_id=request.mess_id
        )

        # 2️⃣ Mark attendance + create DietLog
        result = mark_attendance(
            db=db,
            booking=booking,
            meal_type=meal_type
        )

        return result

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error."
        )
