import json
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "locations.seed.json"
LOCATIONS = json.loads(DATA_FILE.read_text())

app = FastAPI(title="RentNHost API")

@app.get("/", response_class=PlainTextResponse)
def root():
    return "Car Rental"

# Health check endpoint
@app.get("/health")
def health():
    return {"ok": True}

def active_locations() -> list[dict]:
    active = [loc for loc in LOCATIONS if loc.get("isActive", True)]
    active.sort(key=lambda loc: (loc.get("sortOrder", 99), loc["name"]))
    return active


@app.get("/api/locations")
def get_locations():
    return {"success": True, "locations": active_locations()}

@app.get("/api/locations/search")
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

@app.get("/api/locations/{location_id}")
def get_location(location_id: str):
    key = location_id.lower()
    for loc in LOCATIONS:
        if loc["id"].lower() == key or loc["name"].lower() == key:
            return {"success": True, "location": loc}
    raise HTTPException(status_code=404, detail="Location not found")
