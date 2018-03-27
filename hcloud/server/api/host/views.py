from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import abort
from hcloud.server.api.error import ApiError
from .controller import Host

#parser = reqparse.RequestParser()
#parser.add_argument('host_id', type=str)


hostlist_data_fields = {}
hostlist_data_fields['host_id'] = fields.String(attribute='host_id')
hostlist_data_fields['name'] = fields.String(attribute='name')

hostlist_fields = {
    'total': fields.Integer,
    'data': fields.List(fields.Nested(hostlist_data_fields))
    }

class HostList(Resource):

    @marshal_with(hostlist_fields)    
    def get(self):
        try:
            data_res = Host.lst()
        except Exception as e:
            abort(501, message=str(e), error="123")
        return {"data": data_res}
