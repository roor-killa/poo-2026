FROM php:8.2-fpm-alpine AS base

# Extensions PHP nécessaires
RUN apk add --no-cache \
        postgresql-dev \
        libzip-dev \
        zip \
        unzip \
        curl \
    && docker-php-ext-install \
        pdo \
        pdo_pgsql \
        zip \
        pcntl

# Composer
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

# Copie des fichiers de dépendances en premier (cache layer)
COPY composer.json composer.lock* ./

RUN composer install \
        --no-dev \
        --no-interaction \
        --optimize-autoloader \
        --no-scripts

# Code source
COPY . .

# Crée les répertoires nécessaires à Laravel
RUN mkdir -p bootstrap/cache \
        storage/framework/cache/data \
        storage/framework/sessions \
        storage/framework/views \
        storage/logs

# Autoload optimisé (sans caches config/route — ils seront générés à l'entrypoint)
RUN composer dump-autoload --optimize

# Permissions storage
RUN chown -R www-data:www-data storage bootstrap/cache \
    && chmod -R 775 storage bootstrap/cache

# Entrypoint : recache config, migrate, démarre le serveur
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 8001

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["php", "-S", "0.0.0.0:8001", "-t", "public"]
