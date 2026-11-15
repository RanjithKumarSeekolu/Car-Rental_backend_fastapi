# RentNHost API (FastAPI)

Backend for the RentNHost car rental app, built with FastAPI.
This is a rewrite of the original Node.js/Express backend, being migrated step by step.

## Requirements

- Python 3.10+

## Setup

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run (development)

```bash
fastapi dev app/main.py
```

The API runs at http://127.0.0.1:8000, with auto-reload on file changes.

## API docs

FastAPI generates interactive docs automatically:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/api/locations` | List active locations |
| GET | `/api/locations/search?q=&limit=` | Search locations by name, state or id |
| GET | `/api/locations/{location_id}` | Get one location by id or name |

## Project structure

```
app/
├── main.py                    # FastAPI app and routes
└── data/
    └── locations.seed.json    # Location seed data
```

## Migration status

- [x] Project setup
- [x] Locations (read-only, from seed file)
- [ ] Firestore connection
- [ ] Auth
- [ ] Users, cars, bookings, payments, dashboard, contact