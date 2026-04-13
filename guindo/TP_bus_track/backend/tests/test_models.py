import pytest
import math
from models.arret import Arret
from models.ligne import Ligne
from models.bus import Bus


# ── Fixtures ──────────────────────────────────────────────────────────────────
@pytest.fixture
def arrets():
    return [
        Arret(id=1, nom="Fort-de-France",  latitude=14.6014, longitude=-61.0590, ordre=0),
        Arret(id=2, nom="Dillon",          latitude=14.5960, longitude=-61.0720, ordre=1),
        Arret(id=3, nom="Le Lamentin",     latitude=14.5973, longitude=-60.9941, ordre=2),
    ]

@pytest.fixture
def ligne(arrets):
    return Ligne(id=1, nom="Ligne Test", couleur="#FF0000", description="Test", arrets=arrets)

@pytest.fixture
def bus(ligne):
    return Bus(
        id=1, nom="Bus Test", ligne=ligne,
        latitude=ligne.arrets[0].latitude,
        longitude=ligne.arrets[0].longitude,
    )


# ── Tests Arrêt ───────────────────────────────────────────────────────────────
def test_arret_creation(arrets):
    a = arrets[0]
    assert a.nom == "Fort-de-France"
    assert a.latitude == 14.6014
    assert a.ordre == 0

def test_arret_repr(arrets):
    assert "Fort-de-France" in repr(arrets[0])


# ── Tests Ligne ───────────────────────────────────────────────────────────────
def test_ligne_nombre_arrets(ligne, arrets):
    assert ligne.nombre_arrets() == len(arrets)

def test_ligne_get_arret_valide(ligne):
    arret = ligne.get_arret(0)
    assert arret is not None
    assert arret.nom == "Fort-de-France"

def test_ligne_get_arret_hors_limites(ligne):
    assert ligne.get_arret(-1) is None
    assert ligne.get_arret(99) is None


# ── Tests Bus ─────────────────────────────────────────────────────────────────
def test_bus_creation(bus, ligne):
    assert bus.statut == "en_service"
    assert bus.direction == 1
    assert bus.ligne.id == ligne.id

def test_bus_prochain_arret(bus):
    prochain = bus.prochain_arret()
    assert prochain is not None
    assert prochain.ordre == 1

def test_bus_haversine():
    """Distance Fort-de-France → Le Lamentin ≈ 7 km."""
    dist = Bus._haversine(14.6014, -61.0590, 14.5973, -60.9941)
    assert 5 < dist < 10

def test_bus_avancer_deplacement(bus):
    lat_init = bus.latitude
    lon_init = bus.longitude
    bus.avancer(delta_secondes=30.0)
    # Le bus doit avoir bougé
    assert bus.latitude != lat_init or bus.longitude != lon_init

def test_bus_hors_service_ne_bouge_pas(bus):
    bus.statut = "hors_service"
    lat_init = bus.latitude
    bus.avancer(delta_secondes=60.0)
    assert bus.latitude == lat_init

def test_bus_inversion_direction(bus):
    """Le bus doit inverser sa direction en bout de ligne."""
    bus.arret_courant_idx = len(bus.ligne.arrets) - 1
    bus.direction = 1
    # Forcer l'atteinte du dernier arrêt
    bus._atteindre_prochain()
    assert bus.direction == -1

def test_bus_to_dict(bus):
    d = bus.to_dict()
    assert "latitude" in d
    assert "longitude" in d
    assert d["statut"] == "en_service"

def test_bus_repr(bus):
    assert "Bus Test" in repr(bus)


# ── Tests Simulateur ──────────────────────────────────────────────────────────
def test_simulateur_lignes():
    from simulation.engine import simulateur
    assert len(simulateur.lignes) == 3

def test_simulateur_bus():
    from simulation.engine import simulateur
    assert len(simulateur.bus) == 6  # 2 bus × 3 lignes

def test_simulateur_positions():
    from simulation.engine import simulateur
    positions = simulateur.get_toutes_positions()
    assert len(positions) == 6
    for p in positions:
        assert "latitude" in p
        assert "longitude" in p
        assert "ligne_id" in p
