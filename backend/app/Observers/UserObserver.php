<?php

namespace App\Observers;

use App\Models\Contributeur;
use App\Models\User;
use Illuminate\Support\Facades\Log;

/**
 * Observateur User :
 * - À la création d'un utilisateur → insère automatiquement une ligne
 *   dans la table `contributeurs` et assigne le rôle `contributeur`.
 */
class UserObserver
{
    public function created(User $user): void
    {
        try {
            Contributeur::create([
                'laravel_id'  => $user->id,
                'pseudo'      => $user->name,
                'nb_contrib'  => 0,
                'de_confiance' => false,
            ]);

            $user->assignRole('contributeur');
        } catch (\Throwable $e) {
            Log::error('UserObserver::created — échec', [
                'user_id' => $user->id,
                'error'   => $e->getMessage(),
            ]);
        }
    }
}
