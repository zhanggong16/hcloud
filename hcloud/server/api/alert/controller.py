import os
from hcloud.models.alert_rules import AlertRulesData
from hcloud.exceptions import Error
from hcloud.task.ansible import async_ansible_task

YML_LOCATION = '/tmp/yaml_files/'
RULES_LOCATION = '/opt/monitor/server/rules/'

class AlertManager(object):
    @classmethod
    def send(cls, alertinfo):
        print alertinfo

    @classmethod
    def create_alert_rules(cls, *add):
        alert_rules_id, host_id, service, monitor_items, statistical_period, statistical_approach, compute_mode, threshold_value, status = add
        rs = AlertRulesData.add(alert_rules_id, host_id, service, monitor_items, statistical_period, statistical_approach, compute_mode, threshold_value, status)
        return rs

    @classmethod
    def update_alert_rules(cls, *update):
        alert_rules_id, statistical_period, statistical_approach, compute_mode, threshold_value = update
        rs = AlertRulesData.update(alert_rules_id,statistical_period, statistical_approach, compute_mode, threshold_value)
        return rs

    @classmethod
    def get_alert_rules(cls, alert_rules_id):
        rs = AlertRulesData.get_alert_rules(alert_rules_id)
        if rs:
            return [line.dump() for line in rs]
        else:
            return


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

    @classmethod
    def init_target_yaml(cls, host_ip):
        file_name = host_ip + ".inv"
        inv_file = YML_LOCATION + file_name
        fobj = None
        try:
            fobj = open(inv_file, 'w')
        except Exception, e:
            msg = "Can't open file {0}: {1}".format(inv_file, e)
            raise Error(msg)

        fobj.write("[target_host]\n")
        fobj.write(host_ip + "\n")
        fobj.close()
        return inv_file

    @classmethod
    def init_metrics_yaml(cls, service, metrics, host_ip, instance, threshold_value, statistical_period, compute_mode):

        file_name = host_ip + ".yml"
        yml_file = YML_LOCATION + file_name

        fobj = None
        try:
            fobj = open(yml_file, 'w')
        except Exception, e:
            msg = "Can't open file {0}: {1}".format(yml_file, e)
            raise Error(msg)

        fobj.write("---\n")
        fobj.write("- name: install target_host\n")
        fobj.write("  hosts: target_host\n")
        fobj.write("  remote_user: root\n")
        fobj.write("  vars:\n")
        fobj.write("    instance: {0}\n".format(instance))
        fobj.write("    threshold_value: {0}\n".format(threshold_value))
        fobj.write("    statistical_period: '{0}'\n".format(statistical_period))
        fobj.write("    compute_mode: '{0}'\n".format(compute_mode))
        fobj.write("  tasks:\n")
        yml_rules_path = os.path.abspath("hcloud/server/api/alert/files/")
        yml_rules_rec =  service + "_" + metrics + ".yml"
        dest_file = RULES_LOCATION + instance.replace(":", "_") + "_" + yml_rules_rec
        fobj.write("    - template: src=" + yml_rules_path + "/" + yml_rules_rec + " dest={0} mode=640 force=yes\n".format(dest_file))

        fobj.close()
        return yml_file

    @classmethod
    def async_cmd_run(cls, cmd, alert_rules_id, expires=3600):
        res = async_ansible_task.apply_async(args=[cmd, alert_rules_id, ], expires=expires)

    @classmethod
    def execute(cls, yml_file, inv_file, alert_rules_id):
        if os.path.exists(yml_file):
            cmd = "ansible-playbook {0} -i {1}".format(yml_file, inv_file)
            cls.async_cmd_run(cmd, alert_rules_id)
        else:
            msg = "Can't found {0}".format(yml_file)
            raise Error(msg)


