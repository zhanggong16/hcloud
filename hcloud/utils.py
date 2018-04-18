import os
import logging as lg
<<<<<<< HEAD
=======
from eventlet.green import subprocess
from hcloud.task.common import async_cmd_task
>>>>>>> 56de43e482cb327fb4a6a25aa65d9a9c77ef2c2d
from envcfg.json.hcloud import EXCEPTION_LOG_FILE


def logger():
    logname = EXCEPTION_LOG_FILE
    logpath = r'%s/logs' % os.getcwd()
    logfile = r'%s/%s' % (logpath, logname)
    if not os.path.isdir(logpath):
        os.mkdir(logpath)
    format = '%(asctime)s [%(filename)s][%(levelname)s] %(message)s'
    lg.basicConfig(level=lg.DEBUG, filename=logfile, filemode='a', format=format)
    logger = lg.getLogger()
    return logger


<<<<<<< HEAD
logging = logger()
=======
logging = logger()


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
>>>>>>> 56de43e482cb327fb4a6a25aa65d9a9c77ef2c2d
