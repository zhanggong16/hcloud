CELERY_IMPORTS = ['hcloud.task.alert', 'hcloud.task.scheduled']

BEAT_SCHEDULE = {
    'monitor_instance-every-30-seconds': {
        'task': 'hcloud.task.scheduled.monitor_instance',
        'schedule': 30.0
    },
    }
