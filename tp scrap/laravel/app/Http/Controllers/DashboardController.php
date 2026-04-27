<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class DashboardController extends Controller
{
    private string $apiBase;

    public function __construct()
    {
        $this->apiBase = env('FASTAPI_URL', 'http://fastapi:8000');
    }

    public function index()
    {
        $statsResponse = Http::timeout(5)->get("{$this->apiBase}/api/stats");
        $stats = $statsResponse->successful() ? $statsResponse->json() : [];

        $healthResponse = Http::timeout(3)->get("{$this->apiBase}/health");
        $apiStatus = $healthResponse->successful() ? 'online' : 'offline';

        return view('dashboard.index', [
            'stats' => $stats,
            'apiStatus' => $apiStatus,
        ]);
    }

    public function triggerScrape(Request $request)
    {
        $regions = collect((array) $request->input('regions', []))
            ->map(fn ($region) => trim((string) $region))
            ->filter()
            ->values()
            ->all();

        $regions = empty($regions) ? null : $regions;
        $max = $request->input('max', 30);

        $response = Http::timeout(10)->post("{$this->apiBase}/api/scrape", [
            'regions' => $regions,
            'max_per_region' => (int) $max,
            'fetch_details' => true,
        ]);

        if ($response->successful()) {
            return redirect()->route('dashboard')->with('success', 'Scraping Bizouk lance en arriere-plan.');
        }

        return redirect()->route('dashboard')->with('error', 'Impossible de lancer le scraper.');
    }
}
