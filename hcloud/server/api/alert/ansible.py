import re
from hcloud.libs.monitor.monitor import m
from hcloud.logger import logging
from hcloud.models.alert_rules import AlertRulesData

class Check(object):
    @classmethod
    def check_result(cls, output, alert_rules_id):
        msg = ""
        logging.info(output.strip())
        #logging.info("debug******************1")
        try:
            for x in output.replace('*', '').strip().split("\n"):
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
                    msg += "There are {0} ansible-playbook sub task run into error".format(
                        failed_count + unreachable_count)
            if flag is False:
                msg += "ansible-playbook command execute failed."

        except Exception as e:
            # return {'status': -1, 'result': str(e)}
            msg += str(e)

        try:
            if msg != "":
                logging.error(msg)
                #AlertRulesData.update_status(alert_rules_id, 2)
                AlertRulesData.delete_alert_rule(alert_rules_id)
            else:
                AlertRulesData.update_status(alert_rules_id, 1)
                m.reload()
        except Exception as e:
            logging.error(e)