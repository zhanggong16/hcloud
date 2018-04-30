import os
from hcloud.libs.celery.celery import celery


@celery.task
def monitor_instance():
    os.system('echo zhanggong > /tmp/zhanggong')
