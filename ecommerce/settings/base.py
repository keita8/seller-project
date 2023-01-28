import os
from pathlib import Path
import dj_database_url
from decouple import Csv, config
import datetime 

BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# CORE SETTINGS
# ==============================================================================

SECRET_KEY = config("SECRET_KEY", default="django-insecure$simple.settings.local")

DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=Csv())

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'address',
    "tinymce",


    "ecommerce.apps.accounts",
    "ecommerce.apps.api",
    "ecommerce.apps.search",
    "ecommerce.apps.cart",
    "ecommerce.apps.products",
    "ecommerce.apps.upload",
    "phonenumber_field",
    # "django_address",
    'djmoney',
    'versatileimagefield',
    'import_export',
    
    
    #third part api services
    # 'algoliasearch_django',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    
    

]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ROOT_URLCONF = "ecommerce.urls"

INTERNAL_IPS = ["127.0.0.1"]

WSGI_APPLICATION = "ecommerce.wsgi.application"


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ecommerce.urls"

CORS_URLS_REGEX = r"^/api/.*$"

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8111',
    'https://localhost:8111',
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

if DEBUG:
    CORS_ALLOWED_ORIGINS += [
        'http://localhost:8111',
        'https://localhost:8111',
    ]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "ecommerce.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


LANGUAGE_CODE = config("LANGUAGE_CODE", default="fr-FR")

TIME_ZONE = config("TIME_ZONE", default="Africa/Casablanca")

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [BASE_DIR / "locale"]


STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static_my_proj")]
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "static_root")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "media_root")


# ==============================================================================
# STATIC FILES SETTINGS
# ==============================================================================

# STATIC_URL = "/static/"

# STATIC_ROOT = BASE_DIR.parent.parent / "static"

# STATICFILES_DIRS = [BASE_DIR / "static"]

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)


TINYMCE_DEFAULT_CONFIG = {
    "height": "320px",
    "width": "960px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
    "language": "fr_FR",  # To force a specific language instead of the Django current language.
}


#PHONENUMBER_DEFAULT_REGION = "US"
#
# AUTH_USER_MODEL = 'accounts.User'

# AUTHENTICATION_BACKENDS = [
# 'accounts.backends.EmailPhoneUsernameAuthenticationBackend'
# ]

# auth_classes =[
#         'rest_framework.authentication.SessionAuthentication',
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#         'ecommerce.apps.api.authentication.TokenAuthentication', 
# ]

# if DEBUG:
#    auth_classes =[
#        'ecommerce.apps.api.authentication.TokenAuthentication', 
#     ]
 

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':[
        'rest_framework.authentication.SessionAuthentication',
        'ecommerce.apps.api.authentication.TokenAuthentication', 
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS' : 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}

# ALGOLIA = {
#     'APPLICATION_ID': 'YWQL22FK3L',
#     'API_KEY': '8158070f245688cffe6e07da3bbb1bd7',
#     'INDEX_PREFIX': 'store'
# }

# ALGOLIA = {
#     'APPLICATION_ID': 'YWQL22FK3L',
#     'API_KEY': '8158070f245688cffe6e07da3bbb1bd7'
# }


SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ["Bearer"],
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(seconds=30),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(minutes=1),
}


AUTH_USER_MODEL = 'accounts.User'
