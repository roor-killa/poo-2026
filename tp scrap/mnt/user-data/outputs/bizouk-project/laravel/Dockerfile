FROM php:8.3-apache

# Extensions PHP nécessaires
RUN apt-get update && apt-get install -y \
    git curl zip unzip libpq-dev libzip-dev nodejs npm \
    && docker-php-ext-install pdo pdo_pgsql zip \
    && rm -rf /var/lib/apt/lists/*

# Composer
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

# Apache : DocumentRoot → /var/www/html/public
RUN sed -i 's|/var/www/html|/var/www/html/public|g' /etc/apache2/sites-available/000-default.conf
RUN a2enmod rewrite

WORKDIR /var/www/html

# Installe les dépendances si composer.json présent
COPY composer.json composer.lock* ./
RUN composer install --no-scripts --no-autoloader --ignore-platform-reqs 2>/dev/null || true

COPY . .

RUN composer dump-autoload --optimize 2>/dev/null || true

RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache 2>/dev/null || true

EXPOSE 80
