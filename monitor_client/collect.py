#!/usr/bin/env python  
'''
date: 2018.4

--------------
node
    curl -s http://localhost:9100/metrics | curl --data-binary @- http://gateway:9091/metrics/job/node_group/instance/local_ip(eth0):9100

''' 
 
import os
import sys
import time
import fcntl
import psutil
import atexit
import struct
import socket
import logging
import threading
import subprocess
import ConfigParser
from signal import SIGTERM  
  

base_dir = os.path.split(os.path.realpath(__file__))[0]
script_name = os.path.basename(sys.argv[0]).split('.')[0]
pid_file = "%s/%s.pid" % (base_dir, script_name)
log_file = "%s/%s.log" % (base_dir, script_name)
config_file = "%s/%s.conf" % (base_dir, script_name)
libs_dir = "%s/libs"

support_kind_list = [
    'gateway',
    'node',
    'mysql',
    'summary'
]

def logger():
    format = '%(asctime)s [%(filename)s][%(levelname)s] %(message)s'
    logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode='a', format=format)
    logger = logging.getLogger()
    return logger

logging = logger()

###############

def _check():
    pass   

def _local_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915, # SIOCGIFADDR
                struct.pack('256s', ifname[:15])
                )[20:24])
    except Exception as e:
        return False

def _cmd_run(cmd):
    _pipe = subprocess.PIPE
    obj = subprocess.Popen(cmd, stdin=_pipe,
                           stdout=_pipe,
                           stderr=_pipe,
                           env=os.environ,
                           shell=True)
    result = obj.communicate()
    obj.stdin.close()
    _returncode = obj.returncode
    return _returncode, result

def _get_config(config_file):
    config_lst = []
    if os.path.isfile(config_file):
        cf = ConfigParser.ConfigParser()
        cf.read(config_file)
        for section in cf.sections():
            opt_dict = dict()
            if section not in support_kind_list:
                logging.warning("Config file %s: %s not support." % (config_file, section))
                continue
            for option in cf.options(section):
                opt_dict[option] = cf.get(section, option)
                opt_dict['kind'] = section
            if section == 'gateway':
                gateway_dict = opt_dict
            else:
                config_lst.append(opt_dict)
        return gateway_dict, config_lst
    else:
        raise CollectException("Config file %s not found." % config_file)

def _collect_data(kind_dict, gateway_dict):
    
    def _node(curl, ip_addr, node_port, gateway_host, gateway_port):
        ''' push node metrics '''
        job_name = 'node_group'
        cmd = ('{curl} -s http://{local_ip}:{port}/metrics | {curl} --data-binary @- '
            'http://{gateway_host}:{gateway_port}/metrics/job/{job_name}/instance/{local_ip}:{port}').format(curl=curl, local_ip=ip_addr, port=node_port, gateway_host=gateway_host, gateway_port=gateway_port, job_name=job_name)
        return _cmd_run(cmd)

    def _summary(curl, ip_addr, summary_port, gateway_host, gateway_port):
        ''' push summary metrics '''
        item_lst = ['cpu_process_num', 'cpu_physical_num', 'memory_total', 'disk_usage']
        job_name = 'summary'
        cmd_head = ('cat << EOF | {curl} --data-binary @- '
                'http://{gateway_host}:{gateway_port}/metrics/job/{job_name}/instance/{local_ip}:{port}').format(curl=curl, local_ip=ip_addr, port=summary_port, gateway_host=gateway_host, gateway_port=gateway_port, job_name=job_name)
        cmd_foot = '\nEOF'
        cmd_middle = ''
        cmd_middle_template = '''
            # TYPE {item} gauge
            {item} {value}'''
        for item in item_lst:
            if item == 'disk_usage':
                for p in psutil.disk_partitions():
                    device = p.device.split('/')[-1]
                    mountpoint = p.mountpoint
                    res = psutil.disk_usage(mountpoint).total
                    cmd_res = cmd_middle_template.format(item=device, value=res)
                    cmd_middle += cmd_res
            else:
                if item == 'cpu_process_num':
                    res = psutil.cpu_count()
                elif item == 'cpu_physical_num':
                    res = psutil.cpu_count(logical=False)
                elif item == 'memory_total':
                    mem = psutil.virtual_memory()
                    res = mem.total
                cmd_res = cmd_middle_template.format(item=item, value=res)
                cmd_middle += cmd_res
        cmd_total = cmd_head + cmd_middle + cmd_foot
        logging.error(cmd_total)
        return _cmd_run(cmd_total)
    
    ###
    gateway_host, gateway_port = gateway_dict['host'], gateway_dict['port']
    ip_addr = _local_ip('eth0') if _local_ip('eth0') else '127.0.0.1'
    curl = '/usr/bin/curl'
    while True:
        if kind_dict['kind'] == 'node':
            interval, node_port = kind_dict['interval'], kind_dict['port']
            try:
                code, res = _node(curl, ip_addr, node_port, gateway_host, gateway_port)
                if code == 0:
                    logging.info("Node data collection success.")
                else:
                    logging.error("Node data collection failed, check http://{local_ip}:{port}/metrics, {res}".format(local_ip=ip_addr, port=node_port, res=res))
            except Exception as e:
                raise CollectException("Node error:%s" % str(e))
            time.sleep(int(interval))        
        elif kind_dict['kind'] == 'summary':
            interval, summary_port = kind_dict['interval'], kind_dict['port']
            try:
                code, res = _summary(curl, ip_addr, summary_port, gateway_host, gateway_port)
                if code == 0:
                    logging.info("Summary data collection success.")
                else:
                    logging.error("Summary data collection failed.")
            except Exception as e:
                raise CollectException("Summary error:%s" % str(e))
            time.sleep(int(interval))
    
###############
class Daemon(object):  
    
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):  
        self.stdin = stdin  
        self.stdout = stdout  
        self.stderr = stderr  
        self.pidfile = pidfile  
    
    def _daemonize(self):  
        try:  
            pid = os.fork()    
            if pid > 0:  
                sys.exit(0)
        except OSError, e:  
            sys.stderr.write('fork #1 failed: %d (%s)\n' % (e.errno, e.strerror))  
            sys.exit(1)  
    
        os.chdir("/")      
        os.setsid()        
        os.umask(0)          
    
        try:  
            pid = os.fork() 
            if pid > 0:  
                sys.exit(0)  
        except OSError, e:  
            sys.stderr.write('fork #2 failed: %d (%s)\n' % (e.errno, e.strerror))  
            sys.exit(1)  
        
        sys.stdout.flush()  
        sys.stderr.flush()  
        si = file(self.stdin, 'r')  
        so = file(self.stdout, 'a+')  
        se = file(self.stderr, 'a+', 0)  
        os.dup2(si.fileno(), sys.stdin.fileno())  
        os.dup2(so.fileno(), sys.stdout.fileno())  
        os.dup2(se.fileno(), sys.stderr.fileno())  
         
        atexit.register(self.delpid)  
        pid = str(os.getpid())  
        file(self.pidfile,'w+').write('%s\n' % pid)  
    
    def delpid(self):  
        os.remove(self.pidfile)  
  
    def start(self):  
        try:  
            pf = file(self.pidfile,'r')  
            pid = int(pf.read().strip())  
            pf.close()  
        except IOError:  
            pid = None  
    
        if pid:  
            message = 'pidfile %s already exist. Daemon already running!\n'  
            sys.stderr.write(message % self.pidfile)  
            sys.exit(1)  
      
        self._daemonize()  
        self._run()  
  
    def stop(self):  
        try:  
            pf = file(self.pidfile,'r')  
            pid = int(pf.read().strip())  
            pf.close()  
        except IOError:  
            pid = None  
    
        if not pid:
            message = 'pidfile %s does not exist. Daemon not running!\n'  
            sys.stderr.write(message % self.pidfile)  
            return  
  
        try:  
            while 1:  
                os.kill(pid, SIGTERM)  
                time.sleep(0.1)  
        except OSError, err:  
            err = str(err)  
            if err.find('No such process') > 0:  
                if os.path.exists(self.pidfile):  
                    os.remove(self.pidfile)  
            else:  
                print str(err)  
                sys.exit(1)  
  
    def restart(self):  
        self.stop()  
        self.start()  


class CollectException(Exception):
    
    def __init__(self, msg):
        self.msg = msg
        logging.error("CollectException: %s" % str(msg))
        Exception.__init__(self)
    

class CollectDaemon(Daemon):
    
    def _run(self):
        gateway_dict, kind_list = _get_config(config_file)
        logging.info("Gateway items: %s" % gateway_dict)
        logging.info("Monitor items: %s" % kind_list)

        threads = []
        for i in range(len(kind_list)):
            kind = kind_list[i]
            t = threading.Thread(target=_collect_data, args=(kind, gateway_dict))
            threads.append(t)
        for i in range(len(kind_list)):
            threads[i].start()
        for i in range(len(kind_list)):
            threads[i].join()

###############

def main():

    daemon = CollectDaemon(pid_file)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print 'unknown command'
            sys.exit(2)
        sys.exit(0)
    else:
        print 'usage: %s start|stop|restart' % sys.argv[0]
        sys.exit(2)


if __name__ == '__main__':
    main()
