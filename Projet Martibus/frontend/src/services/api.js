/**
 * services/api.js
 * Fonctions d'appel à l'API REST backend.
 */

const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001/api';

/**
 * Récupère tous les bus actifs depuis l'API.
 * @returns {Promise<Array>}
 */
export async function fetchBus() {
  const res = await fetch(`${BASE_URL}/bus`);
  if (!res.ok) throw new Error(`Erreur API /bus : ${res.status}`);
  const json = await res.json();
  return json.data;
}

/**
 * Récupère tous les arrêts depuis l'API.
 * @returns {Promise<Array>}
 */
export async function fetchArrets() {
  const res = await fetch(`${BASE_URL}/arrets`);
  if (!res.ok) throw new Error(`Erreur API /arrets : ${res.status}`);
  const json = await res.json();
  return json.data;
}

/**
 * Récupère toutes les lignes avec leurs arrêts.
 * @returns {Promise<Array>}
 */
export async function fetchLignes() {
  const res = await fetch(`${BASE_URL}/lignes`);
  if (!res.ok) throw new Error(`Erreur API /lignes : ${res.status}`);
  const json = await res.json();
  return json.data;
}

/**
 * Récupère le détail d'une ligne (avec ses arrêts dans l'ordre).
 * @param {number} id
 * @returns {Promise<Object>}
 */
export async function fetchLigneDetail(id) {
  const res = await fetch(`${BASE_URL}/lignes/${id}`);
  if (!res.ok) throw new Error(`Erreur API /lignes/${id} : ${res.status}`);
  const json = await res.json();
  return json.data;
}
