import { Pool } from 'pg';

const pool = new Pool({
  host:     process.env.POSTGRES_HOST     ?? 'postgres',
  port:     Number(process.env.POSTGRES_PORT ?? 5432),
  database: process.env.POSTGRES_DB       ?? 'poo_db',
  user:     process.env.POSTGRES_USER     ?? 'postgres',
  password: process.env.POSTGRES_PASSWORD ?? 'postgres',
});

export async function GET() {
  try {
    const { rows } = await pool.query(`
      SELECT
        title,
        metadata->>'author'  AS author,
        metadata->>'photo'   AS photo,
        metadata->>'infos'   AS infos,
        content              AS body,
        url,
        published_at         AS date_extraction
      FROM documents
      WHERE source = 'rci'
      ORDER BY scraped_at DESC
      LIMIT 200
    `);
    return Response.json(rows);
  } catch (err) {
    console.error('[/api/raw-data]', err.message);
    return Response.json({ error: err.message }, { status: 500 });
  }
}
