from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import marshal_with
from hcloud.server.api.error import ApiException
from .controller import Host
from .views import HostListViews


class HostList(Resource):
    '''get host list from MySQL, api'''    

    hostlist_fields = HostListViews.hostlist_fields    

    @marshal_with(hostlist_fields)    
    def get(self):
        try:
            data_res = Host.lst()
        except Exception as e:
            ApiException.nodatareturn(e)
        return {"data": data_res}

