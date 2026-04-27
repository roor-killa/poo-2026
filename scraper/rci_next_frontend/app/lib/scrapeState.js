// Module-level singleton shared across all route handlers in the same process.
export const scrapeState = {
  running: false,
  articles: 0,
  pages_visited: 0,
  error: null,
};
