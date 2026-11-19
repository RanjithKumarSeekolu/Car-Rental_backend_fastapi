from app.core.exceptions import AppError
from app.repositories import booking_repository
from app.schemas.auth import TokenUser
from app.services import pricing_service
from app.utils.datetime import to_iso

DATE_FIELDS = ("startDate", "endDate", "createdAt", "confirmedAt", "cancelledAt")


def normalize_booking(raw: dict) -> dict:
    booking = dict(raw)
    for field in DATE_FIELDS:
        if field in booking:
            booking[field] = to_iso(booking[field])
    return {**booking, **pricing_service.resolve_split(booking)}


def get_booking_for_user(booking_id: str, user: TokenUser) -> dict:
    raw = booking_repository.get(booking_id)
    if raw is None:
        raise AppError(404, "Booking not found")

    booking = normalize_booking(raw)
    is_party = user.uid in (booking.get("renterId"), booking.get("hostId"))
    if not is_party and user.role != "admin":
        raise AppError(403, "Not authorized")

    return booking

def cancel_booking(booking_id: str, user: TokenUser, reason: str) -> None:
    return 