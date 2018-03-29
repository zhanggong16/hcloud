from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import marshal_with
from hcloud.server.api.error import ApiException
from .controller import Host
from .views import HostListViews


class HostList(Resource):
    '''get host list from MySQL, api'''    

    hostlist_fields = HostListViews.hostlist_fields    
    hostlist_parser = HostListViews.parser

    @marshal_with(hostlist_fields)    
    def get(self):
        try:
            data_res = Host.lst()
        except Exception as e:
            ApiException.nodatareturn(e)
        return {'data': data_res, 'total': len(data_res)}

    
    def post(self):
        args = HostList.hostlist_parser.parse_args()
        host_id = args['host_id']
        return host_id
