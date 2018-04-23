from flask_restful import Resource
from flask_restful import marshal_with
from hcloud.exceptions import ModelsDBError
from hcloud.exceptions import NotFound
from .controller import HostsController
from .views import HostsViews

header = {'Access-Control-Allow-Origin': '*'}

class HostListAPI(Resource):
    '''get host list'''

    hostlist_fields = HostsViews.hostlist_fields    
    hostlist_parser = HostsViews.parser

    @marshal_with(hostlist_fields)    
    def get(self):
        try:
            data_res = HostsController.get_list()
        except Exception as e:
            raise ModelsDBError(str(e))
        resp = {'data': data_res, 'message': 'undefine', 'status': 'success'}
        return resp

class HostAPI(Resource):
    pass
#    
#    host_parser = HostsViews.parser_host
#
#    def delete(self, host_id):
#        _abort_if_host_id_doesnt_exist_hostpool(host_id)
#        ###if host id doesnt exist instance pool / db pool       
#        try:
#            res = Host.delete_from_hostpool(host_id)
#        except Exception as e:
#            raise ModelsDBError(str(e))
#        return {'host_id': res}, 200
#
#    def put(self, host_id):
#        _abort_if_host_id_doesnt_exist_hostpool(host_id)
#        args = HostAPI.host_parser.parse_args()
#        name = args['name']
#        description = args['description']
#        device_key = args['device_key']
#        state = args['state']
#        region = args['region']
#        remark = args['remark']
#        dns = args['dns']
#        project_id = args['project_id']
#        try:
#            res = Host.update_hostpool(host_id, name, description, device_key, state, region, remark, dns, project_id)
#        except Exception as e:
#            raise ModelsDBError(str(e))
#        return {'host_id': res}, 200
#    
#
#
#def _abort_if_host_id_doesnt_exist_hostpool(host_id):
#    res = Host.get_id_from_hostpool(host_id)
#    if not res:
#        raise NotFound("Resource %s not exist" % host_id)
