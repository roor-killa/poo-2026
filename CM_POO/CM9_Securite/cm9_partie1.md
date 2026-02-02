# CM9 - Sécurité des Applications (Partie 1)
## OWASP Top 10, Authentication et Authorization

---

## Introduction

### Rappel des cours précédents

**CM1-CM6 :** Architecture et Design  
**CM7 :** Tests et Qualité  
**CM8 :** DevOps et CI/CD  

**Aujourd'hui - CM9 :**
- **OWASP Top 10** : Vulnérabilités critiques
- **Authentication** : Qui êtes-vous ?
- **Authorization** : Que pouvez-vous faire ?
- **JWT** : JSON Web Tokens
- **Password Security** : Hashing et stockage
- **Session Management** : Gestion des sessions

---

## 1. OWASP Top 10 (2021)

### 1.1 Introduction à OWASP

> **OWASP (Open Web Application Security Project)** est une organisation qui publie le Top 10 des vulnérabilités web les plus critiques.

**OWASP Top 10 - 2021 :**

```
1. A01 - Broken Access Control
2. A02 - Cryptographic Failures
3. A03 - Injection
4. A04 - Insecure Design
5. A05 - Security Misconfiguration
6. A06 - Vulnerable and Outdated Components
7. A07 - Identification and Authentication Failures
8. A08 - Software and Data Integrity Failures
9. A09 - Security Logging and Monitoring Failures
10. A10 - Server-Side Request Forgery (SSRF)
```

### 1.2 A01 - Broken Access Control

**Problème :** Utilisateurs accèdent à des ressources non autorisées.

**Exemple vulnérable :**

```python
# ❌ VULNÉRABLE
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    """N'importe qui peut accéder à n'importe quel profil"""
    user = User.query.get(user_id)
    return jsonify(user.to_dict())
```

**Attaque :**
```bash
# Attaquant change l'ID dans l'URL
curl http://api.example.com/api/users/1      # Mon profil
curl http://api.example.com/api/users/2      # Profil d'un autre! 🚨
curl http://api.example.com/api/users/999    # Profil admin! 🚨
```

**Solution sécurisée :**

```python
# ✅ SÉCURISÉ
from flask import Flask, jsonify, g
from functools import wraps

def require_auth(f):
    """Décorateur pour vérifier l'authentification"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function


def require_owner_or_admin(f):
    """Décorateur pour vérifier les permissions"""
    @wraps(f)
    def decorated_function(user_id, *args, **kwargs):
        if not g.user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        # Vérifier si c'est l'utilisateur ou un admin
        if g.user.id != user_id and not g.user.is_admin:
            return jsonify({'error': 'Forbidden'}), 403
        
        return f(user_id, *args, **kwargs)
    return decorated_function


@app.route('/api/users/<int:user_id>')
@require_auth
@require_owner_or_admin
def get_user(user_id):
    """Seulement le propriétaire ou un admin peut accéder"""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())
```

### 1.3 A03 - Injection (SQL Injection)

**Problème :** Données non validées exécutées comme code.

**Exemple vulnérable :**

```python
# ❌ VULNÉRABLE - SQL INJECTION
from flask import request
import sqlite3

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    # Construction de requête SQL avec des strings - DANGEREUX!
    query = f"SELECT * FROM users WHERE email='{email}' AND password='{password}'"
    
    conn = sqlite3.connect('users.db')
    cursor = conn.execute(query)
    user = cursor.fetchone()
    
    if user:
        return jsonify({'message': 'Logged in'})
    return jsonify({'error': 'Invalid credentials'}), 401
```

**Attaque :**
```python
# Attaquant envoie :
email = "admin@example.com' OR '1'='1"
password = "anything"

# Requête devient :
# SELECT * FROM users WHERE email='admin@example.com' OR '1'='1' AND password='anything'
# '1'='1' est toujours vrai → BYPASS!
```

**Solution sécurisée :**

```python
# ✅ SÉCURISÉ - Parameterized Queries
from flask import request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    # ✅ ORM (SQLAlchemy) protège contre l'injection
    user = User.query.filter_by(email=email).first()
    
    if user and user.check_password(password):
        return jsonify({'message': 'Logged in'})
    
    return jsonify({'error': 'Invalid credentials'}), 401


# Ou avec raw SQL sécurisé:
@app.route('/search')
def search():
    query = request.args.get('q')
    
    # ✅ Paramètres bindés (? placeholder)
    results = db.session.execute(
        "SELECT * FROM products WHERE name LIKE ?",
        (f"%{query}%",)
    ).fetchall()
    
    return jsonify([dict(r) for r in results])
```

### 1.4 A02 - Cryptographic Failures

**Problème :** Données sensibles non chiffrées.

**Exemple vulnérable :**

```python
# ❌ VULNÉRABLE - Mot de passe en clair
class User(db.Model):
    email = db.Column(db.String(120))
    password = db.Column(db.String(120))  # 🚨 En clair!

def create_user(email, password):
    user = User(email=email, password=password)  # 🚨 Stocké en clair
    db.session.add(user)
    db.session.commit()
```

**Solution sécurisée :**

```python
# ✅ SÉCURISÉ - Hashing avec bcrypt
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

class User(db.Model):
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(256))  # ✅ Hash, pas clair
    
    def set_password(self, password):
        """Hash le mot de passe"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Vérifie le mot de passe"""
        return bcrypt.check_password_hash(self.password_hash, password)


def create_user(email, password):
    user = User(email=email)
    user.set_password(password)  # ✅ Hash automatique
    db.session.add(user)
    db.session.commit()
```

---

## 2. Authentication (Authentification)

### 2.1 Qu'est-ce que l'Authentication ?

> **L'authentication vérifie l'identité : "Qui êtes-vous ?"**

**Méthodes d'authentication :**
1. **Something you know** : Mot de passe, PIN
2. **Something you have** : Token, smartphone, clé
3. **Something you are** : Biométrie (empreinte, visage)

**2FA (Two-Factor Authentication) :** Combinaison de 2 méthodes

### 2.2 Password-Based Authentication

**Système complet avec Flask :**

```python
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# ============================================================================
# MODELS
# ============================================================================

class User(db.Model):
    """Modèle utilisateur sécurisé"""
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)
    
    def set_password(self, password):
        """Hash et stocke le mot de passe"""
        # Validation du mot de passe
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Vérifie le mot de passe"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def is_locked(self):
        """Vérifie si le compte est verrouillé"""
        if self.locked_until and datetime.utcnow() < self.locked_until:
            return True
        
        # Reset si le verrouillage est expiré
        if self.locked_until and datetime.utcnow() >= self.locked_until:
            self.locked_until = None
            self.failed_login_attempts = 0
            db.session.commit()
        
        return False
    
    def increment_failed_login(self):
        """Incrémente les tentatives échouées"""
        self.failed_login_attempts += 1
        
        # Verrouiller après 5 tentatives
        if self.failed_login_attempts >= 5:
            self.locked_until = datetime.utcnow() + timedelta(minutes=30)
        
        db.session.commit()
    
    def reset_failed_login(self):
        """Reset après login réussi"""
        self.failed_login_attempts = 0
        self.locked_until = None
        self.last_login = datetime.utcnow()
        db.session.commit()


# ============================================================================
# ROUTES
# ============================================================================

@app.route('/api/register', methods=['POST'])
def register():
    """Inscription d'un nouvel utilisateur"""
    data = request.get_json()
    
    # Validation
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    # Vérifier si l'email existe déjà
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    try:
        # Créer l'utilisateur
        user = User(email=data['email'])
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'user_id': user.id
        }), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500


@app.route('/api/login', methods=['POST'])
def login():
    """Connexion utilisateur"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    # Timing attack protection : toujours vérifier le mot de passe
    # même si l'utilisateur n'existe pas
    if not user:
        bcrypt.generate_password_hash('dummy').decode('utf-8')
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Vérifier si le compte est actif
    if not user.is_active:
        return jsonify({'error': 'Account deactivated'}), 403
    
    # Vérifier si le compte est verrouillé
    if user.is_locked():
        return jsonify({
            'error': 'Account locked due to too many failed attempts',
            'locked_until': user.locked_until.isoformat()
        }), 423
    
    # Vérifier le mot de passe
    if not user.check_password(data['password']):
        user.increment_failed_login()
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Login réussi
    user.reset_failed_login()
    
    # Créer la session
    session['user_id'] = user.id
    session['email'] = user.email
    session['is_admin'] = user.is_admin
    
    return jsonify({
        'message': 'Logged in successfully',
        'user': {
            'id': user.id,
            'email': user.email,
            'is_admin': user.is_admin
        }
    }), 200


@app.route('/api/logout', methods=['POST'])
def logout():
    """Déconnexion"""
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200


@app.route('/api/profile')
def profile():
    """Profil utilisateur (requiert authentication)"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = User.query.get(session['user_id'])
    
    if not user:
        session.clear()
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'email': user.email,
        'is_admin': user.is_admin,
        'created_at': user.created_at.isoformat(),
        'last_login': user.last_login.isoformat() if user.last_login else None
    }), 200


@app.route('/api/change-password', methods=['POST'])
def change_password():
    """Changement de mot de passe"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    if not data or not data.get('old_password') or not data.get('new_password'):
        return jsonify({'error': 'Old and new passwords required'}), 400
    
    user = User.query.get(session['user_id'])
    
    # Vérifier l'ancien mot de passe
    if not user.check_password(data['old_password']):
        return jsonify({'error': 'Invalid old password'}), 401
    
    try:
        # Changer le mot de passe
        user.set_password(data['new_password'])
        db.session.commit()
        
        return jsonify({'message': 'Password changed successfully'}), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
```

### 2.3 JWT (JSON Web Tokens)

**Qu'est-ce qu'un JWT ?**

> **JWT est un standard pour transmettre des informations de manière sécurisée entre parties sous forme de JSON.**

**Structure d'un JWT :**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

HEADER.PAYLOAD.SIGNATURE
```

**Implémentation avec Flask-JWT-Extended :**

```python
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from datetime import timedelta

app = Flask(__name__)

# Configuration JWT
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Changer en production!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

jwt = JWTManager(app)


# Liste noire pour tokens révoqués
token_blocklist = set()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    """Vérifie si le token est dans la liste noire"""
    jti = jwt_payload['jti']
    return jti in token_blocklist


@app.route('/api/login', methods=['POST'])
def login():
    """Login avec JWT"""
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    
    # Vérifier credentials
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Créer les tokens
    access_token = create_access_token(
        identity=user.id,
        additional_claims={'email': user.email, 'is_admin': user.is_admin}
    )
    
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200


@app.route('/api/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Rafraîchir le token d'accès"""
    current_user = get_jwt_identity()
    
    new_access_token = create_access_token(identity=current_user)
    
    return jsonify({'access_token': new_access_token}), 200


@app.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout - ajoute le token à la liste noire"""
    jti = get_jwt()['jti']
    token_blocklist.add(jti)
    
    return jsonify({'message': 'Logged out successfully'}), 200


@app.route('/api/protected')
@jwt_required()
def protected():
    """Route protégée nécessitant un JWT valide"""
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    
    return jsonify({
        'logged_in_as': current_user_id,
        'email': claims.get('email'),
        'is_admin': claims.get('is_admin')
    }), 200


@app.route('/api/admin-only')
@jwt_required()
def admin_only():
    """Route accessible seulement aux admins"""
    claims = get_jwt()
    
    if not claims.get('is_admin'):
        return jsonify({'error': 'Admin access required'}), 403
    
    return jsonify({'message': 'Welcome admin!'}), 200
```

**Utilisation du JWT côté client :**

```javascript
// Login
const response = await fetch('/api/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({email: 'user@ua.fr', password: 'password123'})
});

const data = await response.json();
const accessToken = data.access_token;
const refreshToken = data.refresh_token;

// Stocker les tokens
localStorage.setItem('access_token', accessToken);
localStorage.setItem('refresh_token', refreshToken);

// Utiliser le token pour les requêtes
const protectedResponse = await fetch('/api/protected', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});

// Rafraîchir le token quand il expire
const refreshResponse = await fetch('/api/refresh', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${refreshToken}`
  }
});
```

---

## 3. Authorization (Autorisation)

### 3.1 Qu'est-ce que l'Authorization ?

> **L'authorization vérifie les permissions : "Que pouvez-vous faire ?"**

**Difference Authentication vs Authorization :**
- **Authentication** : Qui êtes-vous ? (Login)
- **Authorization** : Que pouvez-vous faire ? (Permissions)

### 3.2 Role-Based Access Control (RBAC)

**Implémentation :**

```python
from enum import Enum
from functools import wraps
from flask import g, jsonify


class Role(Enum):
    """Rôles utilisateur"""
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"


class Permission(Enum):
    """Permissions"""
    READ_PROFILE = "read_profile"
    EDIT_PROFILE = "edit_profile"
    DELETE_PROFILE = "delete_profile"
    READ_GRADES = "read_grades"
    EDIT_GRADES = "edit_grades"
    MANAGE_USERS = "manage_users"


# Mapping rôles → permissions
ROLE_PERMISSIONS = {
    Role.STUDENT: [
        Permission.READ_PROFILE,
        Permission.EDIT_PROFILE,
        Permission.READ_GRADES
    ],
    Role.TEACHER: [
        Permission.READ_PROFILE,
        Permission.EDIT_PROFILE,
        Permission.READ_GRADES,
        Permission.EDIT_GRADES
    ],
    Role.ADMIN: [
        Permission.READ_PROFILE,
        Permission.EDIT_PROFILE,
        Permission.DELETE_PROFILE,
        Permission.READ_GRADES,
        Permission.EDIT_GRADES,
        Permission.MANAGE_USERS
    ]
}


class User(db.Model):
    """Utilisateur avec rôle"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    role = db.Column(db.Enum(Role), default=Role.STUDENT)
    
    def has_permission(self, permission: Permission) -> bool:
        """Vérifie si l'utilisateur a une permission"""
        return permission in ROLE_PERMISSIONS.get(self.role, [])


def require_permission(permission: Permission):
    """Décorateur pour vérifier les permissions"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.user:
                return jsonify({'error': 'Unauthorized'}), 401
            
            if not g.user.has_permission(permission):
                return jsonify({'error': 'Forbidden - Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# Utilisation
@app.route('/api/grades/<int:student_id>', methods=['POST'])
@jwt_required()
@require_permission(Permission.EDIT_GRADES)
def update_grade(student_id):
    """Seuls teachers et admins peuvent modifier les notes"""
    # Logique...
    return jsonify({'message': 'Grade updated'})


@app.route('/api/users', methods=['DELETE'])
@jwt_required()
@require_permission(Permission.MANAGE_USERS)
def delete_user():
    """Seuls les admins peuvent supprimer des utilisateurs"""
    # Logique...
    return jsonify({'message': 'User deleted'})
```

---

## Résumé Partie 1

### Ce que nous avons vu

✅ **OWASP Top 10** : Vulnérabilités critiques  
✅ **Injection SQL** : Protection avec ORM  
✅ **Access Control** : Vérifications de permissions  
✅ **Password Security** : Hashing avec bcrypt  
✅ **Authentication** : Session et JWT  
✅ **Authorization** : RBAC et permissions  

### Concepts clés

- **Authentication** ≠ Authorization
- **Hashing** > Encryption pour mots de passe
- **JWT** = Stateless authentication
- **RBAC** = Role-Based Access Control
- **Least Privilege** = Permissions minimales

### Dans la Partie 2, nous verrons :

- CORS et CSRF
- XSS (Cross-Site Scripting)
- Sécurité des API
- Rate Limiting
- Audit et Logging de sécurité
- Cas pratiques complets

---

*Suite dans la Partie 2...*