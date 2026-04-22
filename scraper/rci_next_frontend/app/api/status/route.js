export async function GET() {
  return Response.json({ running: false, articles: 0, pages_visited: 0 });
}
