from app import celery


@celery.task(queue='q_default')
def say_hello(message):
    print 'Hello, %s' % message
