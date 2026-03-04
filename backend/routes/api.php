<?php

use App\Http\Controllers\Api\AdminController;
use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Api\ContributionController;
use Illuminate\Support\Facades\Route;

// ============================================================
// Auth (publique)
// ============================================================
Route::prefix('auth')->group(function () {
    Route::post('register', [AuthController::class, 'register']);
    Route::post('login',    [AuthController::class, 'login']);

    Route::middleware('auth:sanctum')->group(function () {
        Route::post('logout', [AuthController::class, 'logout']);
        Route::get('user',    [AuthController::class, 'user']);
    });
});

// ============================================================
// Contributions (authentifié)
// ============================================================
Route::middleware('auth:sanctum')->group(function () {
    Route::get('contributions',        [ContributionController::class, 'index']);
    Route::post('contributions',       [ContributionController::class, 'store']);
    Route::delete('contributions/{id}', [ContributionController::class, 'destroy']);
});

// ============================================================
// Admin (role: admin)
// ============================================================
Route::prefix('admin')
    ->middleware(['auth:sanctum', 'role:admin'])
    ->group(function () {
        Route::get('contributions',                [AdminController::class, 'index']);
        Route::put('contributions/{id}/validate', [AdminController::class, 'validate']);
        Route::put('contributions/{id}/reject',   [AdminController::class, 'reject']);
    });

// ============================================================
// Healthcheck
// ============================================================
Route::get('health', fn () => response()->json(['status' => 'ok', 'service' => 'laravel']));
