export interface Arret {
  id: number;
  nom: string;
  latitude: number;
  longitude: number;
  ordre: number;
}

export interface Ligne {
  id: number;
  nom: string;
  couleur: string;
  description: string;
  nombre_arrets?: number;
  arrets?: Arret[];
  bus?: BusPosition[];
}

export interface BusPosition {
  id: number;
  nom: string;
  ligne_id: number;
  ligne_nom: string;
  ligne_couleur: string;
  latitude: number;
  longitude: number;
  vitesse: number;
  statut: "en_service" | "a_larret" | "hors_service";
  arret_courant: string | null;
  prochain_arret: string | null;
}
