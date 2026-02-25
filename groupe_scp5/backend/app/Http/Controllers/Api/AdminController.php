<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Contribution;
use App\Models\Contributeur;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class AdminController extends Controller
{
    /**
     * GET /api/admin/contributions
     * Toutes les contributions en_attente (paginées).
     */
    public function index(): JsonResponse
    {
        $contributions = Contribution::with('contributeur')
            ->where('statut', 'en_attente')
            ->orderByDesc('created_at')
            ->paginate(30);

        return response()->json($contributions);
    }

    /**
     * PUT /api/admin/contributions/{id}/validate
     * Valide une contribution → applique contenu_apres sur la table cible.
     */
    public function validate(Request $request, int $id): JsonResponse
    {
        $contribution = Contribution::where('statut', 'en_attente')
            ->findOrFail($id);

        $moderateur = $request->user()->contributeur;

        DB::transaction(function () use ($contribution, $moderateur) {
            // Applique contenu_apres sur la table cible
            if ($contribution->contenu_apres) {
                DB::table($contribution->table_cible)
                    ->where('id', $contribution->entite_id)
                    ->update($contribution->contenu_apres);
            }

            $contribution->update([
                'statut'        => 'validé',
                'moderateur_id' => $moderateur?->id,
                'modere_at'     => now(),
            ]);
        });

        return response()->json(['message' => 'Contribution validée.', 'contribution' => $contribution->fresh()]);
    }

    /**
     * PUT /api/admin/contributions/{id}/reject
     * Rejette une contribution.
     */
    public function reject(Request $request, int $id): JsonResponse
    {
        $contribution = Contribution::where('statut', 'en_attente')
            ->findOrFail($id);

        $moderateur = $request->user()->contributeur;

        $contribution->update([
            'statut'        => 'rejeté',
            'moderateur_id' => $moderateur?->id,
            'modere_at'     => now(),
        ]);

        return response()->json(['message' => 'Contribution rejetée.', 'contribution' => $contribution->fresh()]);
    }
}
