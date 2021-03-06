from __future__ import absolute_import
from celery import Celery
from hcloud import config
from hcloud.task import CELERY_IMPORTS, BEAT_SCHEDULE

def _get_celery_app():
    celery_app = Celery('hcloud', broker=config.CELERY_BROKER_URL)
    celery_app.config_from_object(config)
    celery_app.conf.update(CELERY_IMPORTS=CELERY_IMPORTS)
    celery_app.conf.beat_schedule = BEAT_SCHEDULE
    return celery_app


def _get_celery():
    if not getattr(_get_celery, '_celery', None):
        celery_ = _get_celery_app()
        _get_celery._celery = celery_
    return _get_celery._celery

celery = _get_celery()
