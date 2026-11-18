from pathlib import Path
import json
from app.core.firebase import db

SEED_FILE = Path(__file__).parent.parent / "data" / "locations.seed.json"
SEED_LOCATIONS = json.loads(SEED_FILE.read_text())
COLLECTION = "locations"

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

