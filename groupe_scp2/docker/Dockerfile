FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Créer les dossiers de données
RUN mkdir -p data/raw data/processed data/cache

ENTRYPOINT ["python", "main.py"]
