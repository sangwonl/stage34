from celery.schedules import crontab
from datetime import timedelta


REDIS_URL = 'redis://0.0.0.0:6379/0'
BROKER_URL = [REDIS_URL]
CELERY_RESULT_BACKEND = REDIS_URL 
CELERY_IGNORE_RESULT = False
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_RESULT_EXPIRES = 10 * 1     # in seconds
#CELERY_DISABLE_RATE_LIMITS = True
CELERY_ACKS_LATE = False
CELERYD_PREFETCH_MULTIPLIER = 4
CELERYD_MAX_TASKS_PER_CHILD = 10        # pre-forked task pool
CELERYD_CONCURRENCY = 4                 # # of worker processes
CELERY_TIMEZONE = 'Asia/Seoul'
CELERYBEAT_SCHEDULE = {
    'hello-every-10s': {
        'task': 'tasks.hello.say_hello',
        'schedule': timedelta(seconds=10),
        'args': ('world',),
    },
}

# override proper config variables
# by importing custom config module
# matched to the environment variable, ENV 
try:
    from importlib import import_module
    import os
    env = os.environ.get('ENV', 'local')
    custom_conf = import_module('.' + env, __name__)
    for key in filter(lambda x: not x.startswith('__'), dir(custom_conf)):
        globals()[key] = getattr(custom_conf, key)
except (ImportError, AttributeError):
    pass
