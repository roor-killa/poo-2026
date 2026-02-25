<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Contribution;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class ContributionController extends Controller
{
    /**
     * POST /api/contributions
     * Soumet une nouvelle contribution (statut = en_attente).
     */
    public function store(Request $request): JsonResponse
    {
        $data = $request->validate([
            'table_cible'   => ['required', 'string', 'in:mots,traductions,expressions,definitions'],
            'entite_id'     => ['required', 'integer', 'min:1'],
            'contenu_apres' => ['required', 'array'],
        ]);

        $user          = $request->user();
        $contributeur  = $user->contributeur;

        if (! $contributeur) {
            return response()->json(['message' => 'Profil contributeur introuvable.'], 422);
        }

        $contribution = Contribution::create([
            'contributeur_id' => $contributeur->id,
            'table_cible'     => $data['table_cible'],
            'entite_id'       => $data['entite_id'],
            'type_action'     => 'correction',
            'contenu_apres'   => $data['contenu_apres'],
            'statut'          => 'en_attente',
        ]);

        $contributeur->incrementContrib();

        return response()->json($contribution, 201);
    }

    /**
     * GET /api/contributions
     * Liste les contributions de l'utilisateur connecté.
     */
    public function index(Request $request): JsonResponse
    {
        $contributions = $request->user()
            ->contributeur
            ?->contributions()
            ->orderByDesc('created_at')
            ->paginate(20);

        return response()->json($contributions ?? ['data' => []]);
    }

    /**
     * DELETE /api/contributions/{id}
     * Supprime une contribution en_attente (auteur uniquement).
     */
    public function destroy(Request $request, int $id): JsonResponse
    {
        $contributeur = $request->user()->contributeur;

        $contribution = Contribution::where('id', $id)
            ->where('contributeur_id', $contributeur?->id)
            ->firstOrFail();

        if ($contribution->statut !== 'en_attente') {
            return response()->json(['message' => 'Seules les contributions en attente peuvent être supprimées.'], 403);
        }

        $contribution->delete();

        return response()->json(['message' => 'Contribution supprimée.']);
    }
}
