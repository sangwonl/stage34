import os

HOME_DIR = os.path.join(os.path.dirname(__file__), os.pardir)

settings = {
    'database': {
        'engine': 'sqlite',
        'dbname': os.path.join(HOME_DIR, 'stage34.db'),
    }
}
