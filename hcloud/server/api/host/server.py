from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import marshal_with
from hcloud.server.api.error import ApiException
from .controller import Host
from .views import HostViews


class HostListAPI(Resource):
    '''get host list from MySQL, api'''    

    hostlist_fields = HostViews.hostlist_fields    
    hostlist_parser = HostViews.parser

    @marshal_with(hostlist_fields)    
    def get(self):
        try:
            data_res = Host.lst()
        except Exception as e:
            ApiException.get_data_from_mysql_error(str(e))
        return {'data': data_res, 'total': len(data_res)}

    def post(self):
        ''' add host '''
        args = HostListAPI.hostlist_parser.parse_args()
        name = args['name']
        description = args['description']
        device_key = args['device_key']
        privateip = args['privateip']
        os_type = args['os_type']
        state = args['state']
        attribute = args['attribute']
        region = args['region']
        remark = args['remark']
        dns = args['dns']
        project_id = args['project_id']
        try:
            data_res = Host.add_hostpool(name, description, device_key, privateip, os_type, state, attribute, region, remark, dns, project_id)
        except Exception as e:
            ApiException.get_data_from_mysql_error(str(e))    
        return {'id': data_res}, 201

class HostAPI(Resource):
    
    host_parser = HostViews.parser_host

    def delete(self, host_id):
        abort_if_host_id_doesnt_exist_hostpool(host_id)
        ###if host id doesnt exist instance pool / db pool       
        try:
            res = Host.delete_from_hostpool(host_id)
        except Exception as e:
            ApiException.get_data_from_mysql_error(str(e))
        return {'host_id': res}, 200

    def put(self, host_id):
        abort_if_host_id_doesnt_exist_hostpool(host_id)
        args = HostAPI.host_parser.parse_args()
        name = args['name']
        description = args['description']
        device_key = args['device_key']
        state = args['state']
        region = args['region']
        remark = args['remark']
        dns = args['dns']
        project_id = args['project_id']
        try:
            res = Host.update_hostpool(host_id, name, description, device_key, state, region, remark, dns, project_id)
        except Exception as e:
            ApiException.get_data_from_mysql_error(str(e))
        return {'host_id': res}, 200
    


def abort_if_host_id_doesnt_exist_hostpool(host_id):
    res = Host.get_id_from_hostpool(host_id)
    if not res:
        ApiException.data_not_found(host_id)
