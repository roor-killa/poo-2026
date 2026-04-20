{{-- laravel/resources/views/dashboard/index.blade.php --}}
@extends('layouts.app')
@section('title', 'Dashboard')

@push('styles')
<style>
.dash-wrap { padding: 2.5rem; max-width: 960px; }
.dash-title { font-family: var(--font-display); font-size: 1.8rem; font-weight: 800; letter-spacing: -0.03em; margin-bottom: 0.4rem; }
.dash-sub { color: var(--muted); font-size: 0.875rem; margin-bottom: 2.5rem; }

/* Status badge */
.status-badge { display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.3rem 0.8rem; border-radius: 50px; font-size: 0.78rem; font-weight: 600; }
.status-online  { background: rgba(0,229,160,0.15); color: var(--accent); }
.status-offline { background: rgba(255,107,53,0.15); color: var(--accent2); }
.dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }

/* Stats grid */
.stats-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px,1fr)); gap: 1rem; margin-bottom: 2rem; }
.stat-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.3rem; }
.stat-value { font-family: var(--font-display); font-size: 2.2rem; font-weight: 800; color: var(--accent); line-height: 1; }
.stat-label { color: var(--muted); font-size: 0.78rem; margin-top: 0.4rem; }

/* Categories table */
.table-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; margin-bottom: 2rem; }
.table-card h3 { padding: 1rem 1.3rem; font-family: var(--font-display); font-size: 0.85rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; border-bottom: 1px solid var(--border); }
.cat-row { display: flex; align-items: center; justify-content: space-between; padding: 0.75rem 1.3rem; border-bottom: 1px solid var(--border); font-size: 0.875rem; }
.cat-row:last-child { border-bottom: none; }
.cat-row-label { text-transform: capitalize; }
.cat-row-bar-wrap { flex: 1; margin: 0 1rem; height: 4px; background: var(--surface2); border-radius: 2px; overflow: hidden; }
.cat-row-bar { height: 100%; background: var(--accent); border-radius: 2px; transition: width 1s ease; }
.cat-row-count { color: var(--accent); font-weight: 600; font-size: 0.82rem; min-width: 28px; text-align: right; }

/* Scrape form */
.scrape-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.5rem; }
.scrape-card h3 { font-family: var(--font-display); font-size: 0.85rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 1.2rem; }
.form-row { display: flex; gap: 1rem; flex-wrap: wrap; align-items: flex-end; }
.form-group { display: flex; flex-direction: column; gap: 0.35rem; }
.form-group label { font-size: 0.78rem; color: var(--muted); }
.form-input { background: var(--surface2); border: 1px solid var(--border); border-radius: 8px; padding: 0.55rem 0.9rem; color: var(--text); font-family: inherit; font-size: 0.875rem; outline: none; transition: border-color 0.2s; min-width: 120px; }
.form-input:focus { border-color: var(--accent); }
.btn-scrape { background: var(--accent); color: #0b0d11; border: none; border-radius: 8px; padding: 0.58rem 1.4rem; font-family: var(--font-display); font-size: 0.875rem; font-weight: 700; cursor: pointer; transition: opacity 0.15s; }
.btn-scrape:hover { opacity: 0.85; }
.scrape-note { margin-top: 0.75rem; font-size: 0.78rem; color: var(--muted); }
</style>
@endpush

@section('content')
<div class="dash-wrap">
  <div style="display:flex; align-items:center; gap:1rem; margin-bottom:0.4rem;">
    <h1 class="dash-title">Dashboard</h1>
    <span class="status-badge {{ $apiStatus === 'online' ? 'status-online' : 'status-offline' }}">
      <span class="dot"></span>
      FastAPI {{ $apiStatus }}
    </span>
  </div>
  <p class="dash-sub">Statistiques en temps réel et contrôle du scraper</p>

  {{-- Stats --}}
  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-value">{{ $stats['total_businesses'] ?? 0 }}</div>
      <div class="stat-label">Entreprises total</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">{{ $stats['with_email'] ?? 0 }}</div>
      <div class="stat-label">Avec email</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">{{ $stats['with_phone'] ?? 0 }}</div>
      <div class="stat-label">Avec téléphone</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">{{ count($stats['by_category'] ?? []) }}</div>
      <div class="stat-label">Catégories</div>
    </div>
  </div>

  {{-- Par catégorie --}}
  @if(!empty($stats['by_category']))
  @php $maxCount = max(array_column($stats['by_category'], 'count')); @endphp
  <div class="table-card">
    <h3>Répartition par catégorie</h3>
    @foreach($stats['by_category'] as $cat)
      <div class="cat-row">
        <span class="cat-row-label">{{ $cat['label'] }}</span>
        <div class="cat-row-bar-wrap">
          <div class="cat-row-bar" style="width: {{ $maxCount > 0 ? round($cat['count'] / $maxCount * 100) : 0 }}%"></div>
        </div>
        <span class="cat-row-count">{{ $cat['count'] }}</span>
      </div>
    @endforeach
  </div>
  @endif

  {{-- Lancer le scraper --}}
  <div class="scrape-card">
    <h3>🕷 Lancer le scraper</h3>
    <form method="POST" action="{{ route('dashboard.scrape') }}">
      @csrf
      <div class="form-row">
        <div class="form-group">
          <label>Catégorie (vide = toutes)</label>
          <input type="text" name="categories[]" placeholder="ex: restaurants" class="form-input">
        </div>
        <div class="form-group">
          <label>Max / catégorie</label>
          <input type="number" name="max" value="30" min="5" max="200" class="form-input" style="width:90px">
        </div>
        <button type="submit" class="btn-scrape">Lancer ▶</button>
      </div>
    </form>
    <p class="scrape-note">⚠️ Le scraping s'exécute en arrière-plan. Actualisez la page dans quelques secondes pour voir les nouvelles données. Respectez le robots.txt de Bizouk.</p>
  </div>
</div>
@endsection
