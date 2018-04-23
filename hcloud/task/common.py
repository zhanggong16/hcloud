import subprocess
from hcloud.libs.celery.celery import celery
from hcloud.server.api.alert.ansible import Check
@celery.task
def push_alert(cmd, alert_rules_id):
    msg = ""
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        Check.check_result(output.strip(), alert_rules_id)
    except Exception as e:
        return {'status': -1, 'result': str(e)}

    return {'status': p_status, 'result': output.strip()}

def _push_alert_db():
    pass


@celery.task
def async_cmd_task(cmd):
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
    except Exception as e:
        return {'status': -1, 'result': str(e)}
    return {'status': p_status, 'result': output.strip()}
