import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

LANGUAGES = {
    'en': 'English',
    'es': 'Español'
}

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    JSON_SORT_KEYS = False
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
