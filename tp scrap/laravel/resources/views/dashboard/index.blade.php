@extends('layouts.app')
@section('title', 'Dashboard')

@push('styles')
<style>
.dash-wrap { padding: 2.5rem; max-width: 980px; }
.dash-head { display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; margin-bottom: 0.45rem; }
.dash-title { font-family: var(--font-display); font-size: 1.8rem; font-weight: 800; }
.dash-sub { color: var(--muted); font-size: 0.875rem; margin-bottom: 2rem; }
.status-badge { display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.3rem 0.8rem; border-radius: 8px; font-size: 0.78rem; font-weight: 600; }
.status-online { background: rgba(0,229,160,0.15); color: var(--accent); }
.status-offline { background: rgba(255,107,53,0.15); color: var(--accent2); }
.dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
.stat-card, .table-card, .scrape-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); }
.stat-card { padding: 1.3rem; }
.stat-value { font-family: var(--font-display); font-size: 2.15rem; font-weight: 800; color: var(--accent); line-height: 1; }
.stat-label { color: var(--muted); font-size: 0.78rem; margin-top: 0.4rem; }
.table-card { overflow: hidden; margin-bottom: 2rem; }
.panel-title { padding: 1rem 1.3rem; font-family: var(--font-display); font-size: 0.85rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; border-bottom: 1px solid var(--border); }
.cat-row { display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: 0.75rem 1.3rem; border-bottom: 1px solid var(--border); font-size: 0.875rem; }
.cat-row:last-child { border-bottom: none; }
.cat-row-label { text-transform: capitalize; min-width: 110px; }
.cat-row-bar-wrap { flex: 1; height: 4px; background: var(--surface2); border-radius: 2px; overflow: hidden; }
.cat-row-bar { height: 100%; background: var(--accent); border-radius: 2px; }
.cat-row-count { color: var(--accent); font-weight: 600; font-size: 0.82rem; min-width: 28px; text-align: right; }
.scrape-card { padding: 1.5rem; }
.scrape-title { font-family: var(--font-display); font-size: 0.85rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 1.2rem; }
.form-row { display: flex; gap: 1rem; flex-wrap: wrap; align-items: flex-end; }
.form-group { display: flex; flex-direction: column; gap: 0.35rem; }
.form-group label { font-size: 0.78rem; color: var(--muted); }
.form-input { background: var(--surface2); border: 1px solid var(--border); border-radius: 8px; padding: 0.55rem 0.9rem; color: var(--text); font-family: inherit; font-size: 0.875rem; outline: none; min-width: 150px; }
.form-input:focus { border-color: var(--accent); }
.btn-scrape { background: var(--accent); color: #0b0d11; border: none; border-radius: 8px; padding: 0.58rem 1.4rem; font-family: var(--font-display); font-size: 0.875rem; font-weight: 700; cursor: pointer; }
.btn-scrape:hover { opacity: 0.85; }
.scrape-note { margin-top: 0.75rem; font-size: 0.78rem; color: var(--muted); }
</style>
@endpush

@section('content')
<div class="dash-wrap">
  <div class="dash-head">
    <h1 class="dash-title">Dashboard</h1>
    <span class="status-badge {{ $apiStatus === 'online' ? 'status-online' : 'status-offline' }}">
      <span class="dot"></span>
      FastAPI {{ $apiStatus }}
    </span>
  </div>
  <p class="dash-sub">Statistiques et controle du scraper Bizouk</p>

  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-value">{{ $stats['total_events'] ?? 0 }}</div>
      <div class="stat-label">Evenements</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">{{ $stats['upcoming_events'] ?? 0 }}</div>
      <div class="stat-label">A venir</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">{{ $stats['with_email'] ?? 0 }}</div>
      <div class="stat-label">Avec email</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">{{ $stats['with_phone'] ?? 0 }}</div>
      <div class="stat-label">Avec telephone</div>
    </div>
  </div>

  @if(!empty($stats['by_type']))
    @php $maxCount = max(array_column($stats['by_type'], 'count')); @endphp
    <div class="table-card">
      <h2 class="panel-title">Repartition par type</h2>
      @foreach($stats['by_type'] as $cat)
        <div class="cat-row">
          <span class="cat-row-label">{{ str_replace('-', ' ', $cat['label']) }}</span>
          <div class="cat-row-bar-wrap">
            <div class="cat-row-bar" style="width: {{ $maxCount > 0 ? round($cat['count'] / $maxCount * 100) : 0 }}%"></div>
          </div>
          <span class="cat-row-count">{{ $cat['count'] }}</span>
        </div>
      @endforeach
    </div>
  @endif

  <div class="scrape-card">
    <h2 class="scrape-title">Lancer le scraper</h2>
    <form method="POST" action="/dashboard/scrape">
      @csrf
      <div class="form-row">
        <div class="form-group">
          <label>Region</label>
          <input type="text" name="regions[]" value="martinique" class="form-input">
        </div>
        <div class="form-group">
          <label>Max / region</label>
          <input type="number" name="max" value="30" min="1" max="200" class="form-input">
        </div>
        <button type="submit" class="btn-scrape">Lancer</button>
      </div>
    </form>
    <p class="scrape-note">Le scraper lit les cartes publiques Bizouk puis les donnees structurees des pages detail. Gardez un volume raisonnable.</p>
  </div>
</div>
@endsection
