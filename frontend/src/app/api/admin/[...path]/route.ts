/**
 * Proxy sécurisé vers les endpoints admin FastAPI.
 *
 * - Vérifie que l'utilisateur est admin via le token Laravel (Bearer)
 * - Transfère la requête à FastAPI avec la clé API (serveur uniquement)
 *
 * Routes exposées : /api/admin/[...path]
 * → GET/PUT/DELETE /api/v1/admin/[...path]
 */
import { NextRequest, NextResponse } from "next/server";

const FASTAPI =
  process.env.FASTAPI_INTERNAL_URL ??
  process.env.NEXT_PUBLIC_FASTAPI_URL ??
  "http://localhost:8000/api/v1";

const LARAVEL =
  process.env.LARAVEL_INTERNAL_URL ??
  process.env.NEXT_PUBLIC_LARAVEL_URL ??
  "http://localhost:8001/api";

const FASTAPI_API_KEY = process.env.FASTAPI_API_KEY ?? "changeme";

async function verifyAdmin(authHeader: string | null): Promise<boolean> {
  if (!authHeader) return false;
  try {
    const res = await fetch(`${LARAVEL}/auth/user`, {
      headers: { Authorization: authHeader },
      cache:   "no-store",
    });
    console.log("[admin-proxy] /auth/user status:", res.status);
    if (!res.ok) return false;
    const user = (await res.json()) as { roles?: unknown };
    console.log("[admin-proxy] user.roles raw:", JSON.stringify(user.roles));
    // getRoleNames() retourne une Collection Laravel — peut sérialiser en objet ou tableau
    const roles = user.roles;
    if (Array.isArray(roles)) return roles.includes("admin");
    if (roles && typeof roles === "object") return Object.values(roles).includes("admin");
    return false;
  } catch (e) {
    console.error("[admin-proxy] verifyAdmin error:", e);
    return false;
  }
}

async function handler(
  req: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const authHeader = req.headers.get("Authorization");
  if (!(await verifyAdmin(authHeader))) {
    return NextResponse.json({ message: "Accès refusé" }, { status: 403 });
  }

  const { path } = await params;
  const url      = new URL(req.url);
  const target   = `${FASTAPI}/admin/${path.join("/")}${url.search}`;

  const body =
    req.method !== "GET" && req.method !== "DELETE"
      ? await req.text()
      : undefined;

  const res = await fetch(target, {
    method:  req.method,
    headers: {
      "Content-Type": "application/json",
      "X-Api-Key":    FASTAPI_API_KEY,
    },
    body:  body ?? undefined,
    cache: "no-store",
  });

  if (res.status === 204) {
    return new NextResponse(null, { status: 204 });
  }

  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}

export const GET    = handler;
export const PUT    = handler;
export const DELETE = handler;
export const POST   = handler;
