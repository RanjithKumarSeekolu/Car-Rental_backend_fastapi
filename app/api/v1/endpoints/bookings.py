from fastapi import APIRouter

from app.api.deps import CurrentUser
from app.core.exceptions import AppError
from app.services import booking_service

router = APIRouter()


@router.get("/{booking_id}")
def get_booking(booking_id: str, user: CurrentUser):
    booking = booking_service.get_booking_for_user(booking_id, user)
    return {"success": True, "booking": booking}


@router.put("/{booking_id}/confirm")
def confirm_booking(booking_id: str, user: CurrentUser):
    raise AppError(400, "Complete Razorpay checkout to confirm this booking")