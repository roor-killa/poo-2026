# Cahier des charges - RTG Suivi Temps Reel (MVP)

## 1. Analyse

### 1.1 Contexte
La RTG souhaite superviser sa flotte de bus en temps reel, remonter les positions GPS, diffuser les donnees aux operateurs et fournir des indicateurs d'exploitation.

### 1.2 Problemes a resoudre
- Visibilite limitee sur la flotte en circulation.
- Difficultes a informer rapidement en cas d'incident.
- Faible centralisation des KPI d'exploitation.

### 1.3 Objectifs
- Centraliser les positions bus via API/WebSocket.
- Visualiser les lignes, les bus, les KPI et les alertes sur un dashboard.
- Exposer un socle extensible vers une architecture production complete.

### 1.4 Perimetre MVP
- Backend Python FastAPI.
- Frontend dashboard web.
- Stockage en memoire (seed de donnees).
- WebSocket agent et live.
- Docker pour execution standardisee.

### 1.5 Hors perimetre MVP
- Authentification OAuth2/JWT robuste.
- Persistance PostgreSQL/Redis en production.
- IAM avance, observabilite complete, autoscaling K8s.

## 2. Conception

### 2.1 Principes
- API first.
- Separation par couches: modeles, services, store, presentation.
- Evolutivite vers stockage persistant.

### 2.2 Cas d'usage
- Operateur consulte bus/lignes/KPI.
- Agent embarque pousse des positions GPS.
- Operateur cree une alerte incident.
- Operateur interroge l'assistant IA stub.

## 3. IHM

### 3.1 Ecran principal
- Header: statut API + action de rafraichissement.
- Bloc KPI: total bus, bus actifs, alertes ouvertes, couverture.
- Tableau bus: etat courant et derniere position.
- Liste lignes: lignes et nombre d'arrets.
- Formulaires: creation d'alerte et requete IA.

### 3.2 Exigences UX
- Temps de rafraichissement automatique 15s.
- Compatibilite desktop/mobile.
- Messages explicites en cas d'erreur API.

## 4. Storyboard

1. L'utilisateur ouvre le dashboard.
2. Le frontend appelle health, buses, lines, kpi.
3. Le backend repond et l'IHM s'actualise.
4. Un agent GPS envoie une position via WebSocket agent.
5. Le backend met a jour l'etat bus et diffuse sur WebSocket live.
6. L'operateur cree une alerte (incident).
7. L'operateur pose une question IA, recoit une reponse structuree.

## 5. Modele de donnees

### 5.1 Entites
- Bus(id, immatriculation, modele, capacite, statut, line_id, depot)
- Line(id, numero, nom, couleur, direction_aller, direction_retour)
- Stop(id, nom, latitude, longitude, line_id)
- PositionGPS(bus_id, lat, lng, speed, heading, ts, sig)
- Alert(id, type, bus_id, message, timestamp, statut)
- KPIResponse(active_buses, total_buses, open_alerts, coverage_ratio)

### 5.2 Relations
- Une ligne contient plusieurs arrets.
- Un bus appartient a une ligne.
- Une position est rattachee a un bus.
- Une alerte reference un bus.

## 6. Architecture (schema)

```mermaid
flowchart LR
  A[Agent GPS Bus] -->|WS /ws/agent/{bus_id}| B[FastAPI Backend]
  B --> C[(InMemory Store MVP)]
  B -->|WS /ws/live/{line_id}| D[Dashboard Frontend]
  D -->|REST /api/v1/*| B
  E[Operateur] --> D
```

## 7. Stack technique

### 7.1 Backend
- Python 3.13
- FastAPI + Uvicorn
- Pydantic v2

### 7.2 Frontend
- HTML/CSS/JS natif (MVP)
- Fetch API

### 7.3 Conteneurisation
- Docker
- Docker Compose (dev)

## 8. Mise en prod / Infra

### 8.1 Cible
- Deploiement Docker sur VM Linux.
- Reverse proxy Nginx (gateway) pour servir frontend + backend sous meme domaine.

### 8.2 Topologie
- service frontend (Nginx static)
- service backend (Uvicorn/FastAPI)
- service gateway (Nginx reverse proxy)

### 8.3 Exigences non-fonctionnelles
- Disponibilite cible MVP: 99%.
- Journalisation applicative standard.
- Redemarrage automatique des conteneurs.

## 9. Plan / ressources / moyens

### 9.1 Plan de realisation
- Phase 1: cadrage et CDC.
- Phase 2: MVP backend + frontend.
- Phase 3: Dockerisation et tests smoke.
- Phase 4: CI/CD et scripts de deploiement.

### 9.2 Ressources humaines
- Product Owner / Sponsor.
- Dev Backend (Python/FastAPI).
- Dev Frontend.
- DevOps pour CI/CD et infra.

### 9.3 Moyens techniques
- Repo GitHub.
- Runner GitHub Actions.
- Registre container (GHCR).
- VM de production Docker.

## 10. Critere d'acceptation
- Le dashboard affiche KPI, bus, lignes.
- Les endpoints REST principaux repondent.
- L'alerte est creable via API.
- Le workflow CI passe sur push/PR.
- Le workflow CD deploie via image versionnee.
