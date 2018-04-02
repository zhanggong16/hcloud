from flask_restful import reqparse
from flask_restful import fields


class AlertRulesViews(object):
    # return data schema
    alert_rules_data_fields = {}
    alert_rules_data_fields['alert_rules_id'] = fields.String(attribute='alert_rules_id')
    alert_rules_data_fields['host_id'] = fields.String(attribute='host_id')
    alert_rules_data_fields['service'] = fields.String(attribute='service')
    alert_rules_data_fields['monitor_items'] = fields.String(attribute='monitor_items')
    alert_rules_data_fields['statistical_period'] = fields.String(attribute='statistical_period')
    alert_rules_data_fields['statistical_approach'] = fields.String(attribute='statistical_approach')
    alert_rules_data_fields['compute_mode'] = fields.String(attribute='compute_mode')
    alert_rules_data_fields['threshold_value'] = fields.String(attribute='threshold_value')
    alert_rules_data_fields['create_time'] = fields.String(attribute='create_time')
    alert_rules_data_fields['update_time'] = fields.String(attribute='update_time')


    # request data
    parser = reqparse.RequestParser()
    parser.add_argument('alert_rules_id', type=str, required=True)
    parser.add_argument('host_id', type=str, required=True)
    parser.add_argument('service', type=str, required=True)
    parser.add_argument('monitor_items', type=str, required=True)
    parser.add_argument('statistical_period', type=int, required=True)
    parser.add_argument('statistical_approach', type=int, required=True)
    parser.add_argument('compute_mode', type=int, required=True)
    parser.add_argument('threshold_value', type=int, required=True)
