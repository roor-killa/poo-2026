<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

/**
 * Proxy vers la table `contributeurs` gérée par le schéma PostgreSQL (schema.sql).
 * Laravel n'en gère pas la migration — la table existe déjà via 01_schema.sql.
 */
class Contributeur extends Model
{
    protected $table = 'contributeurs';

    public $timestamps = false;

    protected $fillable = [
        'laravel_id',
        'pseudo',
        'nb_contrib',
        'de_confiance',
    ];

    protected $casts = [
        'de_confiance' => 'boolean',
        'nb_contrib'   => 'integer',
        'created_at'   => 'datetime',
    ];

    public function user()
    {
        return $this->belongsTo(User::class, 'laravel_id');
    }

    public function contributions()
    {
        return $this->hasMany(Contribution::class, 'contributeur_id');
    }

    /**
     * Incrémente le compteur de contributions.
     */
    public function incrementContrib(): void
    {
        $this->increment('nb_contrib');
    }
}
