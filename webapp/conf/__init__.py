import os


settings = {
    'cookie_secret': 'askdfjpo83q47r9haskldfjh8',
    'static_path': os.path.join(os.path.dirname(__file__), os.pardir, 'static'),
    'template_path': os.path.join(os.path.dirname(__file__), os.pardir, 'templates'),
}


try:
    from importlib import import_module
    env = os.environ.get('ENV', 'local')
    env_conf = import_module('.' + env, __name__)
    for k, v in env_conf.settings.iteritems():
        print k, v
        settings.update({k: v})
except (ImportError, AttributeError):
    pass