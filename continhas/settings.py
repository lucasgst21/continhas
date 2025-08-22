from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# --- Paths & Env ---
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=False)

# --- Security / App basics ---
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-change-me")
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"

# Em produção, inclua seu host aqui (ex.: "seuapp.onrender.com", "seu-dominio.com")
ALLOWED_HOSTS = [h.strip() for h in os.getenv(
    "DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1"
).split(",") if h.strip()]

# Para formulários em produção, use https e adicione seus domínios/hosts
# Ex.: "https://seuapp.onrender.com", "https://seu-dominio.com"
CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.getenv(
    "DJANGO_CSRF_TRUSTED", "http://localhost,http://127.0.0.1"
).split(",") if o.strip()]

# --- Installed Apps ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps do projeto
    "core",
]

# --- Middleware ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # estáticos no deploy
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --- URLs / WSGI / ASGI ---
ROOT_URLCONF = "continhas.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # usar templates do app (APP_DIRS=True)
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "continhas.wsgi.application"
ASGI_APPLICATION = "continhas.asgi.application"

# --- Database (DATABASE_URL > fallback SQLite) ---
DATABASES = {
    "default": dj_database_url.parse(
        os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
        ssl_require=False,
    )
}

# --- Password validation (padrão do Django) ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- I18N / TZ ---
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# --- Static files ---
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# Se quiser uma pasta local para seus estáticos (opcional):
# STATICFILES_DIRS = [BASE_DIR / "static"]

# WhiteNoise com compressão e manifest (cache busting) para produção
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# --- Defaults ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Auth redirects ---
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "login"

# --- Security extras para produção ---
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
# Opcional endurecer mais em produção:
# SECURE_SSL_REDIRECT = not DEBUG
# SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
# SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
# SECURE_HSTS_PRELOAD = not DEBUG
