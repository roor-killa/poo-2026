@extends('layouts.app')
@section('title', $event['title'])

@push('styles')
<style>
.back-link { display: inline-flex; align-items: center; gap: 0.4rem; padding: 2rem 2.5rem 0; color: var(--muted); text-decoration: none; font-size: 0.85rem; }
.back-link:hover { color: var(--accent); }
.detail-wrap { padding: 2rem 2.5rem; max-width: 960px; display: grid; grid-template-columns: minmax(0, 1fr) 320px; gap: 1.5rem; }
.detail-header { margin-bottom: 1.5rem; }
.detail-cat { display: inline-block; background: var(--surface2); border-radius: 6px; padding: 0.25rem 0.65rem; font-size: 0.75rem; color: var(--accent); text-transform: capitalize; margin-bottom: 0.75rem; }
.detail-name { font-family: var(--font-display); font-size: clamp(1.5rem, 3vw, 2.2rem); font-weight: 800; line-height: 1.2; }
.detail-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.5rem; margin-bottom: 1rem; }
.detail-card h3 { font-family: var(--font-display); font-size: 0.8rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 1rem; }
.info-row { display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.65rem 0; border-bottom: 1px solid var(--border); }
.info-row:last-child { border-bottom: none; }
.info-label { font-size: 0.72rem; color: var(--muted); margin-bottom: 0.15rem; }
.info-value { font-size: 0.9rem; }
.info-link { color: var(--accent); text-decoration: none; }
.desc-text { font-size: 0.92rem; line-height: 1.7; color: var(--muted); font-weight: 300; white-space: pre-line; }
.poster { width: 100%; border-radius: var(--radius); border: 1px solid var(--border); background: var(--surface2); }
@media (max-width: 860px) {
  .detail-wrap { grid-template-columns: 1fr; }
}
</style>
@endpush

@section('content')
<a href="{{ route('home') }}" class="back-link">Retour aux evenements</a>

<div class="detail-wrap">
  <div>
    <div class="detail-header">
      @if($event['event_type'])
        <span class="detail-cat">{{ str_replace('-', ' ', $event['event_type']) }}</span>
      @endif
      <h1 class="detail-name">{{ $event['title'] }}</h1>
    </div>

    <div class="detail-card">
      <h3>Infos</h3>

      @if($event['start_date'])
        <div class="info-row">
          <div>
            <div class="info-label">Date</div>
            <div class="info-value">{{ \Carbon\Carbon::parse($event['start_date'])->format('d/m/Y H:i') }}</div>
          </div>
        </div>
      @endif

      @if($event['venue'])
        <div class="info-row">
          <div>
            <div class="info-label">Lieu</div>
            <div class="info-value">{{ $event['venue'] }}</div>
          </div>
        </div>
      @endif

      @if($event['address'])
        <div class="info-row">
          <div>
            <div class="info-label">Adresse</div>
            <div class="info-value">{{ $event['address'] }}</div>
          </div>
        </div>
      @endif

      @if($event['min_price'] !== null)
        <div class="info-row">
          <div>
            <div class="info-label">Prix</div>
            <div class="info-value">A partir de {{ number_format($event['min_price'], 2, ',', ' ') }} {{ $event['currency'] ?? 'EUR' }}</div>
          </div>
        </div>
      @endif

      @if($event['organizer'])
        <div class="info-row">
          <div>
            <div class="info-label">Organisateur</div>
            <div class="info-value">{{ $event['organizer'] }}</div>
          </div>
        </div>
      @endif
    </div>

    @if($event['description'])
      <div class="detail-card">
        <h3>Description</h3>
        <p class="desc-text">{{ $event['description'] }}</p>
      </div>
    @endif

    <div class="detail-card">
      <h3>Source</h3>
      <a href="{{ $event['source_url'] }}" target="_blank" rel="noopener" class="info-link">Voir sur Bizouk</a>
    </div>
  </div>

  <aside>
    @if($event['image_url'])
      <img src="{{ $event['image_url'] }}" alt="{{ $event['title'] }}" class="poster">
    @endif

    @if($event['contact_phone'] || $event['contact_email'] || $event['website'])
      <div class="detail-card" style="margin-top:1rem">
        <h3>Contact</h3>
        @if($event['contact_phone'])
          <div class="info-row">
            <div><div class="info-label">Telephone</div><div class="info-value">{{ $event['contact_phone'] }}</div></div>
          </div>
        @endif
        @if($event['contact_email'])
          <div class="info-row">
            <div><div class="info-label">Email</div><div class="info-value"><a href="mailto:{{ $event['contact_email'] }}" class="info-link">{{ $event['contact_email'] }}</a></div></div>
          </div>
        @endif
        @if($event['website'])
          <div class="info-row">
            <div><div class="info-label">Site</div><div class="info-value"><a href="{{ $event['website'] }}" target="_blank" rel="noopener" class="info-link">{{ parse_url($event['website'], PHP_URL_HOST) ?? $event['website'] }}</a></div></div>
          </div>
        @endif
      </div>
    @endif
  </aside>
</div>
@endsection
