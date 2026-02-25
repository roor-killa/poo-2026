/**
 * Clients API — Lang Matinitjé
 *
 * - Lecture dictionnaire/corpus/chat → FastAPI (sans auth)
 * - Auth + Contributions → Laravel (token Sanctum Bearer)
 */

const FASTAPI = process.env.NEXT_PUBLIC_FASTAPI_URL ?? "http://localhost:8000/api/v1";
const LARAVEL = process.env.NEXT_PUBLIC_LARAVEL_URL ?? "http://localhost:8001/api";

// ============================================================
// Types FastAPI
// ============================================================

export interface Mot {
  id:             number;
  mot_creole:     string;
  phonetique:     string | null;
  categorie_gram: string | null;
  valide:         boolean;
}

export interface MotDetail extends Mot {
  traductions: Traduction[];
  definitions: Definition[];
  expressions: Expression[];
}

export interface Traduction {
  id:           number;
  langue_source: string;
  langue_cible:  string;
  texte_source:  string;
  texte_cible:   string;
}

export interface Definition {
  id:     number;
  texte:  string;
  langue: string;
}

export interface Expression {
  id:           number;
  texte_creole: string;
  traduction_fr: string | null;
  explication:   string | null;
}

export interface CorpusEntry {
  id:      number;
  texte:   string;
  domaine: string;
  source:  string | null;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page:  number;
  size:  number;
}

// ============================================================
// Types Laravel
// ============================================================

export interface AuthUser {
  id:           number;
  name:         string;
  email:        string;
  roles:        string[];
  contributeur: {
    id:           number;
    pseudo:       string;
    nb_contrib:   number;
    de_confiance: boolean;
  } | null;
}

export interface Contribution {
  id:              number;
  table_cible:     string;
  entite_id:       number;
  type_action:     string;
  contenu_apres:   Record<string, unknown> | null;
  statut:          "en_attente" | "validé" | "rejeté";
  created_at:      string;
  moderateur_id:   number | null;
  modere_at:       string | null;
}

// ============================================================
// Helpers
// ============================================================

async function apiFetch<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error((body as { message?: string }).message ?? `HTTP ${res.status}`);
  }

  return res.json() as Promise<T>;
}

function authHeaders(token: string): HeadersInit {
  return { Authorization: `Bearer ${token}` };
}

// ============================================================
// FastAPI — Lecture (pas d'auth)
// ============================================================

export const fastapi = {
  /** Mot aléatoire (mot du jour) */
  randomWord: (): Promise<Mot> =>
    apiFetch(`${FASTAPI}/dictionary/random`),

  /** Recherche de mots */
  searchWords: (q: string, limit = 20): Promise<Mot[]> =>
    apiFetch(`${FASTAPI}/dictionary/search?q=${encodeURIComponent(q)}&limit=${limit}`),

  /** Détail d'un mot */
  getWord: (id: number): Promise<MotDetail> =>
    apiFetch(`${FASTAPI}/dictionary/${id}`),

  /** Liste paginée des mots */
  listWords: (page = 1, size = 20): Promise<PaginatedResponse<Mot>> =>
    apiFetch(`${FASTAPI}/dictionary?page=${page}&size=${size}`),

  /** Corpus paginé */
  getCorpus: (page = 1, size = 20): Promise<PaginatedResponse<CorpusEntry>> =>
    apiFetch(`${FASTAPI}/corpus?page=${page}&size=${size}`),

  /** Expressions paginées */
  getExpressions: (page = 1, size = 20): Promise<PaginatedResponse<Expression>> =>
    apiFetch(`${FASTAPI}/dictionary/expressions?page=${page}&size=${size}`),
};

// ============================================================
// Laravel — Auth
// ============================================================

export const laravelAuth = {
  register: (data: {
    name: string;
    email: string;
    password: string;
    password_confirmation: string;
  }): Promise<{ token: string; user: AuthUser }> =>
    apiFetch(`${LARAVEL}/auth/register`, { method: "POST", body: JSON.stringify(data) }),

  login: (email: string, password: string): Promise<{ token: string; user: AuthUser }> =>
    apiFetch(`${LARAVEL}/auth/login`, {
      method: "POST",
      body:   JSON.stringify({ email, password }),
    }),

  logout: (token: string): Promise<{ message: string }> =>
    apiFetch(`${LARAVEL}/auth/logout`, {
      method:  "POST",
      headers: authHeaders(token),
    }),

  me: (token: string): Promise<AuthUser> =>
    apiFetch(`${LARAVEL}/auth/user`, { headers: authHeaders(token) }),
};

// ============================================================
// Laravel — Contributions
// ============================================================

export const laravelContrib = {
  list: (token: string): Promise<{ data: Contribution[] }> =>
    apiFetch(`${LARAVEL}/contributions`, { headers: authHeaders(token) }),

  submit: (
    token:   string,
    payload: { table_cible: string; entite_id: number; contenu_apres: Record<string, unknown> }
  ): Promise<Contribution> =>
    apiFetch(`${LARAVEL}/contributions`, {
      method:  "POST",
      headers: authHeaders(token),
      body:    JSON.stringify(payload),
    }),

  delete: (token: string, id: number): Promise<{ message: string }> =>
    apiFetch(`${LARAVEL}/contributions/${id}`, {
      method:  "DELETE",
      headers: authHeaders(token),
    }),
};

// ============================================================
// Laravel — Admin
// ============================================================

export const laravelAdmin = {
  listPending: (token: string): Promise<{ data: Contribution[] }> =>
    apiFetch(`${LARAVEL}/admin/contributions`, { headers: authHeaders(token) }),

  validate: (token: string, id: number): Promise<{ message: string }> =>
    apiFetch(`${LARAVEL}/admin/contributions/${id}/validate`, {
      method:  "PUT",
      headers: authHeaders(token),
    }),

  reject: (token: string, id: number): Promise<{ message: string }> =>
    apiFetch(`${LARAVEL}/admin/contributions/${id}/reject`, {
      method:  "PUT",
      headers: authHeaders(token),
    }),
};
