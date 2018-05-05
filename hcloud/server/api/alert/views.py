from flask_restful import reqparse
from flask_restful import fields


class AlertRulesViews(object):
    # return data schema
    alert_rules_data_fields = {}
    alert_rules_data_fields['alert_rules_id'] = fields.String(attribute='alert_rules_id')
    alert_rules_data_fields['host_id'] = fields.String(attribute='host_id')
    alert_rules_data_fields['port'] = fields.String(attribute='port')
    alert_rules_data_fields['service'] = fields.String(attribute='service')
    alert_rules_data_fields['monitor_items'] = fields.String(attribute='monitor_items')
    alert_rules_data_fields['statistical_period'] = fields.String(attribute='statistical_period')
    alert_rules_data_fields['statistical_approach'] = fields.String(attribute='statistical_approach')
    alert_rules_data_fields['compute_mode'] = fields.String(attribute='compute_mode')
    alert_rules_data_fields['threshold_value'] = fields.String(attribute='threshold_value')
    alert_rules_data_fields['silence_time'] = fields.String(attribute='silence_time')
    alert_rules_data_fields['contact_groups'] = fields.String(attribute='contact_groups')
    alert_rules_data_fields['notify_type'] = fields.String(attribute='notify_type')
    alert_rules_data_fields['status'] = fields.String(attribute='status')
    alert_rules_data_fields['create_time'] = fields.String(attribute='create_time')
    alert_rules_data_fields['update_time'] = fields.String(attribute='update_time')

    alert_rules_fields = {
        'message': fields.String(default='undefine'),
        'status': fields.String(default='success'),
        'data': fields.List(fields.Nested(alert_rules_data_fields))
    }

    # request data
    parser = reqparse.RequestParser()
    parser.add_argument('host_id', type=str, required=True)
    parser.add_argument('port', type=int, required=True)
    parser.add_argument('service', type=str, required=True)
    parser.add_argument('monitor_items', type=str, required=True)
    parser.add_argument('statistical_period', type=str, required=True)
    parser.add_argument('statistical_approach', type=str, required=True)
    parser.add_argument('compute_mode', type=str, required=True)
    parser.add_argument('threshold_value', type=int, required=True)
    #parser.add_argument('silence_time', type=int, required=True)
    parser.add_argument('contact_groups', type=str, required=True)
    parser.add_argument('notify_type', type=int, required=True)


class AlertHistoryViews(object):
    # return data schema
    alert_history_data_fields = {}
    alert_history_data_fields['alert_rules_id'] = fields.String(attribute='alert_rules_id')
    alert_history_data_fields['host_id'] = fields.String(attribute='host_id')
    alert_history_data_fields['port'] = fields.String(attribute='port')
    alert_history_data_fields['service'] = fields.String(attribute='service')
    alert_history_data_fields['alert_time'] = fields.String(attribute='alert_time')
    alert_history_data_fields['monitor_items'] = fields.String(attribute='monitor_items')
    alert_history_data_fields['current_value'] = fields.String(attribute='current_value')
    alert_history_data_fields['last_time'] = fields.String(attribute='last_time')
    alert_history_data_fields['state'] = fields.String(attribute='state')
    alert_history_data_fields['contact_groups'] = fields.String(attribute='contact_groups')
    alert_history_data_fields['status'] = fields.String(attribute='status')

    alert_history_fields = {
        'message': fields.String(default='undefine'),
        'status': fields.String(default='success'),
        'data': fields.List(fields.Nested(alert_history_data_fields))
    }
