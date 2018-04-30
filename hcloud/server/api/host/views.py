from flask_restful import reqparse
from flask_restful import fields

class HostsViews(object):

    #return host list
    hostlist_data_fields = {}
    hostlist_data_fields['host_key'] = fields.String(attribute='host_key')
    hostlist_data_fields['user_id'] = fields.String(attribute='user_id')
    hostlist_data_fields['description'] = fields.String(attribute='description')
    hostlist_data_fields['name'] = fields.String(attribute='name')
    hostlist_data_fields['os_type'] = fields.String(attribute='os_type')
    hostlist_data_fields['monitor_status'] = fields.String(attribute='monitor_status')
    hostlist_data_fields['state'] = fields.String(attribute='state')
    hostlist_data_fields['privateip'] = fields.String(attribute='privateip')
    hostlist_data_fields['cpu_physical'] = fields.String(attribute='cpu_physical')
    hostlist_data_fields['cpu_process'] = fields.String(attribute='cpu_process')
    hostlist_data_fields['memory_total'] = fields.String(attribute='memory_total')
    hostlist_data_fields['disk_usage'] = fields.String(attribute='disk_usage')
    hostlist_data_fields['project_id'] = fields.String(attribute='project_id')
    hostlist_data_fields['remark'] = fields.String(attribute='remark')
    hostlist_data_fields['create_time'] = fields.String(attribute='create_time')
    hostlist_data_fields['update_time'] = fields.String(attribute='update_time')
    
    hostlist_fields = {
        'message': fields.String(default='undefine'),
        'status': fields.String(default='success'),
        'data': fields.List(fields.Nested(hostlist_data_fields))
    }

    
