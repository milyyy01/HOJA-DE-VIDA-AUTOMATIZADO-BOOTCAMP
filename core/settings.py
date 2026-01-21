"""
Django settings for core project.
Optimized for Local Development, Neon DB and Azure Storage.
"""
from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SEGURIDAD
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-clave-temporal-por-si-acaso')

# DEBUG: True para ver errores, cámbialo a False cuando todo esté listo
DEBUG = True

# Permitimos todos los hosts para evitar bloqueos en Azure
ALLOWED_HOSTS = ['*']

# Configuración crítica para permitir el login en Azure
CSRF_TRUSTED_ORIGINS = [
    'https://hoja-de-vida-emily-dkhhebakbfdvapdn.canadacentral-01.azurewebsites.net'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages', 
    'hoja_de_vida', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'

# =========================================================
# 1. CONFIGURACIÓN DE BASE DE DATOS (NEON)
# =========================================================
# Leemos la URL desde la variable de entorno para que GitHub no nos bloquee
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

# Validadores de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalización
LANGUAGE_CODE = 'es-ec'
TIME_ZONE = 'America/Guayaquil'
USE_I18N = True
USE_TZ = True

# =========================================================
# 2. ARCHIVOS ESTÁTICOS (CSS/JS) Y MEDIA (FOTOS)
# =========================================================
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Leemos la cadena de conexión desde Azure Environment Variables
AZURE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

# Configuración Fija de Azure
AZURE_ACCOUNT_NAME = 'trabajoemily'
AZURE_CONTAINER = 'media'
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'

# Configuración moderna de Almacenamiento (Django 4.2+)
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
            "connection_string": AZURE_CONNECTION_STRING,
            "azure_container": AZURE_CONTAINER,
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# URL pública para ver las fotos
MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'