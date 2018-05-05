import uuid
import os
from hcloud.libs.monitor.monitor import m
from flask_restful import Resource, marshal_with
from flask import request
from hcloud.server.api.alert.controller import AlertManager
from hcloud.server.api.alert.controller import Ansible
from hcloud.exceptions import Error
from hcloud.exceptions import ModelsDBError
from .views import AlertRulesViews
from .views import AlertHistoryViews
from envcfg.json.hcloud import ALERT_MANAGER_PATH
from envcfg.json.hcloud import ALERT_MANAGER_URL
from envcfg.json.hcloud import RULES_LOCATION
from hcloud.config import MONITOR_SERVER_URL
from hcloud.utils import execute_command
from hcloud.models.alert_rules import AlertRulesData
import json
import datetime
from hcloud.logger import logging


class Alert(Resource):
    alert_history_data_fields = AlertHistoryViews.alert_history_fields

    def post(self):

        try:
            result = request.get_json(force=True)
            json_string = json.dumps(result)
            json_data = json.loads(json_string)
            alerts_info = json_data['alerts'][0]

            state = alerts_info['status']
            exported_instance = alerts_info['labels']['exported_instance']
            host_id = exported_instance.split(':')[0]
            port = int(exported_instance.split(':')[1])
            alertname = alerts_info['labels']['alertname']
            monitor_iterm = alertname.split('_')[1] + '_' + alertname.split('_')[2]
            service = alerts_info['labels']['service']

            # endsAt = alerts_info['endsAt'] #exec last time
            startsAt = alerts_info['startsAt']
            start_time = datetime.datetime.strptime(startsAt.split('.')[0], '%Y-%m-%dT%H:%M:%S')
            description = alerts_info['annotations']['description']
            current_value = description.split('=')[1]
            summary = alerts_info['annotations']['summary']
            last_time = 0
            alert_rules = AlertManager.get_alert_rules_by_name(monitor_iterm)
            alert_rules_id = alert_rules[1]
            contact_groups = alert_rules[11]

            status = AlertManager.send_alert(monitor_iterm, summary, description, contact_groups)

            data_res = AlertManager.create_alert(alert_rules_id, host_id, port, service, monitor_iterm,
                                                 start_time, current_value, last_time, state, contact_groups, status)
        except Exception as e:
            raise Error(e)
        return {'status': 'ok'}, 201

    @marshal_with(alert_history_data_fields)
    def get(self):
        try:
            data_res = AlertManager.get_alert_history_list()
        except Exception as e:
            raise ModelsDBError(str(e))
        return {'data': data_res}


class CreateAlertRules(Resource):
    alert_rules_data_fields = AlertRulesViews.alert_rules_fields
    alert_rules_parser = AlertRulesViews.parser

    def post(self):
        args = CreateAlertRules.alert_rules_parser.parse_args()
        host_id = args['host_id']
        port = args['port']
        service = args['service']
        monitor_items = args['monitor_items']
        statistical_period = args['statistical_period']
        statistical_approach = args['statistical_approach']
        compute_mode = args['compute_mode']
        threshold_value = args['threshold_value']
        # silence_time = args['silence_time']
        contact_groups = args['contact_groups']
        notify_type = args['notify_type']
        try:
            # running
            alert_rules_id = str(uuid.uuid1())
            # insert mysql
            data_res = AlertManager.create_alert_rules(alert_rules_id, host_id, port, service, monitor_items,
                                                       statistical_period, statistical_approach, compute_mode,
                                                       threshold_value, contact_groups, notify_type, 0)
            Ansible.check(host_id)
            inv_file = Ansible.init_target_yaml(host_id)
            instance = host_id + ":" + str(port)
            yml_file = Ansible.init_metrics_yaml(service, monitor_items, host_id, instance, threshold_value,
                                                 statistical_period, compute_mode)
            Ansible.execute(yml_file, inv_file, alert_rules_id)
        except Exception as e:
            raise Error(e)
        return {'status': 'ok'}, 201


class AlertRulesList(Resource):
    alert_rules_data_fields = AlertRulesViews.alert_rules_fields

    @marshal_with(alert_rules_data_fields)
    def get(self):
        try:
            data_res = AlertManager.get_alert_rules_list()
        except Exception as e:
            raise ModelsDBError(str(e))
        return {'data': data_res}


class AlertRules(Resource):
    alert_rules_data_fields = AlertRulesViews.alert_rules_fields

    @marshal_with(alert_rules_data_fields)
    def get(self, alert_rules_id):
        try:
            data_res = AlertManager.get_alert_rules_dict(alert_rules_id)
        except Exception as e:
            raise ModelsDBError(str(e))
        return {'data': data_res}

    def put(self, alert_rules_id):
        json_data = request.get_json(force=True)
        action = json_data['action']
        if action['method'] == 'modify':
            statistical_period = action['param']['statistical_period']
            # statistical_approach = action['param']['statistical_approach']
            compute_mode = action['param']['compute_mode']
            threshold_value = action['param']['threshold_value']
            contact_groups = action['param']['contact_groups']
            notify_type = action['param']['notify_type']
            try:
                data_res = AlertManager.update_alert_rules(alert_rules_id, statistical_period, compute_mode,
                                                           threshold_value, contact_groups, notify_type)
            except Exception as e:
                raise Error(str(e))
        elif action['method'] == 'disable':
            try:
                silence_time = action['param']['silence_time']
                silence_time_hour = str(silence_time) + 'h'
                data_res = AlertManager.get_alert_rules(alert_rules_id)
                alert_name = data_res['service'] + '_' + data_res['monitor_items'] + '_' + data_res[
                    'host_id'] + ':' + str(data_res['port'])

                silence_add = "{0}/amtool --alertmanager.url={1} silence add alertname={2} --expires={3}".format(
                    ALERT_MANAGER_PATH, ALERT_MANAGER_URL, alert_name, silence_time_hour)
                status, output, err = execute_command(silence_add)
                if status != 0 or output == None:
                    errmsg = "Execute silence add command error: %s" % err
                    raise Error(str(errmsg))

                AlertRulesData.update_silence_time(alert_rules_id, int(silence_time))
            except Exception as e:
                raise Error(str(e))
        elif action['method'] == 'enable':
            data_res = AlertManager.get_alert_rules(alert_rules_id)
            alert_name = data_res['service'] + '_' + data_res['monitor_items'] + '_' + data_res['host_id'] + ':' + str(
                data_res['port'])
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

            AlertRulesData.update_silence_time(alert_rules_id, 0)
        return {'status': 'ok'}, 201

    def delete(self, alert_rules_id):
        try:
            data_res = AlertManager.get_alert_rules(alert_rules_id)
            file_name = data_res['host_id'] + '_' + str(data_res['port']) + '_' + data_res['service'] + '_' + data_res[
                'monitor_items'] + '.yml'
            file_path = RULES_LOCATION + file_name
            os.remove(file_path)
            m.reload()

            AlertRulesData.delete_alert_rule(alert_rules_id)
        except Exception as e:
            raise Error(str(e))
        return {'status': 'ok'}, 201






