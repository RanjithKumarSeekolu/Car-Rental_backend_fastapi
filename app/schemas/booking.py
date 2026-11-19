from app.schemas.base import CamelModel


class BookingCancel(CamelModel):
    reason: str = ""