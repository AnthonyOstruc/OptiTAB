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
    "dj_rest_auth",
    'storages',
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
    'subscriptions',
    'freecontent',
    'blog',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ========================================
# MIDDLEWARE
# ========================================

MIDDLEWARE = [
    # Sécurité et statiques (WhiteNoise) doivent arriver en tête
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    # CORS dès que possible après la sécurité
    'corsheaders.middleware.CorsMiddleware',

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

# DEBUG : toujours False sur Render; en local True par défaut (surchargable)
_debug_env = os.getenv("DEBUG")
_is_render = (
    os.getenv("RENDER", "").lower() == "true"
    or bool(os.getenv("RENDER_EXTERNAL_URL"))
    or bool(os.getenv("RENDER_SERVICE_NAME"))
)

if _is_render:
    DEBUG = False
else:
    if _debug_env is not None:
        DEBUG = _debug_env.lower() == "true"
    else:
        DEBUG = True

# ALLOWED_HOSTS : localhost pour dev, domaine Render en prod
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,optitab-backend.onrender.com,*.onrender.com,optitab.net,www.optitab.net").split(",")

# ========================================
# SECURITE (HTTPS / COOKIES / HSTS)
# ========================================

# Valeurs par defaut: activer la securite en prod, la desactiver en local
SECURE_SSL_REDIRECT = os.getenv(
    "SECURE_SSL_REDIRECT",
    "True" if not DEBUG else "False",
) == "True"
SESSION_COOKIE_SECURE = os.getenv(
    "SESSION_COOKIE_SECURE",
    "True" if not DEBUG else "False",
) == "True"
CSRF_COOKIE_SECURE = os.getenv(
    "CSRF_COOKIE_SECURE",
    "True" if not DEBUG else "False",
) == "True"

# HSTS: 1 an en prod par defaut, 0 en local
SECURE_HSTS_SECONDS = int(
    os.getenv("SECURE_HSTS_SECONDS", "31536000" if not DEBUG else "0")
)
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS",
    "True" if not DEBUG else "False",
) == "True"
SECURE_HSTS_PRELOAD = os.getenv(
    "SECURE_HSTS_PRELOAD",
    "True" if not DEBUG else "False",
) == "True"

if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    # Honorer les en-tetes proxy pour detecter HTTPS
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ========================================
# BASE DE DONNÉES
# ========================================

# DATABASE_URL : Render fournit l'URL complète (postgres://user:pass@host:port/dbname)
# En local et en prod, on accepte soit DATABASE_URL, soit des variables séparées (POSTGRES_* ou DB_*)
database_url_env = os.getenv("DATABASE_URL")

# Construire une URL Postgres à partir des variables classiques si présentes
pg_db = os.getenv("POSTGRES_DB") or os.getenv("DB_NAME")
pg_user = os.getenv("POSTGRES_USER") or os.getenv("DB_USER")
pg_password = os.getenv("POSTGRES_PASSWORD") or os.getenv("DB_PASSWORD")
pg_host = os.getenv("POSTGRES_HOST") or os.getenv("DB_HOST", "localhost")
pg_port = os.getenv("POSTGRES_PORT") or os.getenv("DB_PORT", "5432")

split_vars_url = None
if pg_db and pg_user and pg_password and pg_host:
    split_vars_url = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"

# Par défaut, on préfère les variables séparées si elles sont présentes
database_url = split_vars_url or database_url_env

db_ssl_required_env = os.getenv("DB_SSL_REQUIRED", "auto").lower()
if db_ssl_required_env not in ("true", "false", "auto"):
    db_ssl_required_env = "auto"

ssl_required = (db_ssl_required_env == "true") or (
    db_ssl_required_env == "auto" and not DEBUG
)

if database_url:
    DATABASES = {
        "default": dj_database_url.parse(
            database_url,
            conn_max_age=600,
            ssl_require=ssl_required
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

# Rendu DRF: Navigable en local, JSON uniquement en production
if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
    )
else:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer',
    )

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
    "https://optitab-frontend.onrender.com",
    "https://optitab.net",
    "https://www.optitab.net",
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\\.netlify\\.app$",
    r"^https://.*\\.onrender\\.com$",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept', 'accept-encoding', 'authorization', 'content-type',
    'dnt', 'origin', 'user-agent', 'x-csrftoken', 'x-requested-with',
    'x-ttclid', 'x-ttp', 'x-page-url', 'x-page-referrer',
]
CORS_ALLOW_METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS  = True

# ========================================
# EMAIL
# ========================================

# Permettre un override depuis l'environnement tout en gardant un fallback simple
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    'django.core.mail.backends.console.EmailBackend' if DEBUG else 'django.core.mail.backends.smtp.EmailBackend'
)
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "OptiTAB <contact@optitab.net>")

# URL absolue du logo utilisé dans les emails (ex: https://optitab.net/Logo_Fr.png)
# À définir dans l'environnement (.env) surtout en développement, car localhost n'est pas accessible par les clients mail
EMAIL_LOGO_URL = os.getenv("EMAIL_LOGO_URL")

# URL du frontend pour construire les liens d'action envoyés par email
FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:3000")
FRONTEND_URL = os.getenv("FRONTEND_URL", FRONTEND_BASE_URL)

# Allow OAuth users (without a usable password) to reset/set a password
DJANGO_REST_MULTITOKENAUTH_REQUIRE_USABLE_PASSWORD = False

# ========================================
# FICHIERS STATIQUES ET MÉDIA
# ========================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
# Permettre de surcharger le dossier médias en production via variable d'env
MEDIA_ROOT = Path(os.getenv('MEDIA_ROOT', BASE_DIR / 'media'))

# Utiliser WhiteNoise pour servir les fichiers statiques en production
# (Configuration compatible Django 5.x)
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

# ========================================
# CONFIGURATION AWS S3
# ========================================

# Configuration S3 (optionnel - seulement si les variables d'environnement sont définies)
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', 'optitab-media')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'eu-west-3')
AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN')

# Indicateur simple pour savoir si S3 est activé
S3_ENABLED = bool(AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY)

# Utiliser S3 pour les médias si les clés AWS sont configurées
if S3_ENABLED:
    # Configurer le stockage par défaut pour utiliser S3
    STORAGES['default'] = {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
        'OPTIONS': {
            'access_key': AWS_ACCESS_KEY_ID,
            'secret_key': AWS_SECRET_ACCESS_KEY,
            'bucket_name': AWS_STORAGE_BUCKET_NAME,
            'region_name': AWS_S3_REGION_NAME,
            'custom_domain': AWS_S3_CUSTOM_DOMAIN,
            # Les buckets "ACLs disabled" requièrent aucun ACL explicite
            'default_acl': None,
            # Rendre les URLs lisibles sans signature (objets doivent être publics via policy)
            'querystring_auth': False,
        }
    }

    # URL pour les médias S3
    if AWS_S3_CUSTOM_DOMAIN:
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
    else:
        MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/'


# Configuration pour les uploads de fichiers
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

# Taille maximale des fichiers uploadés (10MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

# Cache agressif côté client pour les assets versionnés
WHITENOISE_MAX_AGE = 31536000  # 1 an

# CSRF Trusted Origins (local + production)
CSRF_TRUSTED_ORIGINS = [
    'https://optitab.net',
    'https://www.optitab.net',
    'https://optitab-frontend.onrender.com',
    'https://optitab-backend.onrender.com',
    'http://localhost',
    'http://127.0.0.1',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'https://*.netlify.app',
    'https://*.onrender.com',
]

# ========================================
# CACHE
# ========================================

def _int_env(var_name, default):
    try:
        return int(os.getenv(var_name, str(default)))
    except (TypeError, ValueError):
        return default


# En production, eviter LocMem par defaut pour limiter les pics RAM.
# Valeurs possibles via CACHE_BACKEND: locmem | filebased | dummy
cache_backend = os.getenv(
    'CACHE_BACKEND',
    'locmem' if DEBUG else 'filebased'
).strip().lower()

if cache_backend == 'dummy':
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
elif cache_backend == 'filebased':
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': os.getenv('FILEBASED_CACHE_DIR', '/tmp/optitab-django-cache'),
            'TIMEOUT': _int_env('CACHE_DEFAULT_TIMEOUT', 300),
            'OPTIONS': {
                'MAX_ENTRIES': _int_env('CACHE_MAX_ENTRIES', 1000),
                'CULL_FREQUENCY': _int_env('CACHE_CULL_FREQUENCY', 3),
            },
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'opti-tab-local-cache',
            'TIMEOUT': _int_env('CACHE_DEFAULT_TIMEOUT', 300),
            'OPTIONS': {
                'MAX_ENTRIES': _int_env('CACHE_MAX_ENTRIES', 300),
                'CULL_FREQUENCY': _int_env('CACHE_CULL_FREQUENCY', 3),
            },
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
# LOGGING
# ========================================

# Réduire drastiquement le bruit en production. Garder le détail en local.
if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django.security': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': False,
            },
        },
    }

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
# CONFIGURATION TIKTOK EVENTS API
# ========================================
TIKTOK_PIXEL_ID = os.getenv('TIKTOK_PIXEL_ID', '').strip()
TIKTOK_EVENTS_API_ACCESS_TOKEN = os.getenv('TIKTOK_EVENTS_API_ACCESS_TOKEN', '').strip()
TIKTOK_EVENTS_API_URL = os.getenv(
    'TIKTOK_EVENTS_API_URL',
    'https://business-api.tiktok.com/open_api/v1.3/event/track/'
).strip()
TIKTOK_TEST_EVENT_CODE = os.getenv('TIKTOK_TEST_EVENT_CODE', '').strip()

try:
    TIKTOK_EVENTS_API_TIMEOUT_SECONDS = float(os.getenv('TIKTOK_EVENTS_API_TIMEOUT_SECONDS', '3'))
except (TypeError, ValueError):
    TIKTOK_EVENTS_API_TIMEOUT_SECONDS = 3.0

# ========================================
# CONFIGURATION PRODUCTION POUR RENDER
# ========================================

# Import pour la configuration Render
import dj_database_url

# Configuration Render (activée automatiquement en production)
if not DEBUG:
    # Configuration base de données Render (accepte DATABASE_URL ou POSTGRES_*)
    prod_database_url_env = os.getenv('DATABASE_URL')

    prod_pg_db = os.getenv("POSTGRES_DB") or os.getenv("DB_NAME")
    prod_pg_user = os.getenv("POSTGRES_USER") or os.getenv("DB_USER")
    prod_pg_password = os.getenv("POSTGRES_PASSWORD") or os.getenv("DB_PASSWORD")
    prod_pg_host = os.getenv("POSTGRES_HOST") or os.getenv("DB_HOST")
    prod_pg_port = os.getenv("POSTGRES_PORT") or os.getenv("DB_PORT", "5432")

    prod_split_vars_url = None
    if prod_pg_db and prod_pg_user and prod_pg_password and prod_pg_host:
        prod_split_vars_url = f"postgresql://{prod_pg_user}:{prod_pg_password}@{prod_pg_host}:{prod_pg_port}/{prod_pg_db}"

    prod_database_url = prod_split_vars_url or prod_database_url_env

    if prod_database_url:
        DATABASES['default'] = dj_database_url.parse(
            prod_database_url,
            conn_max_age=600,
            ssl_require=True
        )
    else:
        # Fallback configuration si aucune configuration n'est définie
        raise ImproperlyConfigured(
            "Database configuration is required in production. Set DATABASE_URL or POSTGRES_* variables in Render environment."
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
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Configuration HTTPS et securite definies plus haut (section SECURITE)
    # WhiteNoise compression/manifest déjà configurés via STORAGES
    # Les chemins de base restent identiques
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    # Ne pas écraser la configuration S3 si elle est active
    if not S3_ENABLED:
        MEDIA_URL = '/media/'
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    # Cache pour la production (optionnel)
    # CACHES = {
    #     'default': {
    #         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    #         'LOCATION': 'optitab-cache',
    #     }
    # }

