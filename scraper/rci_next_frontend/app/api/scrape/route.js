import { load } from 'cheerio';
import { Pool } from 'pg';
import { scrapeState } from '../../lib/scrapeState.js';

export const dynamic = 'force-dynamic';

const pool = new Pool({
  host:     process.env.POSTGRES_HOST     ?? 'postgres',
  port:     Number(process.env.POSTGRES_PORT ?? 5432),
  database: process.env.POSTGRES_DB       ?? 'poo_db',
  user:     process.env.POSTGRES_USER     ?? 'postgres',
  password: process.env.POSTGRES_PASSWORD ?? 'postgres',
});

const BASE_URL   = 'https://rci.fm';
const START_PATH = '/martinique/infos/toutes-les-infos';
const DOMAIN     = 'rci.fm';
const BOT_UA     = 'Lang-Matinitje-Bot/1.0 (Open Source)';

function normalizeUrl(raw) {
  const u = new URL(raw);
  return `${u.protocol}//${u.host}${u.pathname}`.replace(/\/$/, '');
}

function isValidLink(url) {
  try {
    const u = new URL(url);
    if (!u.hostname.includes(DOMAIN)) return false;
    if (!u.protocol.startsWith('http')) return false;
    const bad = ['.pdf','.jpg','.jpeg','.png','.gif','.mp3','.mp4','.zip'];
    return !bad.some(ext => u.pathname.toLowerCase().endsWith(ext));
  } catch { return false; }
}

function looksLikeArticle(url) {
  try {
    const path = new URL(url).pathname.replace(/^\/|\/$/g, '');
    return path.split('/').length >= 4;
  } catch { return false; }
}

function extractLinks($, currentUrl, visited, knownUrls) {
  const seen = new Set();
  const articles = [], others = [];
  $('a[href]').each((_, el) => {
    try {
      const href = $(el).attr('href');
      const abs  = new URL(href, currentUrl).toString();
      const norm = normalizeUrl(abs);
      if (seen.has(norm) || visited.has(norm) || knownUrls.has(norm)) return;
      if (!isValidLink(norm)) return;
      seen.add(norm);
      (looksLikeArticle(norm) ? articles : others).push(norm);
    } catch { /* bad href */ }
  });
  return [...articles, ...others];
}

function parseArticle($, url) {
  const titleTag = $('h1[itemprop="name"]').first();
  const title    = titleTag.text().trim();
  if (!title) return null;

  const author    = $('[itemprop="author"]').first().text().trim();
  const photo     = $('img[itemprop="image"]').first().attr('src') ?? '';
  const infoElems = $('.info');
  const infos     = infoElems.length > 2 ? $(infoElems.get(2)).text().trim() : '';
  const body      = $('[property="schema:text"]')
                      .map((_, el) => $(el).text().trim()).get().join(' ') || title;

  return { title, author, photo, infos, body, url };
}

async function upsertArticle(article) {
  const meta = JSON.stringify({
    author: article.author,
    photo:  article.photo,
    infos:  article.infos,
  });
  await pool.query(
    `INSERT INTO documents (source, doc_type, title, content, url, metadata)
     VALUES ('rci', 'actualite', $1, $2, $3, $4)
     ON CONFLICT (url) DO UPDATE SET
       title      = EXCLUDED.title,
       content    = EXCLUDED.content,
       metadata   = EXCLUDED.metadata,
       scraped_at = NOW()
     WHERE documents.content  IS DISTINCT FROM EXCLUDED.content
        OR documents.metadata IS DISTINCT FROM EXCLUDED.metadata`,
    [article.title, article.body, article.url, meta],
  );
}

async function crawl(startUrl, maxDepth, maxPages, delaySeconds) {
  const visited = new Set();

  const { rows } = await pool.query(
    "SELECT url FROM documents WHERE source = 'rci' AND url IS NOT NULL",
  );
  const knownUrls = new Set(rows.map(r => r.url));

  async function visit(url, depth) {
    const norm = normalizeUrl(url);
    if (visited.has(norm))                     return;
    if (depth > maxDepth)                      return;
    if (maxPages && visited.size >= maxPages)  return;
    if (depth > 0 && knownUrls.has(norm))      return;

    visited.add(norm);
    scrapeState.pages_visited = visited.size;

    await new Promise(r => setTimeout(r, delaySeconds * 1000));

    let html;
    try {
      const res = await fetch(norm, {
        headers: { 'User-Agent': BOT_UA },
        signal:  AbortSignal.timeout(15000),
      });
      if (!res.ok) return;
      html = await res.text();
    } catch { return; }

    const $ = load(html);
    const article = parseArticle($, norm);
    if (article) {
      await upsertArticle(article);
      scrapeState.articles += 1;
    }

    if (depth < maxDepth) {
      const links = extractLinks($, norm, visited, knownUrls);
      for (const link of links) {
        if (maxPages && visited.size >= maxPages) break;
        await visit(link, depth + 1);
      }
    }
  }

  await visit(startUrl, 0);
}

export async function POST(request) {
  if (scrapeState.running) {
    return Response.json({ error: 'Un scraping est déjà en cours.' }, { status: 409 });
  }

  const body = await request.json().catch(() => ({}));
  const maxDepth = Math.min(Number(body.max_depth ?? 1), 3);
  const maxPages = Math.min(Number(body.max_pages ?? 10), 100);
  const delay    = Math.max(Number(body.delay    ?? 1.5), 0.5);

  scrapeState.running      = true;
  scrapeState.articles     = 0;
  scrapeState.pages_visited = 0;
  scrapeState.error        = null;

  crawl(BASE_URL + START_PATH, maxDepth, maxPages, delay)
    .then(() => { scrapeState.running = false; })
    .catch(err => {
      scrapeState.running = false;
      scrapeState.error   = String(err);
    });

  return Response.json({ ok: true });
}
