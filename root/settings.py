"""
Django settings for root project.

Generated by 'django-admin startproject' using Django 5.0.9.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
from os.path import join, dirname
from typing import TypedDict, List, Literal
import logging
import os
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-_gol%tpw+nh%k0fnsla1mjh!f@n(z0#a3f-xb8$nsuz6&0rz2="

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

class Environtment_Variables(TypedDict):
    EMBEDDING_MODEL: str
    LLM_MODEL: str
    DATA_URLS: List[str]
    CACHE_PATH: str


def load_env() -> Environtment_Variables:
    """
    Loads and returns the environment variables as a dictionary
    """

    dotenv_path = join(dirname(__file__), '../.env')
    logger.info("file: vector_store function: load_env loading the environment")

    try:
        load_dotenv(dotenv_path)
    except Exception as err:
        logger.warn(f"file: vector_store function: load_env could not load environment variables with error: {err}")

    default_embedding_model = "BAAI/bge-small-en-v1.5"
    default_llm_model = ""
    default_data_urls = ""
    default_cache_path = "cache"
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', default_embedding_model)
    LLM_MODEL = os.getenv('LLM_MODEL', default_llm_model)
    DATA_URLS = os.getenv('DATA_URLS', default_data_urls).split(',')
    CACHE_PATH = os.getenv("CACHE_PATH", default_cache_path)
    logger.info(f"EMBEDDING_MODEL: {EMBEDDING_MODEL}, LLM_MODEL: {LLM_MODEL}, DATA_URLS: {DATA_URLS}")
    return {
        'EMBEDDING_MODEL': EMBEDDING_MODEL,
        'LLM_MODEL': LLM_MODEL,
        'DATA_URLS': DATA_URLS,
        "CACHE_PATH": CACHE_PATH,
    }

environment_variables = load_env()



# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "root.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "root.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
