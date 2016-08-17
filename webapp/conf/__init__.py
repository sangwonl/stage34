import os

HOME_DIR = os.path.join(os.path.dirname(__file__), os.pardir)

settings = {
    'cookie_secret': 'askdfjpo83q47r9haskldfjh8',
    'static_path': os.path.join(HOME_DIR, 'static'),
    'template_path': os.path.join(HOME_DIR, 'templates'),
    'database': {
        'engine': 'sqlite',
        'dbname': os.path.join(HOME_DIR, 'stage34.db'),
    },
    'github': {
        'client_id': '7f845815ccbc5c97d622',
        'client_secret': '026219920a2470dbe33af113afe8d781cd154c55',
        'scope': 'user:email,repo',
        'auth_url': 'https://github.com/login/oauth/authorize',
        'redirect_uri': 'http://localhost:8000/api/v1/auth/github/callback/'
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