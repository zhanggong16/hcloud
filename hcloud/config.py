import os
from envcfg.json.hcloud import HTTP_PORT
from envcfg.json.hcloud import DEBUG
from envcfg.json.hcloud import MYSQL_DSN
from envcfg.json.hcloud import EXCEPTION_LOG_FILE
from envcfg.json.hcloud import CELERY_RESULT_BACKEND
from envcfg.json.hcloud import CELERY_BROKER_URL
from envcfg.json.hcloud import CELERY_LOGLEVEL
from envcfg.json.hcloud import CELERY_LOG_FILE


APP = 'hcloud'

__all__ = [
    'HTTP_PORT',
    'DEBUG',
    'MYSQL_DSN',
    'EXCEPTION_LOG_FILE',
    'CELERY_RESULT_BACKEND',
    'CELERY_BROKER_URL',
    'CELERY_LOGLEVEL',
    'CELERY_LOG_FILE'
]

YML_LOCATION = '/tmp/yaml_files/'
RULES_LOCATION = '/opt/monitor/server/rules/'
MONITOR_SERVER = '192.168.0.92'
MONITOR_SERVER_URL = 'http://localhost:9090'
ALERT_MANAGER_PATH = '/opt/monitor/alertmanager'
ALERT_MANAGER_URL = 'http://localhost:9093'
RULES_FILE = os.path.abspath("hcloud/server/api/alert/files/")