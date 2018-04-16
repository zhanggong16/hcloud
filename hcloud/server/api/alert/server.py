import uuid
from flask_restful import Resource, marshal_with
from flask_restful import abort
from flask import request
from hcloud.exceptions import Error
from hcloud.server.api.alert.controller import AlertManager
from hcloud.server.api.alert.controller import Ansible
from hcloud.exceptions import ModelsDBError
from .views import AlertRulesViews



class SendToAlert(Resource):
    def post(self):
        try:
            json_data = request.get_json(force=True)
            AlertManager.send(json_data)
        except Exception as e:
            abort(501, message=str(e), error="Alert post error")


class AlertRules(Resource):

    alert_rules_data_fields = AlertRulesViews.alert_rules_data_fields
    alert_rules_parser = AlertRulesViews.parser

    @marshal_with(alert_rules_data_fields)
    def get(self, alert_rules_id):
        try:
            data_res = AlertManager.get_alert_rules(alert_rules_id)
        except Exception as e:
            raise ModelsDBError(str(e))
        return {'data': data_res, 'total': len(data_res)}

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
        try:
            # running
            alert_rules_id = str(uuid.uuid1())
            data_res = AlertManager.create_alert_rules(alert_rules_id, host_id, service, monitor_items,
                                                       statistical_period, statistical_approach, compute_mode,
                                                       threshold_value, 0)
            Ansible.check(host_id)
            inv_file = Ansible.init_target_yaml(host_id)
            instance = host_id + ":" + str(port)
            yml_file = Ansible.init_metrics_yaml(service, monitor_items, host_id, instance, threshold_value, statistical_period, compute_mode)
            Ansible.execute(yml_file, inv_file, alert_rules_id)
        except Exception as e:
            raise Error(e)
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
            raise Error(str(e))
        return {'status': 'ok'}, 201
