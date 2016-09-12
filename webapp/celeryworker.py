from __future__ import absolute_import

from celery import Celery

import os

# set the default Django settings module for the 'celery' program.
django_settings = 'main.settings.{}'.format(os.environ.get('ENV', 'local'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', django_settings)

from django.conf import settings  # noqa

app = Celery('main')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


if __name__ == '__main__':
    print "using settings '{}'".format(django_settings) 
    app.start()
