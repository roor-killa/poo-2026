import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from db.database import init_db
from simulation.engine import simulateur
from api.routes import lignes, bus, websocket, notifications

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie : démarrage et arrêt."""
    # Démarrage
    logger.info("Initialisation de la base de données...")
    await init_db()

    logger.info("Démarrage du moteur de simulation GPS...")
    sim_task = asyncio.create_task(simulateur.demarrer())

    yield  # l'application tourne ici

    # Arrêt
    logger.info("Arrêt du moteur de simulation...")
    simulateur.arreter()
    sim_task.cancel()
    try:
        await sim_task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title="BusTrack MQ API",
    description="API de suivi en temps réel des bus en Martinique",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ────────────────────────────────────────────────────────────────────
app.include_router(lignes.router)
app.include_router(bus.router)
app.include_router(websocket.router)
app.include_router(notifications.router)


@app.get("/health", tags=["Monitoring"])
async def health():
    """Endpoint de santé pour le CI/CD et le monitoring."""
    return {
        "status": "ok",
        "version": "1.0.0",
        "bus_actifs": len(simulateur.bus),
        "clients_ws": len(simulateur.ws_clients),
    }


@app.get("/", tags=["Root"])
async def root():
    return {"message": "BusTrack MQ API — consultez /docs pour la documentation"}
