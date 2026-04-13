# 🚌 BusTrack MQ — Frontend Next.js

Interface web de suivi en temps réel des bus en Martinique.  
Stack : **Next.js 14 + Tailwind CSS + Leaflet.js + WebSocket**

---

## 🚀 Lancer en local

```bash
cp .env.local.example .env.local
npm install
npm run dev
```

Ouvrir : http://localhost:3000  
*(L'API backend doit tourner sur http://localhost:8000)*

---

## 📄 Pages

| Route | Description |
|-------|-------------|
| `/` | Carte temps réel avec sidebar lignes/bus |
| `/lignes` | Liste de toutes les lignes |
| `/lignes/[id]` | Détail d'une ligne (arrêts + bus) |
| `/bus/[id]` | Détail d'un bus (position, statut, progression) |

---

## 🎨 Thème

Dark mode / Light mode avec toggle dans la navbar.  
Préférence système respectée au premier chargement.

---

## 🚢 Déploiement (Vercel)

1. Importer le dépôt dans Vercel
2. Configurer les variables d'environnement :
   - `NEXT_PUBLIC_API_URL` → URL Railway de l'API (ex: `https://bustrack-mq.up.railway.app`)
   - `NEXT_PUBLIC_WS_URL` → URL WS Railway (ex: `wss://bustrack-mq.up.railway.app`)
3. Deploy automatique sur chaque push `main`
