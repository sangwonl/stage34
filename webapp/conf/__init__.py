import os

HOME_DIR = os.path.join(os.path.dirname(__file__), os.pardir)

settings = {
    'cookie_secret': 'askdfjpo83q47r9haskldfjh8',
    'static_path': os.path.join(HOME_DIR, 'static'),
    'template_path': os.path.join(HOME_DIR, 'templates'),
    'database': {
        'engine': 'sqlite',
        'dbname': os.path.join(HOME_DIR, 'stage34.db'),
    }
}


try:
    from importlib import import_module
    env = os.environ.get('ENV', 'local')
    env_conf = import_module('.' + env, __name__)
    for k, v in env_conf.settings.iteritems():
        settings.update({k: v})
except (ImportError, AttributeError):
    pass