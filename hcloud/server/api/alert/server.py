from flask_restful import Resource
from flask_restful import abort
from flask import request
from hcloud.server.api.error import ApiException
from hcloud.server.api.alert.controller import AlertManager
from hcloud.server.api.alert.views import AlertRulesViews
from hcloud.models.alert_rules import AlertRulesData

class SendToAlert(Resource):

    def post(self):
        try:
            json_data = request.get_json(force=True)
            AlertManager.send(json_data)
        except Exception as e:
            abort(501, message=str(e), error="Alert post error")
        return json_data


class AlertRules(Resource):

    alert_rules_parser = AlertRulesViews.parser

    def post(self):
        args = AlertRulesViews.alert_rules_parser.parse_args()
        alert_rules_id = args['alert_rules_id']
        host_id = args['host_id']
        service = args['service']
        monitor_items = args['monitor_items']
        statistical_period = args['statistical_period']
        statistical_approach = args['statistical_approach']
        compute_mode = args['compute_mode']
        threshold_value = args['threshold_value']
        try:
            data_res = AlertManager.create_alert_rules(alert_rules_id, host_id, service, monitor_items, statistical_period,
                                             statistical_approach, compute_mode, threshold_value)
            #todo
            #add config
        except Exception as e:
            ApiException.handler_hcloud_error(str(e))
        return {'status': 'ok'}, 201

    def put(self,alert_rules_id):
        args = AlertRulesViews.alert_rules_parser.parse_args()
        statistical_period = args['statistical_period']
        statistical_approach = args['statistical_approach']
        compute_mode = args['compute_mode']
        threshold_value = args['threshold_value']
        try:
            data_res = AlertRulesData.update_alert_rules(alert_rules_id, statistical_period, statistical_approach, compute_mode, threshold_value)

        except Exception as e:
           ApiException.handler_hcloud_error(str(e))
        return {'status': 'ok'}, 201