# CM8 - DevOps et CI/CD (Partie 2)
## Monitoring, Scaling et Production

---

## Rappel Partie 1

**Ce que nous avons vu :**
- ✅ DevOps : Culture et principes
- ✅ Docker : Conteneurisation
- ✅ CI/CD : Pipelines automatiques
- ✅ Déploiement production

**Aujourd'hui - Partie 2 :**
- **Monitoring** : Métriques et alertes
- **Logging** : Centralisation et analyse
- **Backup** : Sauvegardes automatiques
- **Scaling** : Mise à l'échelle
- **Load Balancing** : Répartition de charge
- **Sécurité** : Bonnes pratiques production

---

## 5. Monitoring et Observabilité

### 5.1 Les 3 Piliers de l'Observabilité

```
1. METRICS (Métriques)
   - CPU, RAM, disque
   - Temps de réponse
   - Taux d'erreur
   
2. LOGS (Journaux)
   - Événements applicatifs
   - Erreurs
   - Accès

3. TRACES (Traces)
   - Suivi des requêtes
   - Performance distribuée
   - Debugging
```

### 5.2 Prometheus + Grafana

**docker-compose.monitoring.yml :**
```yaml
version: '3.8'

services:
  # Application Flask avec métriques
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - PROMETHEUS_MULTIPROC_DIR=/tmp
    networks:
      - monitoring

  # Prometheus pour collecter les métriques
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
      - '--web.console.templates=/usr/share/prometheus/consoles'
    ports:
      - "9090:9090"
    networks:
      - monitoring
    restart: always

  # Grafana pour visualiser
  grafana:
    image: grafana/grafana:latest
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/datasources:/etc/grafana/provisioning/datasources
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    ports:
      - "3000:3000"
    networks:
      - monitoring
    restart: always
    depends_on:
      - prometheus

  # Node Exporter pour métriques système
  node-exporter:
    image: prom/node-exporter:latest
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    ports:
      - "9100:9100"
    networks:
      - monitoring
    restart: always

volumes:
  prometheus-data:
  grafana-data:

networks:
  monitoring:
    driver: bridge
```

**prometheus.yml :**
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  # Métriques de l'application Flask
  - job_name: 'flask-app'
    static_configs:
      - targets: ['app:5000']
    metrics_path: '/metrics'

  # Métriques système
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  # Auto-monitoring de Prometheus
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

# Règles d'alerte
rule_files:
  - 'alerts.yml'

# Configuration Alertmanager
alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']
```

### 5.3 Métriques dans Flask

**src/metrics.py :**
```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from flask import Response
import time
from functools import wraps


# Métriques
REQUEST_COUNT = Counter(
    'flask_request_count',
    'Application Request Count',
    ['method', 'endpoint', 'http_status']
)

REQUEST_DURATION = Histogram(
    'flask_request_duration_seconds',
    'Flask Request Duration',
    ['method', 'endpoint']
)

ACTIVE_REQUESTS = Gauge(
    'flask_active_requests',
    'Number of active requests'
)

DATABASE_QUERY_DURATION = Histogram(
    'database_query_duration_seconds',
    'Database Query Duration',
    ['query_type']
)


def track_request(func):
    """Décorateur pour tracker les requêtes"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        ACTIVE_REQUESTS.inc()
        start_time = time.time()
        
        try:
            response = func(*args, **kwargs)
            status_code = response.status_code if hasattr(response, 'status_code') else 200
            
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.endpoint,
                http_status=status_code
            ).inc()
            
            return response
        
        finally:
            duration = time.time() - start_time
            REQUEST_DURATION.labels(
                method=request.method,
                endpoint=request.endpoint
            ).observe(duration)
            
            ACTIVE_REQUESTS.dec()
    
    return wrapper


# Route pour exposer les métriques
def metrics_endpoint():
    """Endpoint /metrics pour Prometheus"""
    return Response(generate_latest(), mimetype='text/plain')
```

**src/app.py (avec métriques) :**
```python
from flask import Flask, jsonify, request
from metrics import track_request, metrics_endpoint, DATABASE_QUERY_DURATION
import time

app = Flask(__name__)


@app.route('/metrics')
def metrics():
    """Endpoint Prometheus"""
    return metrics_endpoint()


@app.route('/health')
def health():
    """Health check"""
    return jsonify({'status': 'healthy'}), 200


@app.route('/students', methods=['GET'])
@track_request
def get_students():
    """Liste des étudiants avec tracking"""
    
    # Simuler une requête DB
    start = time.time()
    students = [
        {'id': '001', 'name': 'Marie'},
        {'id': '002', 'name': 'Jean'}
    ]
    duration = time.time() - start
    
    DATABASE_QUERY_DURATION.labels(query_type='SELECT').observe(duration)
    
    return jsonify(students)


@app.route('/students/<student_id>', methods=['GET'])
@track_request
def get_student(student_id):
    """Détails d'un étudiant"""
    # Simuler une requête DB
    start = time.time()
    student = {'id': student_id, 'name': 'Student Name'}
    duration = time.time() - start
    
    DATABASE_QUERY_DURATION.labels(query_type='SELECT').observe(duration)
    
    return jsonify(student)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### 5.4 Alertes Prometheus

**alerts.yml :**
```yaml
groups:
  - name: application
    interval: 30s
    rules:
      # Alerte : Trop d'erreurs 5xx
      - alert: HighErrorRate
        expr: |
          rate(flask_request_count{http_status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Taux d'erreur élevé (instance {{ $labels.instance }})"
          description: "{{ $value }} erreurs/seconde détectées"

      # Alerte : Temps de réponse élevé
      - alert: HighResponseTime
        expr: |
          histogram_quantile(0.95, flask_request_duration_seconds_bucket) > 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Temps de réponse élevé"
          description: "P95 = {{ $value }}s (seuil: 1s)"

      # Alerte : Application down
      - alert: ApplicationDown
        expr: up{job="flask-app"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Application inaccessible"
          description: "L'application ne répond plus depuis 2 minutes"

      # Alerte : CPU élevé
      - alert: HighCPUUsage
        expr: |
          100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Utilisation CPU élevée"
          description: "CPU à {{ $value }}% sur {{ $labels.instance }}"

      # Alerte : Mémoire faible
      - alert: LowMemory
        expr: |
          node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100 < 10
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Mémoire disponible faible"
          description: "Seulement {{ $value }}% de RAM disponible"
```

---

## 6. Logging Centralisé

### 6.1 Stack ELK (Elasticsearch, Logstash, Kibana)

**docker-compose.logging.yml :**
```yaml
version: '3.8'

services:
  # Application avec logs structurés
  app:
    build: .
    environment:
      - LOG_LEVEL=INFO
      - LOGSTASH_HOST=logstash
    depends_on:
      - logstash
    networks:
      - logging

  # Elasticsearch pour stocker les logs
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - xpack.security.enabled=false
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
    networks:
      - logging
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5

  # Logstash pour collecter et transformer les logs
  logstash:
    image: docker.elastic.co/logstash/logstash:8.11.0
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline
    ports:
      - "5044:5044"
      - "9600:9600"
    environment:
      - "LS_JAVA_OPTS=-Xms256m -Xmx256m"
    depends_on:
      - elasticsearch
    networks:
      - logging

  # Kibana pour visualiser les logs
  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    depends_on:
      - elasticsearch
    networks:
      - logging

volumes:
  elasticsearch-data:

networks:
  logging:
    driver: bridge
```

**logstash/pipeline/logstash.conf :**
```
input {
  # Écoute les logs depuis l'application
  tcp {
    port => 5044
    codec => json_lines
  }
}

filter {
  # Parser les logs JSON
  json {
    source => "message"
  }
  
  # Ajouter des métadonnées
  mutate {
    add_field => {
      "environment" => "production"
      "application" => "student-api"
    }
  }
  
  # Parser les timestamps
  date {
    match => [ "timestamp", "ISO8601" ]
    target => "@timestamp"
  }
}

output {
  # Envoyer à Elasticsearch
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "student-api-logs-%{+YYYY.MM.dd}"
  }
  
  # Debug : afficher dans la console
  stdout {
    codec => rubydebug
  }
}
```

### 6.2 Logging Structuré en Python

**src/logging_config.py :**
```python
import logging
import logging.handlers
import json
import socket
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """Formateur JSON pour logs structurés"""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Ajouter les données supplémentaires
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
        
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


def setup_logging(app):
    """Configure le logging pour l'application"""
    
    # Logger principal
    logger = logging.getLogger('student_api')
    logger.setLevel(logging.INFO)
    
    # Handler : Console (développement)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # Handler : Fichier avec rotation
    file_handler = logging.handlers.RotatingFileHandler(
        'logs/app.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(JSONFormatter())
    
    # Handler : Logstash (production)
    logstash_host = app.config.get('LOGSTASH_HOST')
    if logstash_host:
        logstash_handler = logging.handlers.SocketHandler(
            logstash_host,
            5044
        )
        logstash_handler.setLevel(logging.INFO)
        logstash_handler.setFormatter(JSONFormatter())
        logger.addHandler(logstash_handler)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger
```

**src/app.py (avec logging) :**
```python
from flask import Flask, request, g
import uuid
from logging_config import setup_logging

app = Flask(__name__)
logger = setup_logging(app)


@app.before_request
def before_request():
    """Ajoute un request_id unique à chaque requête"""
    g.request_id = str(uuid.uuid4())
    
    logger.info(
        f"Request started: {request.method} {request.path}",
        extra={
            'request_id': g.request_id,
            'method': request.method,
            'path': request.path,
            'remote_addr': request.remote_addr
        }
    )


@app.after_request
def after_request(response):
    """Log la fin de la requête"""
    logger.info(
        f"Request completed: {response.status_code}",
        extra={
            'request_id': g.request_id,
            'status_code': response.status_code
        }
    )
    return response


@app.route('/students/<student_id>')
def get_student(student_id):
    """Route avec logging détaillé"""
    logger.info(
        f"Fetching student {student_id}",
        extra={'request_id': g.request_id, 'student_id': student_id}
    )
    
    try:
        # Logique métier
        student = {'id': student_id, 'name': 'Student Name'}
        
        logger.info(
            f"Student found: {student_id}",
            extra={'request_id': g.request_id}
        )
        
        return jsonify(student)
    
    except Exception as e:
        logger.error(
            f"Error fetching student {student_id}",
            exc_info=True,
            extra={'request_id': g.request_id, 'student_id': student_id}
        )
        return jsonify({'error': 'Internal error'}), 500
```

---

## 7. Backup et Disaster Recovery

### 7.1 Script de Backup PostgreSQL

**backup.sh :**
```bash
#!/bin/bash

# Configuration
BACKUP_DIR="/backups"
DB_NAME="students"
DB_USER="user"
DB_HOST="db"
RETENTION_DAYS=7

# Timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.sql.gz"

# Créer le répertoire si nécessaire
mkdir -p ${BACKUP_DIR}

# Backup
echo "[$(date)] Starting backup..."
pg_dump -h ${DB_HOST} -U ${DB_USER} ${DB_NAME} | gzip > ${BACKUP_FILE}

if [ $? -eq 0 ]; then
    echo "[$(date)] Backup successful: ${BACKUP_FILE}"
    
    # Calculer la taille
    SIZE=$(du -h ${BACKUP_FILE} | cut -f1)
    echo "[$(date)] Backup size: ${SIZE}"
    
    # Supprimer les anciens backups
    find ${BACKUP_DIR} -name "${DB_NAME}_*.sql.gz" -mtime +${RETENTION_DAYS} -delete
    echo "[$(date)] Old backups cleaned (retention: ${RETENTION_DAYS} days)"
else
    echo "[$(date)] Backup failed!"
    exit 1
fi

# Upload vers S3 (optionnel)
if [ ! -z "$AWS_S3_BUCKET" ]; then
    echo "[$(date)] Uploading to S3..."
    aws s3 cp ${BACKUP_FILE} s3://${AWS_S3_BUCKET}/backups/
    echo "[$(date)] Upload complete"
fi
```

**Dockerfile pour backup :**
```dockerfile
FROM postgres:15-alpine

RUN apk add --no-cache \
    aws-cli \
    bash

COPY backup.sh /usr/local/bin/backup.sh
RUN chmod +x /usr/local/bin/backup.sh

# Cron pour backup quotidien à 2h du matin
RUN echo "0 2 * * * /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1" > /etc/crontabs/root

CMD ["crond", "-f"]
```

**docker-compose (avec backup) :**
```yaml
services:
  backup:
    build:
      context: .
      dockerfile: Dockerfile.backup
    environment:
      - DB_NAME=students
      - DB_USER=user
      - DB_HOST=db
      - PGPASSWORD=${DB_PASSWORD}
      - AWS_S3_BUCKET=${S3_BUCKET}
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_KEY}
    volumes:
      - ./backups:/backups
    depends_on:
      - db
    networks:
      - app-network
```

### 7.2 Restore depuis Backup

**restore.sh :**
```bash
#!/bin/bash

BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: ./restore.sh <backup_file.sql.gz>"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "File not found: $BACKUP_FILE"
    exit 1
fi

echo "Restoring from: $BACKUP_FILE"
echo "WARNING: This will REPLACE the current database!"
read -p "Continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Restore cancelled"
    exit 0
fi

# Drop existing database
echo "Dropping existing database..."
psql -h db -U user -c "DROP DATABASE IF EXISTS students;"

# Create new database
echo "Creating new database..."
psql -h db -U user -c "CREATE DATABASE students;"

# Restore
echo "Restoring data..."
gunzip -c $BACKUP_FILE | psql -h db -U user students

if [ $? -eq 0 ]; then
    echo "Restore successful!"
else
    echo "Restore failed!"
    exit 1
fi
```

---

## 8. Scaling et Load Balancing

### 8.1 Scaling Horizontal

**docker-compose.scale.yml :**
```yaml
version: '3.8'

services:
  # Load Balancer (Nginx)
  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "80:80"
    depends_on:
      - app
    networks:
      - app-network

  # Application (plusieurs instances)
  app:
    build: .
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/students
    depends_on:
      - db
    networks:
      - app-network
    # Pas de ports exposés (Nginx fait le proxy)

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=students
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - app-network

volumes:
  postgres-data:

networks:
  app-network:
```

**nginx.conf (Load Balancing) :**
```nginx
events {
    worker_connections 1024;
}

http {
    # Pool de serveurs backend
    upstream app_servers {
        least_conn;  # Algorithme: moins de connexions
        
        server app:5000 weight=1 max_fails=3 fail_timeout=30s;
        # Les autres instances seront détectées automatiquement
    }
    
    # Configuration du serveur
    server {
        listen 80;
        server_name api.students.ua.fr;
        
        # Logs
        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;
        
        # Proxy vers les applications
        location / {
            proxy_pass http://app_servers;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Timeouts
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
            
            # Health check
            proxy_next_upstream error timeout http_500 http_502 http_503;
        }
        
        # Health check endpoint
        location /health {
            access_log off;
            proxy_pass http://app_servers/health;
        }
        
        # Métriques Prometheus
        location /metrics {
            proxy_pass http://app_servers/metrics;
        }
    }
}
```

**Démarrer avec scaling :**
```bash
# Démarrer avec 3 instances de l'app
docker-compose -f docker-compose.scale.yml up -d --scale app=3

# Vérifier
docker-compose ps

# Scaler à la volée
docker-compose -f docker-compose.scale.yml up -d --scale app=5

# Descaler
docker-compose -f docker-compose.scale.yml up -d --scale app=2
```

---

## 9. Cas Pratique Complet : Production-Ready Setup

**Structure du projet :**
```
project/
├── src/
│   ├── app.py
│   ├── config.py
│   ├── logging_config.py
│   └── metrics.py
├── tests/
├── monitoring/
│   ├── prometheus.yml
│   ├── alerts.yml
│   └── grafana/
├── logging/
│   └── logstash/
├── nginx/
│   └── nginx.conf
├── scripts/
│   ├── backup.sh
│   └── restore.sh
├── .github/
│   └── workflows/
│       └── deploy.yml
├── docker-compose.yml
├── docker-compose.prod.yml
├── Dockerfile
├── Dockerfile.prod
└── requirements.txt
```

**Commandes de déploiement :**
```bash
# 1. Build
docker-compose -f docker-compose.prod.yml build

# 2. Tests
docker-compose -f docker-compose.prod.yml run --rm app pytest

# 3. Migrations DB
docker-compose -f docker-compose.prod.yml run --rm app flask db upgrade

# 4. Démarrage
docker-compose -f docker-compose.prod.yml up -d --scale app=3

# 5. Vérification
docker-compose -f docker-compose.prod.yml ps
curl http://localhost/health

# 6. Logs
docker-compose -f docker-compose.prod.yml logs -f app

# 7. Monitoring
open http://localhost:3000  # Grafana
open http://localhost:9090  # Prometheus

# 8. Backup manuel
docker-compose -f docker-compose.prod.yml exec backup /usr/local/bin/backup.sh
```

---

## 10. Checklist Production

### Avant le Déploiement

**Sécurité :**
- [ ] Variables d'environnement sécurisées (secrets)
- [ ] HTTPS activé (certificats SSL)
- [ ] Firewall configuré
- [ ] Utilisateurs non-root dans les conteneurs
- [ ] Images scannées (vulnérabilités)

**Performance :**
- [ ] Cache configuré (Redis)
- [ ] CDN pour les assets statiques
- [ ] Connection pooling DB
- [ ] Compression Gzip activée

**Monitoring :**
- [ ] Métriques collectées (Prometheus)
- [ ] Dashboards créés (Grafana)
- [ ] Alertes configurées
- [ ] Logs centralisés (ELK)

**Backup :**
- [ ] Backups automatiques (quotidiens)
- [ ] Rétention définie
- [ ] Restore testé
- [ ] Backups off-site (S3)

**CI/CD :**
- [ ] Tests automatiques
- [ ] Linting automatique
- [ ] Build automatique
- [ ] Déploiement automatisé

**Documentation :**
- [ ] README à jour
- [ ] Runbook (procédures)
- [ ] Architecture documentée
- [ ] API documentée (Swagger/OpenAPI)

---

## Résumé CM8 Complet

### Partie 1 - Fondamentaux

✅ DevOps : Culture et principes  
✅ Docker : Conteneurisation  
✅ Docker Compose : Multi-conteneurs  
✅ CI/CD : Pipelines GitHub Actions / GitLab CI  
✅ Configuration production  

### Partie 2 - Production

✅ Monitoring : Prometheus + Grafana  
✅ Logging : ELK Stack  
✅ Backup : Automatisation et recovery  
✅ Scaling : Load balancing avec Nginx  
✅ Checklist production complète  

### Compétences Acquises

1. **Conteneuriser** une application Python/Flask
2. **Automatiser** le build et les tests (CI/CD)
3. **Monitorer** les métriques et logs
4. **Sauvegarder** et restaurer des données
5. **Scaler** une application en production
6. **Déployer** de manière sécurisée et fiable

---

*Fin du CM8 - DevOps et CI/CD*