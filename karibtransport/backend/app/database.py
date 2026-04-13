from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./karibtransport.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def seed_data():
    """Insert initial data only if the database is empty (idempotent)."""
    # Import here to avoid circular imports at module load time
    from .models import Line, Stop, Vehicle

    db = SessionLocal()
    try:
        if db.query(Line).count() > 0:
            return  # Already seeded

        # ── 5 lignes de bus martiniquaises ────────────────────────────────────
        lines_data = [
            {"code": "T1", "name": "Transversale 1 — Fort-de-France / Le Lamentin", "color": "#ef4444"},
            {"code": "N1", "name": "Nord 1 — Fort-de-France / Saint-Pierre",        "color": "#3b82f6"},
            {"code": "S3", "name": "Sud 3 — Fort-de-France / Le Marin",             "color": "#22c55e"},
            {"code": "C2", "name": "Côtière 2 — Le Robert / La Trinité",            "color": "#f59e0b"},
            {"code": "E1", "name": "Est 1 — Fort-de-France / Le François",          "color": "#8b5cf6"},
        ]
        lines = [Line(**d) for d in lines_data]
        db.add_all(lines)
        db.flush()  # assign IDs before referencing them

        # ── 8 arrêts réels de Martinique ──────────────────────────────────────
        stops_data = [
            {"name": "Fort-de-France — Pointe Simon",    "latitude": 14.6037, "longitude": -61.0724,
             "description": "Terminal principal, bord de mer"},
            {"name": "Le Lamentin — Centre Commercial",  "latitude": 14.6116, "longitude": -60.9964,
             "description": "Carrefour Lamentin, zone commerciale"},
            {"name": "Saint-Pierre — Musée du Vulcan",   "latitude": 14.7361, "longitude": -61.1775,
             "description": "Ancien chef-lieu, côte ouest"},
            {"name": "Le Marin — Marina",                "latitude": 14.4703, "longitude": -60.8747,
             "description": "Port de plaisance du Marin"},
            {"name": "La Trinité — Promenade",           "latitude": 14.7383, "longitude": -60.9628,
             "description": "Front de mer de La Trinité"},
            {"name": "Le Robert — Bord de Mer",          "latitude": 14.6800, "longitude": -60.9270,
             "description": "Centre-ville du Robert"},
            {"name": "Le François — Place de l'Église",  "latitude": 14.6219, "longitude": -60.8938,
             "description": "Place centrale du François"},
            {"name": "Schœlcher — Université",           "latitude": 14.6198, "longitude": -61.1020,
             "description": "Campus Universitaire des Antilles"},
        ]
        db.add_all([Stop(**d) for d in stops_data])

        # ── 5 véhicules (un par ligne) — positionnés sur Fort-de-France ───────
        vehicles_data = [
            {"license_plate": "MA-101-FDF", "vehicle_type": "bus",     "capacity": 40,
             "latitude": 14.6037, "longitude": -61.0724, "line_id": lines[0].id},
            {"license_plate": "MA-201-FDF", "vehicle_type": "bus",     "capacity": 35,
             "latitude": 14.6045, "longitude": -61.0730, "line_id": lines[1].id},
            {"license_plate": "MA-301-FDF", "vehicle_type": "bus",     "capacity": 40,
             "latitude": 14.6030, "longitude": -61.0718, "line_id": lines[2].id},
            {"license_plate": "MA-401-FDF", "vehicle_type": "minibus", "capacity": 15,
             "latitude": 14.6041, "longitude": -61.0735, "line_id": lines[3].id},
            {"license_plate": "MA-501-FDF", "vehicle_type": "minibus", "capacity": 15,
             "latitude": 14.6050, "longitude": -61.0710, "line_id": lines[4].id},
        ]
        db.add_all([Vehicle(**d) for d in vehicles_data])

        db.commit()
        print("[seed] Database seeded with 5 lines, 8 stops, 5 vehicles.")
    except Exception as exc:
        db.rollback()
        print(f"[seed] Error during seeding: {exc}")
        raise
    finally:
        db.close()
