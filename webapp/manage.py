#!/usr/bin/env python
from celeryworker import app    # noqa

import os
import sys


if __name__ == '__main__':
    django_settings = 'main.settings.{}'.format(os.environ.get('ENV', 'local'))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', django_settings)

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
