<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>@yield('title', 'Bizouk Events') - Martinique</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #0b0d11;
  --surface: #141720;
  --surface2: #1c2030;
  --border: rgba(255,255,255,0.07);
  --accent: #00e5a0;
  --accent2: #ff6b35;
  --text: #e8eaf0;
  --muted: #6b7280;
  --radius: 8px;
  --font-display: 'Syne', sans-serif;
  --font-body: 'DM Sans', sans-serif;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: var(--text); font-family: var(--font-body); min-height: 100vh; }
nav {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.1rem 2.5rem;
  border-bottom: 1px solid var(--border);
  position: sticky; top: 0; z-index: 100;
  background: rgba(11,13,17,0.92); backdrop-filter: blur(14px);
}
.nav-logo { font-family: var(--font-display); font-weight: 800; font-size: 1.3rem; color: var(--text); text-decoration: none; }
.nav-logo span { color: var(--accent); }
.nav-links { display: flex; gap: 0.3rem; }
.nav-link {
  padding: 0.45rem 1rem; border-radius: 8px; font-size: 0.85rem;
  color: var(--muted); text-decoration: none; transition: all 0.15s;
}
.nav-link:hover, .nav-link.active { background: var(--surface2); color: var(--text); }
.nav-link.cta { background: var(--accent); color: #0b0d11; font-weight: 600; }
.nav-link.cta:hover { opacity: 0.88; }
.alert {
  margin: 1rem 2.5rem 0; padding: 0.8rem 1.2rem; border-radius: 8px;
  font-size: 0.875rem; display: flex; align-items: center; gap: 0.5rem;
}
.alert-success { background: rgba(0,229,160,0.12); border: 1px solid rgba(0,229,160,0.3); color: var(--accent); }
.alert-error { background: rgba(255,107,53,0.12); border: 1px solid rgba(255,107,53,0.3); color: var(--accent2); }
footer { border-top: 1px solid var(--border); padding: 2rem 2.5rem; text-align: center; color: var(--muted); font-size: 0.8rem; margin-top: 4rem; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--surface2); border-radius: 3px; }
</style>
@stack('styles')
</head>
<body>

<nav>
  <a href="{{ route('home') }}" class="nav-logo">Bizouk<span>.</span>events</a>
  <div class="nav-links">
    <a href="{{ route('home') }}" class="nav-link {{ request()->routeIs('home') ? 'active' : '' }}">Evenements</a>
    <a href="{{ route('dashboard') }}" class="nav-link cta">Dashboard</a>
  </div>
</nav>

@if(session('success'))
  <div class="alert alert-success">{{ session('success') }}</div>
@endif
@if(session('error'))
  <div class="alert alert-error">{{ session('error') }}</div>
@endif

@yield('content')

<footer>
  Evenements Bizouk Martinique - Universite des Antilles
</footer>

@stack('scripts')
</body>
</html>
