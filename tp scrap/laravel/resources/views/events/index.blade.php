@extends('layouts.app')

@section('title', 'Evenements')

@push('styles')
<style>
.hero { padding: 3.5rem 2.5rem 1.5rem; }
.hero h1 { font-family: var(--font-display); font-size: clamp(1.8rem,3.5vw,2.8rem); font-weight: 800; line-height: 1.1; }
.hero h1 em { font-style: normal; color: var(--accent); }
.hero p { color: var(--muted); margin-top: 0.6rem; font-size: 0.95rem; font-weight: 300; }
.controls { padding: 1.2rem 2.5rem; display: flex; flex-wrap: wrap; gap: 0.75rem; align-items: center; border-bottom: 1px solid var(--border); }
.search-form { display: flex; flex: 1; min-width: 220px; max-width: 360px; position: relative; }
.search-form svg { position: absolute; left: 13px; top: 50%; transform: translateY(-50%); color: var(--muted); }
.search-form input { width: 100%; background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 0.55rem 1rem 0.55rem 2.5rem; color: var(--text); font-family: inherit; font-size: 0.875rem; outline: none; }
.search-form input:focus { border-color: var(--accent); }
.type-tabs { display: flex; flex-wrap: wrap; gap: 0.35rem; }
.type-tab { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 0.4rem 0.9rem; font-size: 0.8rem; color: var(--muted); text-decoration: none; }
.type-tab:hover { border-color: var(--accent); color: var(--text); }
.type-tab.active { background: var(--accent); border-color: var(--accent); color: #0b0d11; font-weight: 600; }
.grid-wrap { padding: 1.5rem 2.5rem; }
.count-line { font-size: 0.8rem; color: var(--muted); margin-bottom: 1.25rem; }
.count-line strong { color: var(--text); }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px,1fr)); gap: 1rem; }
.card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; display: flex; flex-direction: column; text-decoration: none; color: inherit; min-height: 360px; }
.card:hover { border-color: rgba(0,229,160,0.35); transform: translateY(-2px); }
.card-img { width: 100%; aspect-ratio: 16 / 10; object-fit: cover; background: var(--surface2); }
.card-body { padding: 1.1rem; display: flex; flex-direction: column; gap: 0.65rem; flex: 1; }
.card-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 0.5rem; }
.card-name { font-family: var(--font-display); font-weight: 700; font-size: 0.95rem; line-height: 1.3; }
.type-badge { background: var(--surface2); border-radius: 6px; padding: 0.18rem 0.5rem; font-size: 0.7rem; color: var(--accent); flex-shrink: 0; text-transform: capitalize; }
.card-desc { font-size: 0.8rem; color: var(--muted); line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.card-meta { margin-top: auto; border-top: 1px solid var(--border); padding-top: 0.65rem; display: flex; flex-direction: column; gap: 0.28rem; }
.meta-row { display: flex; align-items: center; gap: 0.45rem; font-size: 0.78rem; color: var(--muted); }
.price { color: var(--accent); font-weight: 700; }
.empty { grid-column: 1/-1; text-align: center; padding: 4rem 2rem; color: var(--muted); }
.empty h3 { font-family: var(--font-display); color: var(--text); margin-bottom: 0.5rem; }
.pagination { display: flex; justify-content: center; gap: 0.4rem; padding: 2rem 2.5rem; flex-wrap: wrap; }
.page-btn { background: var(--surface); border: 1px solid var(--border); color: var(--muted); padding: 0.45rem 0.85rem; border-radius: 8px; text-decoration: none; font-size: 0.82rem; }
.page-btn:hover { border-color: var(--accent); color: var(--text); }
.page-btn.active { background: var(--accent); border-color: var(--accent); color: #0b0d11; font-weight: 600; }
.page-btn.disabled { opacity: 0.3; pointer-events: none; }
</style>
@endpush

@section('content')
<div class="hero">
  <h1>Evenements <em>Martinique</em></h1>
  <p>{{ number_format($total, 0, ',', ' ') }} evenements Bizouk en base</p>
</div>

<div class="controls">
  <form method="GET" action="{{ route('home') }}" class="search-form">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
    <input type="search" name="search" placeholder="Rechercher" value="{{ $search }}">
    @if($type)<input type="hidden" name="type" value="{{ $type }}">@endif
  </form>

  <div class="type-tabs">
    <a href="{{ route('home', ['search' => $search]) }}" class="type-tab {{ !$type ? 'active' : '' }}">Tout</a>
    @foreach($types as $item)
      <a href="{{ route('home', ['type' => $item['slug'], 'search' => $search]) }}"
         class="type-tab {{ $type === $item['slug'] ? 'active' : '' }}">
        {{ $item['label'] }}
        <span style="opacity:0.6">({{ $item['count'] }})</span>
      </a>
    @endforeach
  </div>
</div>

<div class="grid-wrap">
  <p class="count-line"><strong>{{ $total }}</strong> resultat{{ $total > 1 ? 's' : '' }}</p>

  <div class="grid">
    @forelse($events as $event)
      <a href="{{ route('event.show', $event['id']) }}" class="card">
        @if($event['image_url'])
          <img src="{{ $event['image_url'] }}" alt="{{ $event['title'] }}" class="card-img" loading="lazy">
        @else
          <div class="card-img"></div>
        @endif

        <div class="card-body">
          <div class="card-head">
            <div class="card-name">{{ $event['title'] }}</div>
            @if($event['event_type'])
              <span class="type-badge">{{ str_replace('-', ' ', $event['event_type']) }}</span>
            @endif
          </div>

          @if($event['description'])
            <p class="card-desc">{{ $event['description'] }}</p>
          @endif

          <div class="card-meta">
            @if($event['start_date'])
              <div class="meta-row">Date : {{ \Carbon\Carbon::parse($event['start_date'])->format('d/m/Y H:i') }}</div>
            @endif
            @if($event['venue'])
              <div class="meta-row">Lieu : {{ $event['venue'] }}</div>
            @endif
            @if($event['min_price'] !== null)
              <div class="meta-row price">A partir de {{ number_format($event['min_price'], 2, ',', ' ') }} {{ $event['currency'] ?? 'EUR' }}</div>
            @endif
          </div>
        </div>
      </a>
    @empty
      <div class="empty">
        <h3>Aucun evenement trouve</h3>
        <p>Lancez le scraper depuis le dashboard pour charger les donnees Bizouk.</p>
      </div>
    @endforelse
  </div>
</div>

@if($totalPages > 1)
<div class="pagination">
  @php
    $baseParams = array_filter(['type' => $type, 'search' => $search]);
  @endphp

  <a href="{{ route('home', array_merge($baseParams, ['page' => max(1, $currentPage - 1)])) }}"
     class="page-btn {{ $currentPage <= 1 ? 'disabled' : '' }}">Prec.</a>

  @for($i = 1; $i <= $totalPages; $i++)
    @if($totalPages <= 7 || abs($i - $currentPage) <= 2 || $i == 1 || $i == $totalPages)
      <a href="{{ route('home', array_merge($baseParams, ['page' => $i])) }}"
         class="page-btn {{ $i == $currentPage ? 'active' : '' }}">{{ $i }}</a>
    @elseif($i == 2 || $i == $totalPages - 1)
      <span style="color:var(--muted);padding:0 4px;line-height:2">...</span>
    @endif
  @endfor

  <a href="{{ route('home', array_merge($baseParams, ['page' => min($totalPages, $currentPage + 1)])) }}"
     class="page-btn {{ $currentPage >= $totalPages ? 'disabled' : '' }}">Suiv.</a>
</div>
@endif
@endsection
