from flask_restful import reqparse
from flask_restful import fields

class HostViews(object):

    #return data schema
    hostlist_data_fields = {}
    hostlist_data_fields['host_id'] = fields.String(attribute='host_id')
    hostlist_data_fields['name'] = fields.String(attribute='name')
    hostlist_data_fields['description'] = fields.String(attribute='description')
    hostlist_data_fields['name'] = fields.String(attribute='name')
    hostlist_data_fields['device_key'] = fields.String(attribute='device_key')
    hostlist_data_fields['os_type'] = fields.String(attribute='os_type')
    hostlist_data_fields['status'] = fields.String(attribute='status')
    hostlist_data_fields['monitor_status'] = fields.String(attribute='monitor_status')
    hostlist_data_fields['state'] = fields.String(attribute='state')
    hostlist_data_fields['attribute'] = fields.String(attribute='attribute')
    hostlist_data_fields['region'] = fields.String(attribute='region')
    hostlist_data_fields['privateip'] = fields.String(attribute='privateip')
    hostlist_data_fields['privateip_extend'] = fields.String(attribute='privateip_extend')
    hostlist_data_fields['publicip'] = fields.String(attribute='publicip')
    hostlist_data_fields['publicip_extend'] = fields.String(attribute='publicip_extend')
    hostlist_data_fields['cpu'] = fields.String(attribute='cpu')
    hostlist_data_fields['cpu_process'] = fields.String(attribute='cpu_process')
    hostlist_data_fields['memory'] = fields.String(attribute='memory')
    hostlist_data_fields['disk_space'] = fields.String(attribute='disk_space')
    hostlist_data_fields['disk_type'] = fields.String(attribute='disk_type')
    hostlist_data_fields['dns'] = fields.String(attribute='dns')
    hostlist_data_fields['project_id'] = fields.String(attribute='project_id')
    hostlist_data_fields['project_name'] = fields.String(attribute='project_name')
    hostlist_data_fields['project_description'] = fields.String(attribute='project_description')
    hostlist_data_fields['remark'] = fields.String(attribute='remark')
    hostlist_data_fields['create_time'] = fields.String(attribute='create_time')
    hostlist_data_fields['update_time'] = fields.String(attribute='update_time')
    
    hostlist_fields = {
        'total': fields.Integer,
        'data': fields.List(fields.Nested(hostlist_data_fields))
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
