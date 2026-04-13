from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base, seed_data
from .routers import vehicles, stops

# Create all tables then seed initial data
Base.metadata.create_all(bind=engine)
seed_data()

app = FastAPI(
    title="KaribTransport API",
    description="Real-time public transport tracking for the Caribbean",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vehicles.router)
app.include_router(stops.router)


@app.get("/")
def root():
    return {"message": "KaribTransport API is running", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}
