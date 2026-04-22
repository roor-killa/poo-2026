export async function POST() {
  return Response.json(
    { error: 'Le service de scraping Python est requis mais non disponible dans ce conteneur.' },
    { status: 503 }
  );
}
