from flask_restful import Resource
from flask_restful import abort
from flask import request
from hcloud.server.api.error import ApiException
from hcloud.server.api.alert.controller import AlertManager
from hcloud.server.api.alert.controller import Ansible
from hcloud.server.api.alert.controller import Promethues
from hcloud.server.api.alert.views import AlertRulesViews
from hcloud.utils import logging



class SendToAlert(Resource):
    def post(self):
        try:
            json_data = request.get_json(force=True)
            AlertManager.send(json_data)
        except Exception as e:
            abort(501, message=str(e), error="Alert post error")


class AlertRules(Resource):

    alert_rules_parser = AlertRulesViews.parser

    def post(self):
        args = AlertRules.alert_rules_parser.parse_args()
        host_id = args['host_id']
        port = args['port']
        service = args['service']
        monitor_items = args['monitor_items']
        statistical_period = args['statistical_period']
        statistical_approach = args['statistical_approach']
        compute_mode = args['compute_mode']
        threshold_value = args['threshold_value']
        #need write to config file
        url = 'http://localhost:9090'
        try:
            Ansible.check(host_id)
            inv_file = Ansible.init_target_yaml(host_id)
            instance = host_id + ":" + str(port)
            yml_file = Ansible.init_metrics_yaml(service, monitor_items, host_id, instance, threshold_value, statistical_period, compute_mode)

            Ansible.execute(yml_file, inv_file)
            Promethues.reload(url)

            data_res = AlertManager.create_alert_rules(host_id, service, monitor_items,
                                                       statistical_period, statistical_approach, compute_mode, threshold_value)
        except Exception as e:
            logging.info(e)
            ApiException.handler_hcloud_error(str(e))
        return {'status': 'ok'}, 201

    def put(self, alert_rules_id):
        args = AlertRules.alert_rules_parser.parse_args()
        statistical_period = args['statistical_period']
        statistical_approach = args['statistical_approach']
        compute_mode = args['compute_mode']
        threshold_value = args['threshold_value']
        try:
            data_res = AlertManager.update_alert_rules(alert_rules_id, statistical_period, statistical_approach, compute_mode, threshold_value)

        except Exception as e:
           ApiException.handler_hcloud_error(str(e))
        return {'status': 'ok'}, 201
