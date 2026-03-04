<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

/**
 * Table `contributions` — journal communautaire.
 * Gérée par schema.sql. Laravel n'en crée pas la migration.
 */
class Contribution extends Model
{
    protected $table = 'contributions';

    public $timestamps = false;

    protected $fillable = [
        'contributeur_id',
        'table_cible',
        'entite_id',
        'type_action',
        'contenu_avant',
        'contenu_apres',
        'statut',
        'moderateur_id',
        'modere_at',
    ];

    protected $casts = [
        'contenu_avant' => 'array',
        'contenu_apres' => 'array',
        'modere_at'     => 'datetime',
        'created_at'    => 'datetime',
    ];

    public function contributeur()
    {
        return $this->belongsTo(Contributeur::class, 'contributeur_id');
    }

    public function moderateur()
    {
        return $this->belongsTo(Contributeur::class, 'moderateur_id');
    }
}
