FROM python:3.12-slim

WORKDIR /project

# Installation des dependances Python du backend FastAPI et des scrapers.
COPY backend/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copie du code applicatif dans l'image Docker.
COPY backend ./backend
COPY scrapers ./scrapers

# Dossier ou les exports JSON seront crees dans le conteneur.
RUN mkdir -p data

# Lance l'API FastAPI avec uvicorn sur le port interne 8000.
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
