FROM php:8.3-cli

RUN apt-get update && apt-get install -y \
    git \
    unzip \
    zip \
    libonig-dev \
    libpq-dev \
    libxml2-dev \
    libzip-dev \
    && docker-php-ext-install mbstring pdo pdo_pgsql xml zip \
    && rm -rf /var/lib/apt/lists/*

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

RUN composer create-project laravel/laravel . "^11.0" --no-interaction

COPY app app
COPY routes routes
COPY resources/views resources/views

RUN mkdir -p storage bootstrap/cache \
    && chown -R www-data:www-data storage bootstrap/cache

EXPOSE 80

CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=80"]
