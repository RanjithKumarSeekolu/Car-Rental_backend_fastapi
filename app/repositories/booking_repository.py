from app.core.firebase import db

COLLECTION = "bookings"


def get(booking_id: str) -> dict | None:
    doc = db.collection(COLLECTION).document(booking_id).get()
    if not doc.exists:
        return None
    return {"id": doc.id, **doc.to_dict()}


def update(booking_id: str, data: dict) -> None:
    db.collection(COLLECTION).document(booking_id).update(data)