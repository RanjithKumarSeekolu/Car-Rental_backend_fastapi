from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI(title="RentNHost API")

@app.get("/", response_class=PlainTextResponse)
def root():
    return "Car Rental"

# Health check endpoint
@app.get("/health")
def health():
    return {"ok": True}