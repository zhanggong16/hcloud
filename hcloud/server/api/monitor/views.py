from flask_restful import reqparse
from flask_restful import fields
import datetime

class MonitorViews(object):

    #return data schema
    monitor_item_title_data_fields = {}
    monitor_item_title_data_fields['aggregation'] = fields.String(attribute='aggregation')
    monitor_item_title_data_fields['category'] = fields.String(attribute='category')
    monitor_item_title_data_fields['interval'] = fields.String(attribute='interval')
    monitor_item_title_data_fields['name'] = fields.String(attribute='name')
    monitor_item_title_data_fields['nick_name'] = fields.String(attribute='nick_name')
    monitor_item_title_data_fields['status'] = fields.String(attribute='status')
    monitor_item_title_data_fields['sub_name'] = fields.String(attribute='sub_name')
    monitor_item_title_data_fields['query'] = fields.String(attribute='query')    
    monitor_item_title_data_fields['unit'] = fields.String(attribute='unit')

    monitor_item_title_fields = {
        'message': fields.String(default='undefine'),
        'status': fields.String(),
        'data': fields.List(fields.Nested(monitor_item_title_data_fields))
    }
