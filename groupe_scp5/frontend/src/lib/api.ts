/**
 * Clients API — Lang Matinitjé
 *
 * - Lecture dictionnaire/corpus/chat → FastAPI (sans auth)
 * - Auth + Contributions → Laravel (token Sanctum Bearer)
 */

// Sélection de l'URL API :
//   Serveur (SSR/Docker) : FASTAPI_INTERNAL_URL est défini → http://api:8000/api/v1
//   Client (navigateur)  : FASTAPI_INTERNAL_URL est undefined (non-NEXT_PUBLIC_)
//                          → fallback sur NEXT_PUBLIC_FASTAPI_URL → http://localhost:8000/api/v1
const FASTAPI =
  process.env.FASTAPI_INTERNAL_URL ??
  process.env.NEXT_PUBLIC_FASTAPI_URL ??
  "http://localhost:8000/api/v1";

const LARAVEL =
  process.env.LARAVEL_INTERNAL_URL ??
  process.env.NEXT_PUBLIC_LARAVEL_URL ??
  "http://localhost:8001/api";

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
  source_id:   number | null;
  created_at:  string | null;
}

export interface Traduction {
  langue_source: string;
  langue_cible:  string;
  texte_source:  string;
  texte_cible:   string;
}

export interface Definition {
  definition: string;
  exemple:    string | null;
}

export interface Expression {
  id:            number;
  texte_creole:  string;
  texte_fr:      string | null;
  traduction_fr: string | null;
  explication:   string | null;
  type:          string;
}

export interface CorpusEntry {
  id:           number;
  texte_creole: string;
  texte_fr:     string | null;
  domaine:      string;
  source:       string | null;
}

export interface ChatMessage {
  role:    "user" | "fefen";
  content: string;
}

// Forme générique retournée par l'API (total + results)
interface ApiListResponse<T> {
  total:   number;
  page?:   number;
  limit?:  number;
  results: T[];
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
    cache:   "no-store",
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

  /** Recherche de mots — retourne directement le tableau de résultats */
  searchWords: (q: string, limit = 20): Promise<Mot[]> =>
    apiFetch<ApiListResponse<Mot>>(`${FASTAPI}/dictionary/search?q=${encodeURIComponent(q)}&limit=${limit}`)
      .then((r) => r.results),

  /** Détail d'un mot */
  getWord: (id: number): Promise<MotDetail> =>
    apiFetch(`${FASTAPI}/dictionary/${id}`),

  /** Liste paginée des mots — retourne {items, total} */
  listWords: (page = 1, size = 20): Promise<{ items: Mot[]; total: number }> =>
    apiFetch<ApiListResponse<Mot>>(`${FASTAPI}/dictionary?page=${page}&limit=${size}`)
      .then((r) => ({ items: r.results, total: r.total })),

  /** Corpus paginé — retourne {items, total} */
  getCorpus: (page = 1, size = 20): Promise<{ items: CorpusEntry[]; total: number }> =>
    apiFetch<ApiListResponse<CorpusEntry>>(`${FASTAPI}/corpus?page=${page}&limit=${size}`)
      .then((r) => ({ items: r.results, total: r.total })),

  /** Expressions paginées — retourne {items, total} */
  getExpressions: (page = 1, size = 20): Promise<{ items: Expression[]; total: number }> =>
    apiFetch<ApiListResponse<Expression>>(`${FASTAPI}/dictionary/expressions?page=${page}&limit=${size}`)
      .then((r) => ({ items: r.results, total: r.total })),

  /** Chatbot Fèfèn */
  chat: (message: string, sessionId?: string): Promise<{ reply: string; session_id: string }> =>
    apiFetch(`${FASTAPI}/chat`, {
      method: "POST",
      body:   JSON.stringify({ message, session_id: sessionId ?? null }),
    }),
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
