from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5z(r!k@3wongjbsvrrewd9xanx5k1hyj)mhkq5l&kii+0=z*bi'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blogMain',
    'blogAuth',
    'OnlineGame',
    'channels',
]
app_id = "2087904"
key = "e26f629e059816f35eaf"
secret = "52b8e668ee5bc6df29a8"
cluster = "ap1"
# Pusher 核心配置（替换为你的实际值）
PUSHER_APP_ID = app_id
PUSHER_KEY = key
PUSHER_SECRET = secret
PUSHER_CLUSTER = cluster
# 跨域设置（根据需要调整）
CORS_ALLOW_ALL_ORIGINS = True
# ASGI_APPLICATION = 'BlogWeb.asgi.application'
# CHANNEL_LAYERS = {
#     'default': {
#         # 本地开发用内存模式（生产环境用 Redis）
#         'BACKEND': 'channels.layers.InMemoryChannelLayer',
#         # 生产环境配置（需启动 Redis）
#         # 'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         # 'CONFIG': {
#         #     "hosts": [('127.0.0.1', 6379)],
#         # },
#     },
# }
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'BlogWeb.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [
                'django.templatetags.static',
            ],
        },
    },
]
WSGI_APPLICATION = 'BlogWeb.wsgi.application'
# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'IIZOM$default',
        'USER': 'IIZOM',
        'PASSWORD': 'Jjrjj3545wyx',
        'HOST': 'IIZOM.mysql.pythonanywhere-services.com',
        'PORT': '3306',
    }
}
# DATABASES = {
#     'default':{
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3', 
#     }
# }
# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'iizom <1739645729@qq.com>'
EMAIL_HOST_USER = '1739645729@qq.com'
EMAIL_HOST_PASSWORD = 'ydwbmvwvqbdddjji'
DEFAULT_FROM_EMAIL = '1739645729@qq.com'
LOGIN_URL = "/auth/login/"
