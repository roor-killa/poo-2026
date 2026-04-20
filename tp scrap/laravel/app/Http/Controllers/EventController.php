<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class EventController extends Controller
{
    private string $apiBase;

    public function __construct()
    {
        $this->apiBase = env('FASTAPI_URL', 'http://fastapi:8000');
    }

    public function index(Request $request)
    {
        $page = $request->get('page', 1);
        $type = $request->get('type');
        $search = $request->get('search');

        $response = Http::timeout(10)->get("{$this->apiBase}/api/events", [
            'page' => $page,
            'per_page' => 24,
            'region' => 'martinique',
            'event_type' => $type,
            'search' => $search,
        ]);

        $data = $response->successful()
            ? $response->json()
            : ['data' => [], 'total' => 0, 'pages' => 0, 'page' => 1];

        $typeResponse = Http::timeout(5)->get("{$this->apiBase}/api/event-types");
        $types = $typeResponse->successful() ? $typeResponse->json() : [];

        return view('events.index', [
            'events' => $data['data'] ?? [],
            'total' => $data['total'] ?? 0,
            'currentPage' => $data['page'] ?? 1,
            'totalPages' => $data['pages'] ?? 1,
            'types' => $types,
            'type' => $type,
            'search' => $search,
        ]);
    }

    public function show(int $id)
    {
        $response = Http::timeout(10)->get("{$this->apiBase}/api/events/{$id}");

        if (!$response->successful()) {
            abort(404, 'Evenement introuvable');
        }

        return view('events.show', ['event' => $response->json()]);
    }
}
