import re
import subprocess
from hcloud.libs.celery.celery import celery
from hcloud.models.alert_rules import AlertRulesData
from hcloud.utils import logging
from hcloud.libs.monitor import monitor

@celery.task
def async_ansible_task(cmd, alert_rules_id):
    msg = ""
    try:
        # p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        # (output, err) = p.communicate()
        # p_status = p.wait()
        popen = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        # check_results
        failed_count = 0
        unreachable_count = 0
        tmp = []
        while True:
            line = popen.stdout.readline().replace('*', '').strip()
            if line != '':
                tmp.append(line)
                logging.info(tmp)
            if subprocess.Popen.poll(popen) is not None:
                break

        flag = False
        for x in tmp:
            p1 = re.compile(r'failed=(\d)')
            r1 = p1.search(x)
            p2 = re.compile(r'unreachable=(\d)')
            r2 = p2.search(x)
            if r1 is None or r2 is None:
                continue
            else:
                flag = True
            failed_count = int(r1.group(1))
            unreachable_count = int(r2.group(1))
            if failed_count != 0 or unreachable_count != 0:
                msg += " There are {0} ansible-playbook sub task run into error ".format(
                    failed_count + unreachable_count)

        if flag is False:
            msg += " ansible-playbook command execute failed. "
    except Exception as e:
        msg += str(e)

    try:
        if msg != "":
            logging.error(msg)
            AlertRulesData.update_status(alert_rules_id, 2)
        else:
            AlertRulesData.update_status(alert_rules_id, 1)
            url = 'http://localhost:9090'
            monitor.reload(url)
    except Exception as e:
        logging.error(e)

    return {'status': popen.wait(), 'result': msg}