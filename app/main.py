import json
import re
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse
from pathlib import Path

from firebase_admin import firestore
from app.core.firebase import db
from app.schemas.location import Location, LocationListResponse, LocationResponse, LocationCreate
from app.api.deps import AdminUser, CurrentUser

SEED_FILE = Path(__file__).parent / "data" / "locations.seed.json"
SEED_LOCATIONS = json.loads(SEED_FILE.read_text())
COLLECTION = "locations"

app = FastAPI(title="RentNHost API")

@app.get("/", response_class=PlainTextResponse)
def root():
    return "Car Rental"

# Health check endpoint
@app.get("/health")
def health():
    return {"ok": True}

def to_public_location(doc_id: str, data: dict) -> dict:
    return {
        "id": doc_id,
        "name": data.get("name") or doc_id,
        "state": data.get("state", ""),
        "country": data.get("country", "IN"),
        "center": data.get("center") or {"lat": 0, "lng": 0},
        "bounds": data.get("bounds"),
        "isActive": data.get("isActive") is not False,
        "sortOrder": data.get("sortOrder", 99),
        "type": data.get("type", "city"),
    }


def is_catalog_city(data: dict) -> bool:
    if data.get("isActive") is False:
        return False
    center = data.get("center") or {}
    has_geo = isinstance(center.get("lat"), (int, float)) and isinstance(center.get("lng"), (int, float))
    return has_geo and bool(data.get("name"))


def sort_locations(locations: list[dict]) -> list[dict]:
    return sorted(locations, key=lambda loc: (loc["sortOrder"], loc["name"]))


FALLBACK_LOCATIONS = sort_locations(
    [to_public_location(loc["id"], loc) for loc in SEED_LOCATIONS]
)


def active_locations() -> list[dict]:
    try:
        docs = db.collection(COLLECTION).stream()
        locations = [
            to_public_location(doc.id, doc.to_dict())
            for doc in docs
            if is_catalog_city(doc.to_dict())
        ]
    except Exception:
        return FALLBACK_LOCATIONS
    return sort_locations(locations) or FALLBACK_LOCATIONS



@app.get("/api/me")
def me(user: CurrentUser):
    return user


@app.get("/api/locations", response_model=LocationListResponse)
def get_locations():
    return {"success": True, "locations": active_locations()}

@app.get("/api/locations/search", response_model=LocationListResponse)
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

@app.post("/api/locations", response_model=LocationResponse, status_code=201)
def create_location(body: LocationCreate, admin: AdminUser):
    location_id = re.sub(r"\s+", "-", (body.id or body.name).strip().lower())
    ref = db.collection(COLLECTION).document(location_id)

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

@app.post("/api/locations/preview", response_model=LocationResponse)
def preview_location(body: LocationCreate):
    location_id = re.sub(r"\s+", "-", (body.id or body.name).strip().lower())
    location = Location(id=location_id, **body.model_dump(exclude={"id"}))
    return {"success": True, "location": location}
