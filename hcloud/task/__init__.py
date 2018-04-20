CELERY_IMPORTS = ['hcloud.task.alert', 'hcloud.task.scheduled']

BEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'hcloud.task.scheduled.monitor_instance',
        'schedule': 100.0
    },
    }
