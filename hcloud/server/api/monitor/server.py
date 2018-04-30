from flask_restful import Resource
from flask_restful import marshal_with
from hcloud.exceptions import NotFound
#from .controller import HostsController
#from .views import HostsViews

class MonitorAPI(Resource):
    '''get host list'''

    #hostlist_fields = HostsViews.hostlist_fields    
    #hostlist_parser = HostsViews.parser

    #@marshal_with(hostlist_fields)    
    def get(self):
        try:
            data_res = '123'
        except Exception as e:
            raise ModelsDBError(str(e))
        return {'data': data_res}

