#!/bin/sh
set -e

# Recache config + routes avec les variables d'env réelles (injectées par Docker Compose)
php artisan config:clear
php artisan config:cache
php artisan route:cache

# Migrations automatiques (idempotent)
php artisan migrate --force

# Seeding des rôles (idempotent — firstOrCreate)
php artisan db:seed --class=Database\\Seeders\\RoleSeeder --force

exec "$@"
