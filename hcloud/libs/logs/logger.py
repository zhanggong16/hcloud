import os
import logging
from envcfg.json.hcloud import EXCEPTION_LOG_FILE

def error_logger():
    logname = EXCEPTION_LOG_FILE
    logpath = r'%s/logs' % os.getcwd()
    logfile = r'%s/%s' % (logpath, logname)
    if not os.path.isdir(logpath):
        os.system("mkdir -p %s" % logpath)
    format='%(asctime)s [%(filename)s][%(levelname)s] %(message)s'
    logging.basicConfig(level = logging.DEBUG, filename = logfile, filemode = 'a', format = format)
    logger = logging.getLogger()
    return logger

