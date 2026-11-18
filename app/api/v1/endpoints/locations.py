import re

from fastapi import APIRouter, HTTPException, Query
from firebase_admin import firestore

from app.api.deps import AdminUser
from app.core.firebase import db
from app.schemas.location import Location, LocationCreate, LocationListResponse, LocationResponse
from app.services import location_service
from  app.services.location_service import COLLECTION, active_locations, to_public_location

router = APIRouter()

@router.get("/", response_model=LocationListResponse)
def get_locations():
    return {"success": True, "locations": location_service.active_locations()}

@router.get("/{location_id}", response_model=LocationResponse)
def get_location(location_id: str):
    key = location_id.lower()
    doc = db.collection(location_service.COLLECTION).document(key).get()

    if doc.exists:
        location = to_public_location(doc.id, doc.to_dict())
        return {"success": True, "location": location}

    for loc in location_service.active_locations():
        if loc["name"].lower() == key:
            return {"success": True, "location": loc}

    raise HTTPException(status_code=404, detail="Location not found")

@router.get("/search", response_model=LocationListResponse)
def search_locations(
    q: str = "",
    limit: int | None = Query(None, ge=1, le=100),
):
    term = q.strip().lower()
    results = active_locations()
    if term:
        results = [
            loc for loc in results
            if term in loc["name"].lower()
            or term in loc.get("state", "").lower()
            or term in loc["id"]
        ]
    if limit is not None:
        results = results[:limit]
    return {"success": True, "locations": results}

@router.post("/", response_model=LocationResponse, status_code=201)
def create_location(body: LocationCreate, admin: AdminUser):
    location_id = re.sub(r"\s+", "-", (body.id or body.name).strip().lower())
    ref = db.collection(location_service.COLLECTION).document(location_id)

    if ref.get().exists:
        raise HTTPException(409, "Location already exists")

    location = Location(id=location_id, **body.model_dump(exclude={"id"}))
    ref.set({
        **location.model_dump(by_alias=True, exclude={"id"}),
        "createdAt": firestore.SERVER_TIMESTAMP,
        "updatedAt": firestore.SERVER_TIMESTAMP,
        "createdBy": admin.uid,
    })
    return {"success": True, "location": location}

