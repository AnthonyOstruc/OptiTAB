"""
Configuration Django simplifiée et sécurisée
"""
import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from datetime import timedelta
from django.core.exceptions import ImproperlyConfigured

# ========================================
# CONFIGURATION DE BASE
# ========================================

BASE_DIR = Path(__file__).resolve().parent.parent


# Charge automatiquement le fichier .env le plus proche en remontant les dossiers
env_path = find_dotenv(filename='.env', usecwd=True)
if env_path:
    load_dotenv(env_path, override=True)
else:
    # Fallback: tente backend/.env si non trouvé
    load_dotenv(BASE_DIR / '.env', override=True)



# ========================================
# APPLICATIONS
# ========================================

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'django_rest_passwordreset',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

LOCAL_APPS = [
    'core',
    'users',
    'curriculum',
    'cours',
    'synthesis',
    'suivis',
    'calc',
    'quiz',
    'pays',
    'ai',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ========================================
# MIDDLEWARE
# ========================================

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# ========================================
# CONFIGURATION URLS ET TEMPLATES
# ========================================

ROOT_URLCONF = 'backendAPI.urls'
WSGI_APPLICATION = 'backendAPI.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # Templates globaux
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ========================================
# CONFIGURATION DE BASE
# ========================================

# SECRET_KEY : utilise la valeur de Render ou .env local, sinon valeur de dev
SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")

# DEBUG : True si local, False si Render (à configurer via variable d'environnement)
DEBUG = os.getenv("DEBUG", "False") == "False"

# ALLOWED_HOSTS : localhost pour dev, domaine Render en prod
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# ========================================
# BASE DE DONNÉES
# ========================================

# DATABASE_URL : Render fournit l'URL complète (postgres://user:pass@host:port/dbname)
# En local, on accepte soit DATABASE_URL, soit des variables séparées (POSTGRES_* ou DB_*)
database_url = os.getenv("DATABASE_URL")

if not database_url:
    # Construire une URL Postgres à partir des variables classiques si présentes
    pg_db = os.getenv("POSTGRES_DB") or os.getenv("DB_NAME")
    pg_user = os.getenv("POSTGRES_USER") or os.getenv("DB_USER")
    pg_password = os.getenv("POSTGRES_PASSWORD") or os.getenv("DB_PASSWORD")
    pg_host = os.getenv("POSTGRES_HOST") or os.getenv("DB_HOST", "localhost")
    pg_port = os.getenv("POSTGRES_PORT") or os.getenv("DB_PORT", "5432")

    if pg_db and pg_user and pg_password:
        database_url = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"

if database_url:
    DATABASES = {
        "default": dj_database_url.parse(
            database_url,
            conn_max_age=600,
            ssl_require=not DEBUG  # SSL requis seulement en prod
        )
    }
else:
    # Pas de fallback SQLite: forcer une configuration PostgreSQL explicite
    raise ImproperlyConfigured(
        "DATABASE configuration is missing. Set DATABASE_URL or POSTGRES_* / DB_* variables."
    )


# ========================================
# AUTHENTIFICATION
# ========================================

AUTH_USER_MODEL = 'users.CustomUser'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ========================================
# REST FRAMEWORK ET JWT
# ========================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # SessionAuthentication peut imposer le CSRF pour les appels non authentifiés
        # Sur les endpoints publics (ex: Google One Tap), on utilisera des vues avec authentication_classes = []
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ========================================
# CORS
# ========================================

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://optitab-frontend.onrender.com",
    "https://optitab.net",
    "https://www.optitab.net",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept', 'accept-encoding', 'authorization', 'content-type',
    'dnt', 'origin', 'user-agent', 'x-csrftoken', 'x-requested-with'
]
CORS_ALLOW_METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']

if DEBUG:
    CORS_ALLOW_ALL_HEADERS = True

# ========================================
# EMAIL
# ========================================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' if DEBUG else 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

# ========================================
# FICHIERS STATIQUES ET MÉDIA
# ========================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ========================================
# CACHE
# ========================================

# Cache en mémoire locale pour activer cache.set/get côté vues
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'opti-tab-local-cache',
    }
}

# ========================================
# INTERNATIONALISATION
# ========================================

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# ========================================
# AUTRES
# ========================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ========================================
# DJANGO-ALLAUTH CONFIGURATION
# ========================================

# Configuration de base pour django-allauth
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

# Configuration des providers sociaux
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
        'APP': {
            'client_id': os.getenv('GOOGLE_OAUTH_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_OAUTH_CLIENT_SECRET'),
            'key': ''
        }
    }
}

# Configuration minimale pour Google One Tap
SOCIALACCOUNT_AUTO_SIGNUP = True

# ========================================
# CONFIGURATION OPENAI
# ========================================
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# ========================================
# CONFIGURATION PRODUCTION POUR RENDER
# ========================================

# Import pour la configuration Render
import dj_database_url

# Configuration Render (activée automatiquement en production)
if not DEBUG:
    # Configuration base de données Render
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        DATABASES['default'] = dj_database_url.config(
            default=database_url,
            conn_max_age=600,
            ssl_require=True
        )
    else:
        # Fallback configuration si DATABASE_URL n'est pas défini
        raise ImproperlyConfigured(
            "DATABASE_URL environment variable is required in production. "
            "Please configure your database URL in the Render environment variables."
        )

    # Configuration des hosts autorisés pour Render
    ALLOWED_HOSTS = [
        'optitab.net',
        'www.optitab.net',
        'optitab-backend.onrender.com',
        '.onrender.com',
        'localhost',
        '127.0.0.1'
    ]

    # Configuration CORS pour la production
    CORS_ALLOWED_ORIGINS = [
        "https://optitab.net",
        "https://www.optitab.net",
        "https://optitab-frontend.onrender.com",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    # Configuration HTTPS et sécurité
    # Désactiver explicitement en développement, activer seulement en production explicite
    SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "False") == "True"
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False") == "True"
    CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "False") == "True"
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

    # Configuration des fichiers statiques pour Render
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    # Cache pour la production (optionnel)
    # CACHES = {
    #     'default': {
    #         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    #         'LOCATION': 'optitab-cache',
    #     }
    # }
