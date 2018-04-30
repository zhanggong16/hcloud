import os
import logging as lg
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

logging = logger()