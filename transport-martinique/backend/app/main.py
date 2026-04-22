from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
 
from .routes import stops as stops_router

app = FastAPI(title="Transport Martinique API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(stops_router.router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok"}

## The GET /api/stops route is handled in routes/stops.py and proxies the GTFS stops.txt as JSON.
