# CM8 - DevOps et CI/CD (Partie 1)
## Docker, Pipelines et Déploiement

---

## Introduction

### Rappel des cours précédents

**CM1-CM3 :** Fondamentaux POO  
**CM4-CM6 :** Patterns, SOLID, Architecture  
**CM7 :** Tests et Qualité de Code  

**Aujourd'hui - CM8 :**
- **DevOps** : Culture et pratiques
- **Docker** : Conteneurisation
- **CI/CD** : Intégration et déploiement continus
- **Pipelines** : GitHub Actions, GitLab CI
- **Déploiement** : Production-ready

---

## 1. Qu'est-ce que DevOps ?

### 1.1 Définition

> **DevOps = Development + Operations**
>
> **Culture et pratiques qui rapprochent le développement et les opérations pour livrer plus rapidement et plus fiablement.**

### 1.2 Avant DevOps (❌)

```
DÉVELOPPEURS          |  OPÉRATIONS
                      |
Écrivent du code  →   |  "Ça marche sur ma machine!"
                      |
Passent en prod   →   |  💥 CRASH
                      |
Blâment les ops   ←   |  Blâment les devs
                      |
      ↓ LENT ↓        |      ↓ INSTABLE ↓
```

### 1.3 Avec DevOps (✅)

```
ÉQUIPE DEVOPS (collaboration)

Développeurs + Opérations travaillent ensemble

Automatisation   →  Tests automatiques
                →  Déploiement automatique
                →  Monitoring

      ↓ RAPIDE ↓  et  ↓ STABLE ↓
```

### 1.4 Principes DevOps

**1. Automatisation**
- Tests automatiques
- Déploiement automatique
- Infrastructure as Code

**2. Collaboration**
- Dev et Ops travaillent ensemble
- Communication constante
- Responsabilité partagée

**3. Mesure**
- Monitoring en production
- Métriques de performance
- Logs centralisés

**4. Amélioration Continue**
- Feedback loops
- Post-mortems sans blâme
- Apprentissage continu

---

## 2. Docker : Conteneurisation

### 2.1 Qu'est-ce qu'un Conteneur ?

> **Un conteneur est un package léger qui contient tout ce dont une application a besoin pour fonctionner.**

**Différence VM vs Conteneur :**

```
MACHINE VIRTUELLE (VM)              CONTENEUR
┌─────────────────────┐            ┌──────────┐
│    Application      │            │   App    │
├─────────────────────┤            ├──────────┤
│     Librairies      │            │   Libs   │
├─────────────────────┤            ├──────────┤
│    OS Invité        │            │  Docker  │
├─────────────────────┤            ├──────────┤
│    Hypervisor       │            │  OS Host │
├─────────────────────┤            └──────────┘
│      OS Host        │
└─────────────────────┘

Lourd (~GB)                        Léger (~MB)
Lent à démarrer (minutes)          Rapide (secondes)
```

### 2.2 Installation Docker

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Vérification
docker --version
docker run hello-world
```

### 2.3 Premier Dockerfile

**Dockerfile :**
```dockerfile
# Image de base
FROM python:3.11-slim

# Métadonnées
LABEL maintainer="roor@ua.fr"
LABEL description="Application Flask de gestion d'étudiants"

# Répertoire de travail
WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY src/ ./src/

# Port exposé
EXPOSE 5000

# Variable d'environnement
ENV FLASK_APP=src/app.py
ENV FLASK_ENV=production

# Commande de démarrage
CMD ["flask", "run", "--host=0.0.0.0"]
```

**requirements.txt :**
```
flask==3.0.0
pytest==7.4.3
```

**Construction et exécution :**
```bash
# Construire l'image
docker build -t student-api:v1.0 .

# Exécuter le conteneur
docker run -d -p 5000:5000 --name student-api student-api:v1.0

# Vérifier
curl http://localhost:5000

# Voir les logs
docker logs student-api

# Arrêter
docker stop student-api

# Supprimer
docker rm student-api
```

### 2.4 Docker Compose

**docker-compose.yml :**
```yaml
version: '3.8'

services:
  # Application Flask
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/students
      - FLASK_ENV=development
    depends_on:
      - db
    volumes:
      - ./src:/app/src  # Hot reload en dev
    networks:
      - app-network

  # Base de données PostgreSQL
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=students
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

  # pgAdmin pour l'administration
  pgadmin:
    image: dpage/pgadmin4:latest
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@ua.fr
      - PGADMIN_DEFAULT_PASSWORD=admin
    ports:
      - "8080:80"
    depends_on:
      - db
    networks:
      - app-network

volumes:
  postgres-data:

networks:
  app-network:
    driver: bridge
```

**Utilisation :**
```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f app

# Arrêter
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v
```

### 2.5 Multi-stage Build (Optimisation)

**Dockerfile optimisé :**
```dockerfile
# ============================================================================
# ÉTAPE 1 : BUILD
# ============================================================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Installer les dépendances de build
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# ============================================================================
# ÉTAPE 2 : RUNTIME
# ============================================================================
FROM python:3.11-slim

WORKDIR /app

# Copier uniquement les dépendances installées (pas gcc ni build tools)
COPY --from=builder /root/.local /root/.local

# Copier le code source
COPY src/ ./src/

# S'assurer que les scripts Python sont dans PATH
ENV PATH=/root/.local/bin:$PATH

# Utilisateur non-root pour la sécurité
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
```

**Avantages :**
- ✅ Image finale plus légère (pas de build tools)
- ✅ Plus sécurisée (pas de gcc en production)
- ✅ Build rapide (cache des layers)

---

## 3. CI/CD avec GitHub Actions

### 3.1 Pipeline de Base

**.github/workflows/ci.yml :**
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  PYTHON_VERSION: '3.11'
  DOCKER_IMAGE: student-api

jobs:
  # =========================================================================
  # JOB 1 : TESTS
  # =========================================================================
  test:
    name: Tests unitaires et intégration
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test_db
        run: |
          pytest --cov=src --cov-report=xml --cov-report=term -v
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: true

  # =========================================================================
  # JOB 2 : QUALITÉ DE CODE
  # =========================================================================
  quality:
    name: Qualité de code
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install linters
        run: |
          pip install black flake8 mypy pylint
      
      - name: Check formatting with Black
        run: black --check src/ tests/
      
      - name: Lint with Flake8
        run: flake8 src/ tests/ --max-line-length=100
      
      - name: Type check with MyPy
        run: mypy src/
      
      - name: Lint with Pylint
        run: pylint src/ --max-line-length=100

  # =========================================================================
  # JOB 3 : BUILD DOCKER
  # =========================================================================
  build:
    name: Build Docker image
    runs-on: ubuntu-latest
    needs: [test, quality]  # Attend que test et quality passent
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Build Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: false
          tags: ${{ env.DOCKER_IMAGE }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
      
      - name: Test Docker image
        run: |
          docker run --rm ${{ env.DOCKER_IMAGE }}:${{ github.sha }} \
            python -c "import flask; print('OK')"

  # =========================================================================
  # JOB 4 : DEPLOY (seulement sur main)
  # =========================================================================
  deploy:
    name: Deploy to production
    runs-on: ubuntu-latest
    needs: [build]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/${{ env.DOCKER_IMAGE }}:latest
            ${{ secrets.DOCKER_USERNAME }}/${{ env.DOCKER_IMAGE }}:${{ github.sha }}
      
      - name: Deploy notification
        run: |
          echo "🚀 Deployed version ${{ github.sha }} to production"
```

### 3.2 Pipeline avec GitLab CI

**.gitlab-ci.yml :**
```yaml
stages:
  - test
  - build
  - deploy

variables:
  PYTHON_VERSION: "3.11"
  DOCKER_IMAGE: "registry.gitlab.com/$CI_PROJECT_PATH"

# ============================================================================
# STAGE: TEST
# ============================================================================
test:unit:
  stage: test
  image: python:${PYTHON_VERSION}
  
  services:
    - postgres:15
  
  variables:
    POSTGRES_DB: test_db
    POSTGRES_USER: test
    POSTGRES_PASSWORD: test
    DATABASE_URL: postgresql://test:test@postgres:5432/test_db
  
  before_script:
    - pip install -r requirements.txt
    - pip install pytest pytest-cov
  
  script:
    - pytest --cov=src --cov-report=term --cov-report=html
  
  coverage: '/TOTAL.*\s+(\d+%)$/'
  
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
    paths:
      - htmlcov/
    expire_in: 1 week

lint:
  stage: test
  image: python:${PYTHON_VERSION}
  
  before_script:
    - pip install black flake8 mypy
  
  script:
    - black --check src/ tests/
    - flake8 src/ tests/
    - mypy src/

# ============================================================================
# STAGE: BUILD
# ============================================================================
build:image:
  stage: build
  image: docker:latest
  
  services:
    - docker:dind
  
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  
  script:
    - docker build -t $DOCKER_IMAGE:$CI_COMMIT_SHA .
    - docker tag $DOCKER_IMAGE:$CI_COMMIT_SHA $DOCKER_IMAGE:latest
    - docker push $DOCKER_IMAGE:$CI_COMMIT_SHA
    - docker push $DOCKER_IMAGE:latest
  
  only:
    - main
    - develop

# ============================================================================
# STAGE: DEPLOY
# ============================================================================
deploy:production:
  stage: deploy
  image: alpine:latest
  
  before_script:
    - apk add --no-cache openssh-client
    - eval $(ssh-agent -s)
    - echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
    - mkdir -p ~/.ssh
    - chmod 700 ~/.ssh
  
  script:
    - ssh user@production-server "
        docker pull $DOCKER_IMAGE:$CI_COMMIT_SHA &&
        docker stop student-api || true &&
        docker rm student-api || true &&
        docker run -d --name student-api -p 5000:5000 $DOCKER_IMAGE:$CI_COMMIT_SHA
      "
  
  environment:
    name: production
    url: https://api.students.ua.fr
  
  only:
    - main
  
  when: manual  # Déploiement manuel
```

---

## 4. Déploiement en Production

### 4.1 Configuration pour Production

**config.py :**
```python
import os
from typing import Optional


class Config:
    """Configuration de base"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = False
    TESTING = False
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')


class DevelopmentConfig(Config):
    """Configuration développement"""
    DEBUG = True
    DATABASE_URL = 'sqlite:///dev.db'


class TestingConfig(Config):
    """Configuration tests"""
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'


class ProductionConfig(Config):
    """Configuration production"""
    DEBUG = False
    
    # Sécurité
    SECRET_KEY = os.getenv('SECRET_KEY')  # DOIT être défini
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in production")
    
    # Database avec pool de connexions
    DATABASE_URL = os.getenv('DATABASE_URL')
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 20
    
    # Logging
    LOG_LEVEL = 'WARNING'


# Factory pour sélectionner la config
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(env: Optional[str] = None) -> Config:
    """Retourne la configuration selon l'environnement"""
    env = env or os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])()
```

### 4.2 Dockerfile Production

**Dockerfile.prod :**
```dockerfile
FROM python:3.11-slim AS builder

WORKDIR /app

# Installer les dépendances de build
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


FROM python:3.11-slim

WORKDIR /app

# Copier les dépendances
COPY --from=builder /root/.local /root/.local

# Copier le code
COPY src/ ./src/
COPY migrations/ ./migrations/
COPY config.py .

# Créer un utilisateur non-root
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

ENV PATH=/root/.local/bin:$PATH
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')"

# Utiliser gunicorn pour la production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "src.app:app"]
```

**requirements.txt (production) :**
```
flask==3.0.0
flask-sqlalchemy==3.1.1
psycopg2-binary==2.9.9
gunicorn==21.2.0
python-dotenv==1.0.0
```

### 4.3 Docker Compose Production

**docker-compose.prod.yml :**
```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.prod
    restart: always
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://user:${DB_PASSWORD}@db:5432/students
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      db:
        condition: service_healthy
    networks:
      - app-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.app.rule=Host(`api.students.ua.fr`)"
      - "traefik.http.routers.app.tls.certresolver=letsencrypt"

  db:
    image: postgres:15-alpine
    restart: always
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=students
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./backups:/backups
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

  traefik:
    image: traefik:v2.10
    restart: always
    command:
      - "--api.dashboard=true"
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.email=admin@ua.fr"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - letsencrypt:/letsencrypt
    networks:
      - app-network

volumes:
  postgres-data:
  letsencrypt:

networks:
  app-network:
    driver: bridge
```

---

## Résumé Partie 1

### Ce que nous avons vu

✅ **DevOps** : Culture et principes  
✅ **Docker** : Conteneurisation et Dockerfile  
✅ **Docker Compose** : Orchestration multi-conteneurs  
✅ **CI/CD** : Pipelines GitHub Actions et GitLab CI  
✅ **Déploiement** : Configuration production  
✅ **Multi-stage builds** : Optimisation des images  

### Concepts clés

- **Conteneurisation** = Package portable
- **CI/CD** = Automatisation du build au déploiement
- **Infrastructure as Code** = Configuration versionnée
- **Environnements** = dev, test, prod séparés

### Dans la Partie 2, nous verrons :

- Monitoring et Logging
- Backup et Disaster Recovery
- Sécurité en production
- Scaling et Load Balancing
- Cas pratique complet

---

*Suite dans la Partie 2...*