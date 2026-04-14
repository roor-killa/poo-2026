from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# L'URL magique pour que Python trouve PostgreSQL dans Docker
# Format: postgresql://utilisateur:mot_de_passe@nom_du_conteneur:port/nom_de_la_base
SQLALCHEMY_DATABASE_URL = "postgresql://admin:password123@db:5432/bus_martinique_db"

# Création du "moteur" qui gère la connexion
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Création des sessions (pour faire des requêtes)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour nos futurs modèles
Base = declarative_base()