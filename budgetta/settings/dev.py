from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
SECRET_KEY = 'g3-mo*$7%vi=_!l*^gqv-z+*wnn2b+u$@dg1$6-c40^3b%*&97'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
     }
}

INSTALLED_APPS = [
    # MY_APP

    'budgetta_app',
    'users',
    'bootstrap4',
    'bootstrap_modal_forms',
    'django_template_maths',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]