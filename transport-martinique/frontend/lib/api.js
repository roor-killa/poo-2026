export async function fetchSearch(search = "", direction = "") {
  const params = new URLSearchParams();
  if (search) {
    params.set("q", search);
  }
  if (direction) {
    params.set("direction", direction);
  }

  const query = params.toString();
  const url = query ? `/backend/api/search?${query}` : "/backend/api/search";

  const response = await fetch(url, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  return response.json();
}
