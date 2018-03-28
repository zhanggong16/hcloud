from flask_restful import reqparse
from flask_restful import fields

#parser = reqparse.RequestParser()
#parser.add_argument('host_id', type=str)

class HostListViews(object):

    hostlist_data_fields = {}
    hostlist_data_fields['host_id'] = fields.String(attribute='host_id')
    hostlist_data_fields['name'] = fields.String(attribute='name')

    hostlist_fields = {
        'total': fields.Integer,
        'data': fields.List(fields.Nested(hostlist_data_fields))
    }
