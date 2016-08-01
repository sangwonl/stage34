REDIS_URL = 'redis://dh-ds-job-queue-001.fecep9.0001.apne1.cache.amazonaws.com:6379/0'
BROKER_URL = [REDIS_URL]
CELERY_RESULT_BACKEND = REDIS_URL
