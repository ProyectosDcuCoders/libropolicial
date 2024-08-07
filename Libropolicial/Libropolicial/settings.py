from pathlib import Path

# Construye rutas dentro del proyecto como BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuraciones rápidas para el desarrollo - no adecuadas para producción
# Ver https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# ADVERTENCIA DE SEGURIDAD: mantén la clave secreta utilizada en producción en secreto.
SECRET_KEY = 'django-insecure-ds6h)mdg35#cm4ez5)**^%lwznbi2-4w#hth1oj2u8aq$zn*gm'

# ADVERTENCIA DE SEGURIDAD: no ejecutes con debug activado en producción.
DEBUG = True

ALLOWED_HOSTS = []

# Definición de la aplicación

INSTALLED_APPS = [
    'django.contrib.admin',  # Admin de Django
    'django.contrib.auth',  # Sistema de autenticación
    'django.contrib.contenttypes',  # Framework de tipos de contenido
    'django.contrib.sessions',  # Soporte para sesiones
    'django.contrib.messages',  # Framework de mensajes
    'django.contrib.staticfiles',  # Manejo de archivos estáticos
    'compartido',  # Aplicación compartida
    'comisarias',  # Aplicación de comisarías
    'comisariasriogrande',  # Aplicación de comisarías de Rio Grande
    'comisariastolhuin',  # Aplicación de comisarías de Tolhuin
    'divisioncomunicaciones',  # Aplicación de la división de comunicaciones
    'channels',  # Soporte para canales (WebSockets)
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Middleware de seguridad
    'django.contrib.sessions.middleware.SessionMiddleware',  # Middleware de sesiones
    'django.middleware.locale.LocaleMiddleware',  # Middleware de localización
    'django.middleware.common.CommonMiddleware',  # Middleware común
    'django.middleware.csrf.CsrfViewMiddleware',  # Middleware de CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Middleware de autenticación
    'django.contrib.messages.middleware.MessageMiddleware',  # Middleware de mensajes
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Middleware de protección contra clickjacking
    'compartido.middleware.NoCacheMiddleware',  # Middleware personalizado para no caché
    'compartido.middleware.RedirectAuthenticatedUserMiddleware',  # Middleware personalizado para redirigir usuarios autenticados
    'compartido.middleware.InactivityLogoutMiddleware',  # Middleware personalizado para cerrar sesión por inactividad
    # 'comisarias.middleware.NoCacheMiddleware',  # Añadir este middleware si es necesario
    # 'comisarias.middleware.RedirectAuthenticatedUserMiddleware',  # Añadir este middleware si es necesario
    # 'comisarias.middleware.InactivityLogoutMiddleware',  # Añadir este middleware si es necesario
]

ROOT_URLCONF = 'Libropolicial.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Backend de plantillas de Django
        'DIRS': [BASE_DIR / 'templates'],  # Añadir la ruta de la carpeta de plantillas
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Libropolicial.wsgi.application'
ASGI_APPLICATION = 'Libropolicial.asgi.application'

# Base de datos
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Utiliza el backend MySQL
        'NAME': 'librodeguardia',  # Nombre de la base de datos
        'USER': 'root',  # Usuario de la base de datos
        'PASSWORD': '',  # Contraseña de la base de datos
        'HOST': 'localhost',  # Host de la base de datos
        'PORT': '3306',  # Puerto de la base de datos
    }
}

# Validación de contraseñas
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# Internacionalización
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-ar'  # Código de idioma para español de Argentina

TIME_ZONE = 'America/Argentina/Buenos_Aires'  # Zona horaria

USE_TZ = False  # Desactiva el uso de la zona horaria UTC
USE_I18N = True  # Habilita la internacionalización
USE_L10N = True  # Habilita la localización

# Archivos estáticos (CSS, JavaScript, Imágenes)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'  # URL para archivos estáticos
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Directorio de archivos estáticos
]

# Tipo de campo de clave primaria predeterminado
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de URL de inicio de sesión
LOGIN_URL = 'login'  # URL de inicio de sesión

# Configuración del motor de sesiones
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Configuración de canales (WebSockets)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}
