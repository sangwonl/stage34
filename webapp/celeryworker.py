from __future__ import absolute_import

from celery import Celery

import os

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

from django.conf import settings  # noqa

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app = Celery('main')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


if __name__ == '__main__':
    app.start()
