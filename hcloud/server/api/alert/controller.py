import os
from hcloud.libs.monitor.monitor import m
from hcloud.exceptions import Error
from hcloud.task.alert import push_alert
from hcloud.models.alert_rules import AlertRulesData
from hcloud.models.alerts import AlertsData
from hcloud.config import YML_LOCATION, RULES_LOCATION, RULES_FILE
from envcfg.json.hcloud import ALERT_MANAGER_PATH
from envcfg.json.hcloud import ALERT_MANAGER_URL
from hcloud.utils import execute_command
from hcloud.utils import write_to_file
from hcloud.config import MONITOR_SERVER_URL


class AlertManager(object):
    @classmethod
    def send_alert(cls, monitor_iterm, summary, description, contact_groups):
        status = 0
        return status

    @classmethod
    def create_alert(cls, *add):
        alert_rules_id, host_id, port, service, monitor_items, alert_time, current_value, last_time, state, contact_groups, status = add
        rs = AlertsData.add(alert_rules_id, host_id, port, service, monitor_items, alert_time,
                                current_value, last_time, state, contact_groups, status)
        return rs

    @classmethod
    def create_alert_rules(cls, *add):
        alert_rules_id, host_id, port, service, temp_name, monitor_items, statistical_period, statistical_approach, compute_mode, threshold_value, contact_groups, notify_type, status = add
        rs = AlertRulesData.add(alert_rules_id, host_id, port, service, temp_name, monitor_items, statistical_period, statistical_approach, compute_mode, threshold_value, contact_groups, notify_type, status)
        return rs

    @classmethod
    def update_alert_rules(cls, *update):
        alert_rules_id, statistical_period, compute_mode, threshold_value, contact_groups, notify_type, status = update
        rs = AlertRulesData.update(alert_rules_id, statistical_period, compute_mode, threshold_value, contact_groups, notify_type, status)
        return rs

    @classmethod
    def get_alert_rules(cls, alert_rules_id):
        rs = AlertRulesData.get_alert_rules(alert_rules_id)
        if rs:
            return rs
        else:
            return

    @classmethod
    def get_alert_rules_dict(cls, service_name):
        rs = AlertRulesData.show_alert_rules(service_name)
        if rs:
            return  [ line.dump() for line in rs ]
        else:
            return

    @classmethod
    def get_alert_rules_list(cls):
        rs = AlertRulesData.get_alert_rules_list()
        if rs:
            return [line.dump() for line in rs]
        else:
            return

    @classmethod
    def get_alert_rules_by_name(cls, host_id, port, monitor_items):
        rs = AlertRulesData.get_alert_rules_by_name(host_id, port, monitor_items)
        if rs:
            return rs
        else:
            return

    @classmethod
    def get_alert_history_list(cls):
        rs = AlertsData.get_alerts_list()
        if rs:
            return [line.dump() for line in rs]
        else:
            return

    @classmethod
    def delete_alert_rules(cls, file_name):
        file_path = RULES_LOCATION + file_name
        os.remove(file_path)
        m.reload()

    @classmethod
    def disable_alert(cls, alert_name, silence_time_hour):

        silence_add = "{0}/amtool --alertmanager.url={1} silence add alertname={2} --expires={3}".format(
            ALERT_MANAGER_PATH, ALERT_MANAGER_URL, alert_name, silence_time_hour)

        status, output, err = execute_command(silence_add)
        if status != 0 or output == None:
            errmsg = "Execute silence add command error: %s" % err
            raise Error(str(errmsg))

    @classmethod
    def enable_alert(cls, alert_name):
        silence_query = "{0}/amtool --alertmanager.url={1} silence query alertname={2}".format(ALERT_MANAGER_PATH,
                                                                                               ALERT_MANAGER_URL,
                                                                                               alert_name)
        status, output, err = execute_command(silence_query)
        if status != 0 or output == None:
            errmsg = "Execute silence query command error: %s" % err
            raise Error(str(errmsg))
        for line in output.split("\n"):
            if line == None or line == "":
                continue
            if not line.find('Matchers') == -1 or not line.find('Comment') == -1:
                continue
            else:
                id = line.split(' ')[0]

            silence_expire = "{0}/amtool --alertmanager.url={1} silence expire {2}".format(ALERT_MANAGER_PATH,
                                                                                           ALERT_MANAGER_URL, id)
            status, output, err = execute_command(silence_expire)
            if status != 0 or output == None:
                errmsg = "Execute silence expire command error: %s" % err
                raise Error(str(errmsg))

class Ansible(object):
    @classmethod
    def check(cls, host_ip):
        # try:
        #     s = paramiko.SSHClient()
        #     s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #     s.connect(host_ip, 22, "root")
        #     s.close()
        # except Exception, e:
        #     msg = "ssh to {0} fail: {1}".format(host_ip, e)
        #     ApiException.handler_hcloud_error(str(msg))

        if not os.path.exists(YML_LOCATION):
            os.makedirs(YML_LOCATION, 0755)

    # @classmethod
    # def init_target_yaml(cls, host_ip):
    #     file_name = host_ip + ".inv"
    #     inv_file = YML_LOCATION + file_name
    #     fobj = None
    #     try:
    #         fobj = open(inv_file, 'w')
    #     except Exception, e:
    #         msg = "Can't open file {0}: {1}".format(inv_file, e)
    #         raise Error(msg)
    #
    #     fobj.write("[target_host]\n")
    #     fobj.write(host_ip + "\n")
    #     fobj.close()
    #     return inv_file

    # @classmethod
    # def init_metrics_yaml(cls, service, metrics, host_ip, instance, threshold_value, statistical_period, compute_mode):
    #
    #     file_name = host_ip + ".yml"
    #     yml_file = YML_LOCATION + file_name
    #
    #     fobj = None
    #     try:
    #         fobj = open(yml_file, 'w')
    #     except Exception, e:
    #         msg = "Can't open file {0}: {1}".format(yml_file, e)
    #         raise Error(msg)
    #
    #     fobj.write("---\n")
    #     fobj.write("- name: install target_host\n")
    #     fobj.write("  hosts: target_host\n")
    #     fobj.write("  remote_user: root\n")
    #     fobj.write("  vars:\n")
    #     fobj.write("    instance: {0}\n".format(instance))
    #     fobj.write("    service: '{0}'\n".format(service))
    #     fobj.write("    monitor_items: '{0}'\n".format(metrics))
    #     fobj.write("    threshold_value: {0}\n".format(threshold_value))
    #     fobj.write("    statistical_period: '{0}'\n".format(statistical_period))
    #     fobj.write("    compute_mode: '{0}'\n".format(compute_mode))
    #     fobj.write("  tasks:\n")
    #     yml_rules_path = os.path.abspath("hcloud/server/api/alert/files/")
    #     yml_rules_rec = service + "_" + metrics + ".yml"
    #     dest_file = RULES_LOCATION + instance.replace(":", "_") + "_" + yml_rules_rec
    #     fobj.write \
    #         ("    - template: src=" + yml_rules_path + "/" + yml_rules_rec + " dest={0} mode=640 force=yes\n".format
    #         (dest_file))
    #
    #     fobj.close()
    #     return yml_file

    @classmethod
    def init_target_yaml(cls, target_host):
        file_name = target_host + ".inv"
        inv_file = YML_LOCATION + file_name

        target_yml = """
[target_host]
{0}

""".format(target_host)
        write_to_file(inv_file, target_yml)

        return inv_file

    @classmethod
    def init_metrics_yaml(cls, service, metrics, host_ip, instance, threshold_value, statistical_period, compute_mode):

        file_name = host_ip + '_' + metrics + ".yml"
        yml_file = YML_LOCATION + file_name

        yml_rules_rec = service + "_" + metrics + ".yml"
        dest_file = RULES_LOCATION + instance.replace(":", "_") + "_" + yml_rules_rec
        src_file = RULES_FILE + "/" + yml_rules_rec
        config_args_list = {"instance": instance,
                            "service": service,
                            "metrics": metrics,
                            "threshold_value": threshold_value,
                            "statistical_period": statistical_period,
                            "compute_mode": compute_mode,
                            "dest_file": dest_file,
                            "src_file": src_file
                            }

        metrics_yml = """
---
- name: install target_host
  hosts: target_host
  remote_user: root
  vars:
    instance: "%(instance)s"
    service: "%(service)s"
    monitor_items: "%(metrics)s"
    threshold_value: %(threshold_value)d
    statistical_period: "%(statistical_period)s"
    compute_mode: "%(compute_mode)s"
  tasks:
      - template: src=%(src_file)s dest=%(dest_file)s mode=640 force=yes"""%config_args_list

        write_to_file(yml_file, metrics_yml)

        return yml_file

    # @celery.task
    # def async_cmd_task(cmd, alert_rules_id):
    #     msg = ""
    #     try:
    #         # p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    #         # (output, err) = p.communicate()
    #         # p_status = p.wait()
    #         popen = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    #         #check_results
    #         failed_count = 0
    #         unreachable_count = 0
    #         tmp = []
    #         while True:
    #             line = popen.stdout.readline().replace('*', '').strip()
    #             if line != '':
    #                 tmp.append(line)
    #                 logging.info(tmp)
    #             if subprocess.Popen.poll(popen) is not None:
    #                 break
    #
    #         flag = False
    #         for x in tmp:
    #             p1 = re.compile(r'failed=(\d)')
    #             r1 = p1.search(x)
    #             p2 = re.compile(r'unreachable=(\d)')
    #             r2 = p2.search(x)
    #             if r1 is None or r2 is None:
    #                 continue
    #             else:
    #                 flag = True
    #             failed_count = int(r1.group(1))
    #             unreachable_count = int(r2.group(1))
    #             if failed_count != 0 or unreachable_count != 0:
    #                 msg += "There are {0} ansible-playbook sub task run into error".format(
    #                     failed_count + unreachable_count)
    #
    #         if flag is False:
    #             msg += "ansible-playbook command execute failed."
    #     except Exception as e:
    #         msg += str(e)
    #
    #     try:
    #         if msg != "":
    #             logging.error(msg)
    #             AlertRulesData.update_status(alert_rules_id, 2)
    #         else:
    #             AlertRulesData.update_status(alert_rules_id, 1)
    #             url = 'http://localhost:9090'
    #             Promethues.reload(url)
    #     except Exception as e:
    #         logging.error(e)
    #
    #     return {'status': popen.wait(), 'result': msg}

    # @classmethod
    # def async_cmd_run(cls, cmd, alert_rules_id, expires=3600):
    #    res = cls.async_cmd_task.apply_async(args=[cmd, alert_rules_id], expires=expires)

    @classmethod
    def execute(cls, yml_file, inv_file, alert_rules_id):
        if os.path.exists(yml_file):
            cmd = "ansible-playbook {0} -i {1}".format(yml_file, inv_file)
            # async_cmd_task.delay(cmd)
            # async_cmd_run(cmd)
            push_alert.delay(cmd, alert_rules_id)
        else:
            msg = "Can't found {0}".format(yml_file)
            raise Error(msg)
