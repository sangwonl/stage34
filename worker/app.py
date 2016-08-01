from celery import Celery


celery = Celery('tasks', include=['tasks'])

celery.config_from_object('conf')


if __name__ == '__main__':
    celery.start()
