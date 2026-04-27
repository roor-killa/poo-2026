import { scrapeState } from '../../lib/scrapeState.js';

export const dynamic = 'force-dynamic';

export async function GET() {
  return Response.json({
    running:       scrapeState.running,
    articles:      scrapeState.articles,
    pages_visited: scrapeState.pages_visited,
    error:         scrapeState.error,
  });
}
