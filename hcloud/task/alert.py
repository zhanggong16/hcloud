from hcloud.utils import cmd_run
from hcloud.libs.celery.celery import celery
from hcloud.server.api.alert.ansible import Check

@celery.task
def push_alert(cmd, alert_rules_id):
    try:
        status, res = cmd_run(cmd)
        Check.check_result(res[0], alert_rules_id)
    except Exception as e:
        return {'status': -1, 'result': str(e)}
    return {'status': status, 'result': res[0]}

def _xxxxx():
    pass
