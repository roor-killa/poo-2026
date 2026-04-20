<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\DashboardController;
use App\Http\Controllers\EventController;

Route::get('/', [EventController::class, 'index'])->name('home');
Route::get('/evenement/{id}', [EventController::class, 'show'])->name('event.show');

Route::prefix('dashboard')->group(function () {
    Route::get('/', [DashboardController::class, 'index'])->name('dashboard');
    Route::post('/scrape', [DashboardController::class, 'triggerScrape'])->name('dashboard.scrape');
});
