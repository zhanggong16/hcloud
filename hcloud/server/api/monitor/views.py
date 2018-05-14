from flask_restful import reqparse
from flask_restful import fields

class MonitorViews(object):

    #return data schema
    monitor_item_title_data_fields = {}
    monitor_item_title_data_fields['aggregation'] = fields.String(attribute='aggregation')
    monitor_item_title_data_fields['category'] = fields.String(attribute='category')
    monitor_item_title_data_fields['interval'] = fields.String(attribute='interval')
    monitor_item_title_data_fields['name'] = fields.String(attribute='name')
    monitor_item_title_data_fields['nick_name'] = fields.String(attribute='nick_name')
    monitor_item_title_data_fields['status'] = fields.String(attribute='status')
    
    monitor_item_title_fields = {
        'message': fields.String(default='undefine'),
        'status': fields.String(default='success'),
        'data': fields.List(fields.Nested(monitor_item_title_data_fields))
    }

    
    #hostlist post request data
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('device_key', type=str)
    parser.add_argument('dns', type=str)
    parser.add_argument('project_id', type=str)
    parser.add_argument('privateip', type=str, required=True)
    parser.add_argument('os_type', type=int, required=True)
    parser.add_argument('state', type=int, required=True)
    parser.add_argument('attribute', type=int, required=True)
    parser.add_argument('region', type=int, required=True)
    parser.add_argument('remark', type=str)

    #host put request data
    parser_host = reqparse.RequestParser()
    parser_host.add_argument('name', type=str)
    parser_host.add_argument('description', type=str)
    parser_host.add_argument('device_key', type=str)
    parser_host.add_argument('state', type=int, required=True)
    parser_host.add_argument('region', type=int, required=True)
    parser_host.add_argument('dns', type=str)
    parser_host.add_argument('project_id', type=str)
    parser_host.add_argument('remark', type=str)
