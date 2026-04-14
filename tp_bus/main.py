from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import asyncio
import json


from database import engine, SessionLocal
import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bus Martinique Live - MVP")


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Bus Martinique Live</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        
        <style>
            body { margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            #map { height: 100vh; width: 100vw; }
            .bus-info { 
                position: absolute; top: 20px; right: 20px; 
                background: white; padding: 15px; border-radius: 12px; 
                z-index: 1000; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                min-width: 220px;
            }
            h2 { margin: 0 0 10px 0; color: #1a73e8; font-size: 18px; border-bottom: 2px solid #f0f2f5; padding-bottom: 5px; }
            .status { color: #2ecc71; font-weight: bold; }
            .coords { font-family: monospace; color: #666; font-size: 0.9em; }
        </style>
    </head>
    <body>
        <div class="bus-info">
            <h2>🚌 Mozaïk Live</h2>
            <div id="details">
                Statut : <span class="status">Connexion au flux...</span><br>
                <span style="font-size: 0.8em; color: gray;">En attente de données GPS</span>
            </div>
        </div>
        
        <div id="map"></div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        
        <script>
            // 1. Initialisation de la carte sur Fort-de-France
            var map = L.map('map').setView([14.6161, -61.0588], 14);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(map);

            // 2. Icône de bus personnalisée
            var busIcon = L.icon({
                iconUrl: 'https://cdn-icons-png.flaticon.com/512/3448/3448339.png',
                iconSize: [45, 45],
                iconAnchor: [22, 22],
                popupAnchor: [0, -20]
            });

            // 3. Création du marqueur
            var busMarker = L.marker([14.6161, -61.0588], {icon: busIcon}).addTo(map)
                .bindPopup("<b>Bus Ligne 1</b><br>En direction du Centre");

            // 4. Connexion WebSocket
            var ws = new WebSocket("ws://" + window.location.host + "/ws/bus/Ligne1");
            
            ws.onmessage = function(event) {
                var data = JSON.parse(event.data);
                var latlng = [data.lat, data.lon];
                
                // On déplace le marqueur et on centre la carte
                busMarker.setLatLng(latlng);
                map.panTo(latlng);
                
                // Mise à jour de la boîte d'infos
                document.getElementById('details').innerHTML = 
                    "Statut : <span class='status'>En mouvement</span><br>" +
                    "<b>ID Bus :</b> " + data.bus_id + "<br>" +
                    "<span class='coords'>Lat : " + data.lat.toFixed(6) + "<br>" +
                    "Lon : " + data.lon.toFixed(6) + "</span>";
            };

            ws.onerror = function() {
                document.getElementById('details').innerHTML = "<b style='color:red;'>Erreur WebSocket</b>";
            };
        </script>
    </body>
</html>
"""

# --- Logique Métier (POO) ---
class Bus:
    def __init__(self, bus_id: str, lat: float, lon: float):
        self.bus_id = bus_id
        self.lat = lat
        self.lon = lon

    def move(self):
        # Simulation d'un trajet (on déplace légèrement le bus)
        self.lat += 0.00018
        self.lon -= 0.00012
        
    def save_to_db(self, db: Session):
        db_pos = models.BusPosition(
            bus_id=self.bus_id, 
            latitude=self.lat, 
            longitude=self.lon
        )
        db.add(db_pos)
        db.commit()

# --- Points d'entrée (Routes) ---

@app.get("/")
async def get_home():
    return HTMLResponse(html)

@app.get("/check-db")
def get_db_history():
    """Vérifie les 10 dernières positions enregistrées"""
    db = SessionLocal()
    history = db.query(models.BusPosition).order_by(models.BusPosition.id.desc()).limit(10).all()
    db.close()
    return history

@app.websocket("/ws/bus/{bus_id}")
async def websocket_bus_feed(websocket: WebSocket, bus_id: str):
    await websocket.accept()
    # Point de départ (Etang Z'abricot)
    mon_bus = Bus(bus_id=bus_id, lat=14.6050, lon=-61.0730)
    db = SessionLocal()
    
    try:
        while True:
            mon_bus.move()
            mon_bus.save_to_db(db)
            
            await websocket.send_text(json.dumps({
                "bus_id": mon_bus.bus_id, 
                "lat": mon_bus.lat, 
                "lon": mon_bus.lon
            }))
            
            await asyncio.sleep(2) # Mise à jour toutes les 2 sec
            
    except WebSocketDisconnect:
        db.close()