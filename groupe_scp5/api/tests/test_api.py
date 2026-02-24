"""
Tests unitaires — Lang Matinitjé API (SQLite)

Tests pg_trgm marqués @pytest.mark.skip (func.similarity() indisponible en SQLite).
"""
import pytest
from fastapi.testclient import TestClient

from tests.conftest import API_KEY


# ---------------------------------------------------------------------------
# /health
# ---------------------------------------------------------------------------

def test_health(client: TestClient):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "service" in data


# ---------------------------------------------------------------------------
# /api/v1/corpus
# ---------------------------------------------------------------------------

def test_corpus_empty(client: TestClient):
    resp = client.get("/api/v1/corpus")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0
    assert data["results"] == []


# ---------------------------------------------------------------------------
# /api/v1/expressions
# ---------------------------------------------------------------------------

def test_expressions_empty(client: TestClient):
    resp = client.get("/api/v1/expressions")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0
    assert data["results"] == []


# ---------------------------------------------------------------------------
# /api/v1/media
# ---------------------------------------------------------------------------

def test_media_empty(client: TestClient):
    resp = client.get("/api/v1/media")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0
    assert data["results"] == []


def test_media_404(client: TestClient):
    resp = client.get("/api/v1/media/9999")
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# /api/v1/dictionary — erreurs et cas limites
# ---------------------------------------------------------------------------

def test_dictionary_random_empty_db(client: TestClient):
    """Retourne 404 si la table mots est vide."""
    resp = client.get("/api/v1/dictionary/random")
    assert resp.status_code == 404


def test_dictionary_get_404(client: TestClient):
    resp = client.get("/api/v1/dictionary/9999")
    assert resp.status_code == 404
    assert "9999" in resp.json()["detail"]


def test_dictionary_post_no_auth(client: TestClient):
    """POST sans header X-API-Key → 422 (champ manquant)."""
    resp = client.post("/api/v1/dictionary", json={"mot_creole": "lanmou"})
    assert resp.status_code == 422


def test_dictionary_post_wrong_key(client: TestClient):
    """POST avec clé invalide → 401."""
    resp = client.post(
        "/api/v1/dictionary",
        json={"mot_creole": "lanmou"},
        headers={"X-API-Key": "mauvaise-cle"},
    )
    assert resp.status_code == 401


# ---------------------------------------------------------------------------
# /api/v1/dictionary — CRUD complet
# ---------------------------------------------------------------------------

def test_dictionary_crud(client: TestClient):
    """POST → GET → PUT → GET."""
    # Création
    resp = client.post(
        "/api/v1/dictionary",
        json={"mot_creole": "lanmou", "phonetique": "la.mu"},
        headers={"X-API-Key": API_KEY},
    )
    assert resp.status_code == 201
    created = resp.json()
    mot_id = created["id"]
    assert created["mot_creole"] == "lanmou"
    assert created["phonetique"] == "la.mu"

    # Lecture
    resp = client.get(f"/api/v1/dictionary/{mot_id}")
    assert resp.status_code == 200
    assert resp.json()["mot_creole"] == "lanmou"

    # Mise à jour
    resp = client.put(
        f"/api/v1/dictionary/{mot_id}",
        json={"phonetique": "lã.mu"},
        headers={"X-API-Key": API_KEY},
    )
    assert resp.status_code == 200
    assert resp.json()["phonetique"] == "lã.mu"

    # Relecture
    resp = client.get(f"/api/v1/dictionary/{mot_id}")
    assert resp.status_code == 200
    assert resp.json()["phonetique"] == "lã.mu"


def test_dictionary_random_after_insert(client: TestClient):
    """Après insertion, /random retourne 200."""
    # Insérer un mot
    client.post(
        "/api/v1/dictionary",
        json={"mot_creole": "annou"},
        headers={"X-API-Key": API_KEY},
    )
    resp = client.get("/api/v1/dictionary/random")
    assert resp.status_code == 200
    data = resp.json()
    assert "mot_creole" in data
    assert "traductions" in data


# ---------------------------------------------------------------------------
# /api/v1/dictionary/search — SKIP (pg_trgm requis)
# ---------------------------------------------------------------------------

@pytest.mark.skip(reason="func.similarity() nécessite PostgreSQL + pg_trgm")
def test_dictionary_search(client: TestClient):
    resp = client.get("/api/v1/dictionary/search?q=annou")
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# POST /api/v1/translate — SKIP (pg_trgm requis)
# ---------------------------------------------------------------------------

@pytest.mark.skip(reason="func.similarity() nécessite PostgreSQL + pg_trgm")
def test_translate(client: TestClient):
    resp = client.post(
        "/api/v1/translate",
        json={"text": "Allons à la mer", "source": "fr", "target": "crm"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["method"] == "corpus_match"


# ---------------------------------------------------------------------------
# POST /api/v1/chat
# ---------------------------------------------------------------------------

def test_chat_reply(client: TestClient):
    """Vérifie la réponse du stub (déterministe)."""
    msg = "Saw fè ?"
    resp = client.post("/api/v1/chat", json={"message": msg})
    assert resp.status_code == 200
    data = resp.json()
    assert "reply" in data
    assert data["session_id"]
    assert data["model_version"] == "fèfèn-0.1"

    # Déterminisme : même message → même réponse
    resp2 = client.post("/api/v1/chat", json={"message": msg, "session_id": "sess_test"})
    assert resp2.json()["reply"] == data["reply"]
    assert resp2.json()["session_id"] == "sess_test"


def test_chat_reply_index():
    """reply_index = len(message) % 4 → 4 valeurs possibles."""
    from app.routers.chat import _REPLIES
    assert len(_REPLIES) == 4


# ---------------------------------------------------------------------------
# GET /api/v1/me — auth
# ---------------------------------------------------------------------------

def test_me_no_auth(client: TestClient):
    resp = client.get("/api/v1/me")
    assert resp.status_code == 422  # X-API-Key manquant


def test_me_wrong_key(client: TestClient):
    resp = client.get("/api/v1/me", headers={"X-API-Key": "faux"})
    assert resp.status_code == 401


def test_me_empty_db(client: TestClient):
    """Retourne 404 si aucun contributeur en base."""
    resp = client.get("/api/v1/me", headers={"X-API-Key": API_KEY})
    assert resp.status_code == 404
