# CM9 - Sécurité des Applications (Partie 2)
## CORS, CSRF, XSS et Sécurité des API

---

## Rappel Partie 1

**Ce que nous avons vu :**
- ✅ OWASP Top 10
- ✅ SQL Injection
- ✅ Authentication (JWT, Sessions)
- ✅ Authorization (RBAC)
- ✅ Password Security

**Aujourd'hui - Partie 2 :**
- **CORS** : Cross-Origin Resource Sharing
- **CSRF** : Cross-Site Request Forgery
- **XSS** : Cross-Site Scripting
- **API Security** : Rate limiting, validation
- **Encryption** : Données sensibles
- **Security Headers** : Protection navigateur
- **Audit et Logging** : Traçabilité

---

## 4. CORS (Cross-Origin Resource Sharing)

### 4.1 Qu'est-ce que CORS ?

> **CORS est un mécanisme de sécurité qui contrôle quels domaines peuvent accéder à votre API.**

**Problème : Same-Origin Policy**

```javascript
// Frontend sur http://app.example.com
fetch('http://api.example.com/students')  // ❌ Bloqué par le navigateur!
```

**Solution : Configurer CORS**

```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# ❌ DANGEREUX : Autorise TOUT
# CORS(app, resources={r"/*": {"origins": "*"}})

# ✅ SÉCURISÉ : Autorise seulement les domaines spécifiques
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://app.students.ua.fr",
            "https://admin.students.ua.fr"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["X-Total-Count"],
        "max_age": 3600,  # Cache preflight 1h
        "supports_credentials": True  # Cookies autorisés
    }
})


@app.route('/api/students')
def get_students():
    """Accessible depuis les domaines autorisés seulement"""
    return jsonify(students)
```

**Configuration manuelle :**

```python
from flask import Flask, make_response

@app.after_request
def add_cors_headers(response):
    """Ajoute les headers CORS manuellement"""
    origin = request.headers.get('Origin')
    
    # Whitelist des origines autorisées
    allowed_origins = [
        'https://app.students.ua.fr',
        'https://admin.students.ua.fr'
    ]
    
    if origin in allowed_origins:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Max-Age'] = '3600'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
    
    return response


@app.route('/api/students', methods=['OPTIONS'])
def preflight():
    """Réponse aux requêtes preflight"""
    response = make_response()
    response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin')
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response
```

---

## 5. CSRF (Cross-Site Request Forgery)

### 5.1 Qu'est-ce que CSRF ?

> **CSRF force un utilisateur authentifié à exécuter des actions non désirées.**

**Exemple d'attaque :**

```html
<!-- Site malveillant evil.com -->
<img src="https://bank.com/transfer?to=attacker&amount=1000">

<!-- Si l'utilisateur est connecté à bank.com, cette requête s'exécute! -->
```

### 5.2 Protection CSRF avec Flask-WTF

```python
from flask import Flask, render_template, request
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Activer la protection CSRF
csrf = CSRFProtect(app)


class StudentForm(FlaskForm):
    """Formulaire avec protection CSRF"""
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Create Student')


@app.route('/students/create', methods=['GET', 'POST'])
def create_student():
    """Route protégée contre CSRF"""
    form = StudentForm()
    
    if form.validate_on_submit():
        # Le token CSRF a été vérifié automatiquement
        student = Student(
            name=form.name.data,
            email=form.email.data
        )
        db.session.add(student)
        db.session.commit()
        return redirect('/students')
    
    return render_template('create_student.html', form=form)
```

**Template avec token CSRF :**

```html
<!-- create_student.html -->
<form method="POST">
    {{ form.hidden_tag() }}  <!-- Inclut le token CSRF -->
    
    <div>
        {{ form.name.label }}
        {{ form.name }}
    </div>
    
    <div>
        {{ form.email.label }}
        {{ form.email }}
    </div>
    
    {{ form.submit }}
</form>
```

### 5.3 CSRF pour API (Double Submit Cookie)

```python
import secrets
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)


def generate_csrf_token():
    """Génère un token CSRF"""
    return secrets.token_hex(32)


@app.route('/api/csrf-token', methods=['GET'])
def get_csrf_token():
    """Endpoint pour obtenir un token CSRF"""
    token = generate_csrf_token()
    
    response = make_response(jsonify({'csrf_token': token}))
    
    # Stocker le token dans un cookie
    response.set_cookie(
        'csrf_token',
        token,
        httponly=True,
        secure=True,  # HTTPS seulement
        samesite='Strict'
    )
    
    return response


def verify_csrf_token():
    """Vérifie le token CSRF"""
    # Token dans le header
    header_token = request.headers.get('X-CSRF-Token')
    
    # Token dans le cookie
    cookie_token = request.cookies.get('csrf_token')
    
    if not header_token or not cookie_token:
        return False
    
    # Les deux tokens doivent correspondre
    return header_token == cookie_token


@app.route('/api/students', methods=['POST'])
def create_student_api():
    """API protégée contre CSRF"""
    # Vérifier le token CSRF
    if not verify_csrf_token():
        return jsonify({'error': 'CSRF token missing or invalid'}), 403
    
    # Traiter la requête
    data = request.get_json()
    student = create_student(data)
    
    return jsonify(student), 201
```

**Utilisation côté client :**

```javascript
// 1. Obtenir le token CSRF
const response = await fetch('/api/csrf-token');
const data = await response.json();
const csrfToken = data.csrf_token;

// 2. Envoyer la requête avec le token
await fetch('/api/students', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRF-Token': csrfToken  // Token dans le header
  },
  body: JSON.stringify({name: 'Marie', email: 'marie@ua.fr'}),
  credentials: 'include'  // Envoyer les cookies
});
```

---

## 6. XSS (Cross-Site Scripting)

### 6.1 Qu'est-ce que XSS ?

> **XSS permet d'injecter du code JavaScript malveillant dans une page web.**

**Types de XSS :**

1. **Stored XSS** : Code stocké dans la BD
2. **Reflected XSS** : Code dans l'URL reflété dans la page
3. **DOM-based XSS** : Manipulation du DOM côté client

**Exemple d'attaque :**

```python
# ❌ VULNÉRABLE
@app.route('/search')
def search():
    query = request.args.get('q')
    
    # Danger : affiche directement l'input utilisateur
    return f"<h1>Résultats pour : {query}</h1>"

# Attaque :
# http://site.com/search?q=<script>alert('XSS!')</script>
# → Le script s'exécute!
```

### 6.2 Protection contre XSS

**1. Échappement automatique avec Jinja2 :**

```python
from flask import Flask, render_template

@app.route('/search')
def search():
    query = request.args.get('q', '')
    
    # ✅ Jinja2 échappe automatiquement
    return render_template('search.html', query=query)
```

```html
<!-- search.html -->
<h1>Résultats pour : {{ query }}</h1>
<!-- Jinja2 convertit < en &lt; automatiquement -->
```

**2. Échappement manuel :**

```python
from markupsafe import escape

@app.route('/search')
def search():
    query = request.args.get('q', '')
    
    # ✅ Échapper manuellement
    safe_query = escape(query)
    
    return f"<h1>Résultats pour : {safe_query}</h1>"
```

**3. Content Security Policy (CSP) :**

```python
@app.after_request
def add_security_headers(response):
    """Ajoute les headers de sécurité"""
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' https://fonts.gstatic.com;"
    )
    return response
```

**4. Validation et sanitisation des inputs :**

```python
from bleach import clean

ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'a']
ALLOWED_ATTRIBUTES = {'a': ['href', 'title']}

@app.route('/comments', methods=['POST'])
def add_comment():
    """Ajoute un commentaire avec sanitisation"""
    comment = request.form.get('comment')
    
    # ✅ Sanitiser le HTML
    safe_comment = clean(
        comment,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )
    
    # Stocker le commentaire sanitisé
    save_comment(safe_comment)
    
    return redirect('/comments')
```

---

## 7. Sécurité des API

### 7.1 Rate Limiting

```python
from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Configuration du rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="redis://localhost:6379"
)


@app.route('/api/students')
@limiter.limit("10 per minute")
def get_students():
    """Max 10 requêtes par minute"""
    return jsonify(students)


@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    """Max 5 tentatives de login par minute"""
    # Login logic...
    return jsonify({'token': token})


# Rate limit personnalisé par utilisateur
def get_user_id():
    """Récupère l'ID de l'utilisateur depuis le JWT"""
    from flask_jwt_extended import get_jwt_identity
    return get_jwt_identity()


@app.route('/api/protected')
@limiter.limit("100 per hour", key_func=get_user_id)
def protected():
    """Rate limit par utilisateur, pas par IP"""
    return jsonify({'data': 'protected data'})


# Gestion des erreurs de rate limit
@app.errorhandler(429)
def ratelimit_handler(e):
    """Réponse personnalisée pour rate limit dépassé"""
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': str(e.description)
    }), 429
```

### 7.2 Validation des Inputs

```python
from flask import Flask, request, jsonify
from marshmallow import Schema, fields, validate, ValidationError

app = Flask(__name__)


class StudentSchema(Schema):
    """Schéma de validation pour Student"""
    
    student_id = fields.Str(
        required=True,
        validate=validate.Regexp(r'^STU\d{6}$', error='Invalid student ID format')
    )
    
    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=2, max=100),
            validate.Regexp(r'^[a-zA-ZÀ-ÿ\s\-]+$', error='Invalid name format')
        ]
    )
    
    email = fields.Email(required=True)
    
    age = fields.Int(
        validate=validate.Range(min=16, max=100)
    )
    
    grade = fields.Float(
        validate=validate.Range(min=0, max=20)
    )


student_schema = StudentSchema()


@app.route('/api/students', methods=['POST'])
def create_student():
    """Création avec validation stricte"""
    try:
        # Valider les données
        data = student_schema.load(request.get_json())
        
        # Données validées, créer l'étudiant
        student = Student(**data)
        db.session.add(student)
        db.session.commit()
        
        return jsonify(student_schema.dump(student)), 201
    
    except ValidationError as e:
        return jsonify({'errors': e.messages}), 400
```

### 7.3 API Keys et Authentication

```python
from functools import wraps
import secrets

# Générer une API key
def generate_api_key():
    """Génère une API key sécurisée"""
    return secrets.token_urlsafe(32)


class APIKey(db.Model):
    """Modèle pour les API keys"""
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used_at = db.Column(db.DateTime)
    rate_limit = db.Column(db.Integer, default=1000)  # Requêtes/jour


def require_api_key(f):
    """Décorateur pour vérifier l'API key"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Récupérer l'API key
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({'error': 'API key missing'}), 401
        
        # Vérifier l'API key
        key_obj = APIKey.query.filter_by(key=api_key, is_active=True).first()
        
        if not key_obj:
            return jsonify({'error': 'Invalid API key'}), 401
        
        # Mettre à jour last_used_at
        key_obj.last_used_at = datetime.utcnow()
        db.session.commit()
        
        # Stocker dans g pour utilisation dans la route
        g.api_key = key_obj
        
        return f(*args, **kwargs)
    
    return decorated_function


@app.route('/api/v1/students')
@require_api_key
def api_get_students():
    """API protégée par API key"""
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students])
```

---

## 8. Encryption de Données Sensibles

### 8.1 Encryption at Rest

```python
from cryptography.fernet import Fernet
import base64
import os

class EncryptionService:
    """Service d'encryption pour données sensibles"""
    
    def __init__(self, key=None):
        if key is None:
            key = os.getenv('ENCRYPTION_KEY')
            if not key:
                raise ValueError("ENCRYPTION_KEY not set")
        
        self.cipher = Fernet(key.encode())
    
    def encrypt(self, data: str) -> str:
        """Encrypte une chaîne"""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Décrypte une chaîne"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()


# Génération de clé (à faire une seule fois)
def generate_encryption_key():
    """Génère une clé d'encryption"""
    key = Fernet.generate_key()
    print(f"ENCRYPTION_KEY={key.decode()}")
    # Stocker dans .env ou secrets management


# Utilisation
encryption = EncryptionService()

class Student(db.Model):
    """Étudiant avec données sensibles encryptées"""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    _ssn_encrypted = db.Column('ssn', db.String(200))  # SSN encrypté
    
    @property
    def ssn(self):
        """Décrypte le SSN"""
        if self._ssn_encrypted:
            return encryption.decrypt(self._ssn_encrypted)
        return None
    
    @ssn.setter
    def ssn(self, value):
        """Encrypte le SSN avant stockage"""
        if value:
            self._ssn_encrypted = encryption.encrypt(value)
        else:
            self._ssn_encrypted = None
```

### 8.2 HTTPS/TLS

**nginx.conf avec HTTPS :**

```nginx
server {
    listen 80;
    server_name api.students.ua.fr;
    
    # Rediriger HTTP vers HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.students.ua.fr;
    
    # Certificats SSL/TLS
    ssl_certificate /etc/letsencrypt/live/api.students.ua.fr/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.students.ua.fr/privkey.pem;
    
    # Configuration SSL moderne
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    
    # HSTS (HTTP Strict Transport Security)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    location / {
        proxy_pass http://app:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 9. Security Headers

```python
from flask import Flask

@app.after_request
def set_security_headers(response):
    """Ajoute tous les headers de sécurité recommandés"""
    
    # Empêche le clickjacking
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    
    # Empêche le MIME sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Active la protection XSS du navigateur
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Content Security Policy
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:;"
    )
    
    # Referrer Policy
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Permissions Policy (anciennement Feature-Policy)
    response.headers['Permissions-Policy'] = (
        "geolocation=(), "
        "microphone=(), "
        "camera=()"
    )
    
    # HSTS (seulement en HTTPS)
    if request.is_secure:
        response.headers['Strict-Transport-Security'] = (
            'max-age=31536000; includeSubDomains'
        )
    
    return response
```

---

## 10. Audit et Logging de Sécurité

```python
from flask import Flask, request, g
from datetime import datetime
import logging

# Configuration du logger de sécurité
security_logger = logging.getLogger('security')
security_logger.setLevel(logging.INFO)

handler = logging.FileHandler('logs/security.log')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
security_logger.addHandler(handler)


class SecurityAudit(db.Model):
    """Table d'audit de sécurité"""
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    event_type = db.Column(db.String(50))  # login, logout, failed_login, etc.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(256))
    details = db.Column(db.JSON)


def log_security_event(event_type, user_id=None, details=None):
    """Log un événement de sécurité"""
    
    # Log dans fichier
    security_logger.info(
        f"{event_type} - User: {user_id} - IP: {request.remote_addr} - Details: {details}"
    )
    
    # Log dans BD
    audit = SecurityAudit(
        event_type=event_type,
        user_id=user_id,
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string,
        details=details or {}
    )
    db.session.add(audit)
    db.session.commit()


@app.route('/api/login', methods=['POST'])
def login():
    """Login avec audit de sécurité"""
    data = request.get_json()
    email = data.get('email')
    
    user = User.query.filter_by(email=email).first()
    
    if user and user.check_password(data.get('password')):
        # Login réussi
        log_security_event(
            'login_success',
            user_id=user.id,
            details={'email': email}
        )
        
        return jsonify({'token': create_token(user)})
    
    else:
        # Login échoué
        log_security_event(
            'login_failed',
            user_id=user.id if user else None,
            details={'email': email, 'reason': 'invalid_credentials'}
        )
        
        return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
@require_admin
def delete_user(user_id):
    """Suppression avec audit"""
    user = User.query.get_or_404(user_id)
    
    log_security_event(
        'user_deleted',
        user_id=g.current_user.id,
        details={
            'deleted_user_id': user_id,
            'deleted_user_email': user.email
        }
    )
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted'})
```

---

## 11. Checklist de Sécurité Production

### ✅ Authentication & Authorization
- [ ] Mots de passe hashés (bcrypt, argon2)
- [ ] JWT avec expiration courte
- [ ] Refresh tokens sécurisés
- [ ] RBAC implémenté
- [ ] 2FA pour comptes sensibles

### ✅ Injection & Validation
- [ ] ORM pour éviter SQL injection
- [ ] Validation stricte des inputs (Marshmallow)
- [ ] Sanitisation HTML (bleach)
- [ ] Parameterized queries partout

### ✅ CORS & CSRF
- [ ] CORS configuré avec whitelist
- [ ] CSRF tokens sur formulaires
- [ ] SameSite cookies

### ✅ XSS
- [ ] Échappement automatique (Jinja2)
- [ ] Content Security Policy
- [ ] Validation des inputs

### ✅ API Security
- [ ] Rate limiting (Flask-Limiter)
- [ ] API keys ou JWT
- [ ] HTTPS obligatoire
- [ ] Versioning de l'API

### ✅ Encryption
- [ ] HTTPS/TLS configuré
- [ ] Données sensibles encryptées
- [ ] Secrets dans variables d'env
- [ ] Pas de clés dans le code

### ✅ Headers & Configuration
- [ ] Security headers configurés
- [ ] HSTS activé
- [ ] X-Frame-Options
- [ ] X-Content-Type-Options
- [ ] DEBUG=False en production

### ✅ Monitoring & Audit
- [ ] Logs de sécurité centralisés
- [ ] Alertes sur événements suspects
- [ ] Audit trail complet
- [ ] Monitoring des vulnérabilités

### ✅ Dependencies
- [ ] Dépendances à jour
- [ ] Scan de vulnérabilités (safety, snyk)
- [ ] Pas de packages obsolètes

---

## Résumé Partie 2

### Ce que nous avons vu

✅ **CORS** : Contrôle des origines autorisées  
✅ **CSRF** : Protection contre requêtes forgées  
✅ **XSS** : Échappement et sanitisation  
✅ **API Security** : Rate limiting, validation  
✅ **Encryption** : Données au repos et en transit  
✅ **Security Headers** : Protection navigateur  
✅ **Audit** : Logging et traçabilité  

### Conclusion CM9

**Compétences acquises :**
1. **OWASP Top 10** : Comprendre les vulnérabilités critiques
2. **Authentication** : Implémenter JWT et sessions sécurisées
3. **Authorization** : RBAC et contrôle d'accès
4. **Protection** : CORS, CSRF, XSS
5. **API Security** : Rate limiting et validation
6. **Encryption** : Protéger les données sensibles
7. **Audit** : Tracer les événements de sécurité

**Principes de sécurité :**
- **Defense in Depth** : Plusieurs couches de sécurité
- **Least Privilege** : Permissions minimales
- **Fail Secure** : Échouer de manière sécurisée
- **Keep it Simple** : Moins de complexité = moins de bugs
- **Stay Updated** : Patcher régulièrement

---

## Conclusion Générale du Cours POO

**Vous avez maintenant complété :**

✅ **CM1** : Classes et Objets  
✅ **CM2** : Héritage et Composition  
✅ **CM3** : Polymorphisme et Abstraction  
✅ **CM4** : Design Patterns  
✅ **CM5** : Principes SOLID  
✅ **CM6** : Architecture Logicielle  
✅ **CM7** : Tests et Qualité  
✅ **CM8** : DevOps et CI/CD  
✅ **CM9** : Sécurité  

**Félicitations ! 🎓**

Vous maîtrisez maintenant :
- Les fondamentaux de la POO
- Les patterns et architectures professionnels
- Les bonnes pratiques de développement
- Le déploiement et la production
- La sécurité des applications

**Prochaines étapes :**
- Projets personnels complexes
- Contributions open source
- Stage/emploi en développement
- Veille technologique continue

---

*Fin du CM9 - Sécurité des Applications*
*Fin du Cours POO *