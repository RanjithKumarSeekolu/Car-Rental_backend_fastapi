from fastapi import APIRouter

from app.api.v1.endpoints import bookings, locations

api_router = APIRouter()
api_router.include_router(locations.router, prefix="/locations", tags=["locations"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["bookings"])