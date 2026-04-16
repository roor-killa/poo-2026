STOPS = [
    {
        "id": "s-fdf-savane",
        "name": "Fort-de-France - La Savane",
        "lat": 14.6031245,
        "lng": -61.0674007,
        "next_eta_min": 4,
    },
    {
        "id": "s-fdf-pointe-simon",
        "name": "Fort-de-France - Ponton de la Pointe Simon",
        "lat": 14.602085,
        "lng": -61.070788,
        "next_eta_min": 7,
    },
    {
        "id": "s-lelamentin-mairie",
        "name": "Le Lamentin - Four A Chaux",
        "lat": 14.61081173,
        "lng": -61.00162718,
        "next_eta_min": 9,
    },
    {
        "id": "s-schoelcher-madiana",
        "name": "Schoelcher - Madiana",
        "lat": 14.60969637,
        "lng": -61.0973174,
        "next_eta_min": 5,
    },
    {
        "id": "s-trinite-centre",
        "name": "La Trinite - Gare Routiere",
        "lat": 14.73789204,
        "lng": -60.96201281,
        "next_eta_min": 12,
    },
    {
        "id": "s-robert-centre",
        "name": "Le Robert - Gare Courbaril",
        "lat": 14.67575302,
        "lng": -60.94106295,
        "next_eta_min": 16,
    },
    {
        "id": "s-trois-ilets-bourg",
        "name": "Les Trois-Ilets - Bourg",
        "lat": 14.540437,
        "lng": -61.035908,
        "next_eta_min": 8,
    },
    {
        "id": "s-case-pilote-bourg",
        "name": "Case-Pilote - Bourg",
        "lat": 14.64273049,
        "lng": -61.13682487,
        "next_eta_min": 14,
    },
]

LINES = [
    {
        "id": "line-a",
        "code": "A",
        "name": "TCSP Centre",
        "direction": "Fort-de-France -> Le Lamentin",
        "stop_ids": [
            "s-fdf-savane",
            "s-fdf-pointe-simon",
            "s-lelamentin-mairie",
        ],
    },
    {
        "id": "line-a-retour",
        "code": "A",
        "name": "TCSP Centre",
        "direction": "Le Lamentin -> Fort-de-France",
        "stop_ids": [
            "s-lelamentin-mairie",
            "s-fdf-pointe-simon",
            "s-fdf-savane",
        ],
    },
    {
        "id": "line-m1",
        "code": "M1",
        "name": "Navette Maritime",
        "direction": "Fort-de-France -> Les Trois-Ilets",
        "stop_ids": [
            "s-fdf-pointe-simon",
            "s-trois-ilets-bourg",
        ],
    },
    {
        "id": "line-m2",
        "code": "M2",
        "name": "Navette Maritime",
        "direction": "Fort-de-France -> Case-Pilote",
        "stop_ids": [
            "s-fdf-pointe-simon",
            "s-case-pilote-bourg",
        ],
    },
    {
        "id": "line-e2",
        "code": "E2",
        "name": "Nord Atlantique",
        "direction": "Le Robert -> La Trinite",
        "stop_ids": [
            "s-robert-centre",
            "s-trinite-centre",
        ],
    },
    {
        "id": "line-w1",
        "code": "W1",
        "name": "Cote Caraibe",
        "direction": "Schoelcher -> Fort-de-France",
        "stop_ids": [
            "s-schoelcher-madiana",
            "s-fdf-savane",
        ],
    },
]
