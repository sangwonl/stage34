from __future__ import absolute_import

from celery import shared_task


@shared_task(queue='q_default')
def say_hello(message):
    print 'Hello, %s' % message
