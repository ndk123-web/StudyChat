import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Static files configuration
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # Your development static files
STATIC_ROOT = BASE_DIR / "staticfiles"  # Static root for production
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Security settings (Turn off DEBUG in production)
DEBUG = False  # ❌ Never keep DEBUG=True in production

ALLOWED_HOSTS = ['.vercel.app', 'localhost', '127.0.0.1']

# Middleware (Add Whitenoise)
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # ✅ Add Whitenoise Middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

# Collect static files for production
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
