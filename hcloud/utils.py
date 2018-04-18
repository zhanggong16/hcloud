import os
from eventlet.green import subprocess
from hcloud.task.common import async_cmd_task
from hcloud.logger import logging

def async_cmd_run(cmd, expires=3600):
    res_dict = async_cmd_task.apply_async(args=[cmd, ], expires=expires)


def sync_cmd_run(cmd):
    _pipe = subprocess.PIPE
    obj = subprocess.Popen(cmd, stdin=_pipe,
                           stdout=_pipe,
                           stderr=_pipe,
                           env=os.environ,
                           shell=True)
    result = obj.communicate()
    obj.stdin.close()
    _returncode = obj.returncode
    if _returncode not in [0]:
        logging.error("Sync cmd:%s, status:%s, result:%s" % (cmd, _returncode, result))
    else:
        logging.info("Sync cmd:%s, status:%s, result:%s" % (cmd, _returncode, result))
    return result
