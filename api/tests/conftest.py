"""
Configuration pytest — tests unitaires avec SQLite en mémoire.

Les tests pg_trgm (/search, /translate) sont marqués @pytest.mark.skip
car func.similarity() n'existe pas en SQLite.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Forcer la clé API avant tout import de l'app
import os
os.environ.setdefault("API_KEY", "changeme")

from app.database import Base, get_db  # noqa: E402
from app.main import app               # noqa: E402


SQLITE_URL = "sqlite:///./test_langmatinitje.db"

engine_test = create_engine(
    SQLITE_URL,
    connect_args={"check_same_thread": False},
)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    """Crée les tables SQLite pour toute la session de tests."""
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def db_session(create_tables):
    """Fournit une session DB de test avec rollback automatique."""
    connection = engine_test.connect()
    transaction = connection.begin()
    session = TestingSession(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """Client HTTP avec la DB de test injectée."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# Clé API utilisée dans les tests authentifiés
API_KEY = "changeme"
