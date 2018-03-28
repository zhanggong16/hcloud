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
            ApiException.handler_hcloud_error(str(e))
        return {'data': data_res, 'total': len(data_res)}

    def post(self):
        ''' add host '''
        args = HostList.hostlist_parser.parse_args()
        name = args['name']
        description = args['description']
        device_key = args['device_key']
        privateip = args['privateip']
        os_type = args['os_type']
        state = args['state']
        attribute = args['attribute']
        region = args['region']
        remark = args['remark']
        try:
            data_res = Host.add_host(name, description, device_key, privateip, os_type, state, attribute, region, remark)
        except Exception as e:
            ApiException.handler_hcloud_error(str(e))    
        return {'status':'ok'}, 201
            
