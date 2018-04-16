import subprocess
from hcloud.task.common import async_cmd_task

def async_cmd_run(cmd, expires=3600):
    res_dict = async_cmd_task.apply_async(args=[cmd, ], expires=expires)


def sync_cmd_run(cmd):
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
    except Exception as e:
        return {'status': -1, 'result': str(e)}
        logging.error("Sync cmd:%s, status:%s, result:%s" % (cmd, -1, str(e)))
    if p_status == 0:
        logging.info("Sync cmd:%s, status:%s, result:%s" % (cmd, p_status, output.strip()))
    else:
        logging.error("Sync cmd:%s, status:%s, result:%s" % (cmd, p_status, output.strip()))
    return {'status': p_status, 'result': output.strip()}