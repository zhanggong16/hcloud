import subprocess
from hcloud.libs.celery.celery import celery

@celery.task
def async_cmd_task(cmd):
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
    except Exception as e:
        return {'status': -1, 'result': str(e)}
    return {'status': p_status, 'result': output.strip()}
