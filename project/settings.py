import os
import dj_database_url
from whitenoise import WhiteNoise

MIDDLEWARE = [
    # ...existing code...
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ...existing code...
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
