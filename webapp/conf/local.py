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
