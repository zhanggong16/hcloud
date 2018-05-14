from flask_restful import Resource
from flask_restful import marshal_with
from flask import g
from hcloud.middleware.auth import auth
from hcloud.exceptions import (
    NotFound,
    ModelsDBError,
    MonitorError
)
from .controller import MonitorController
from .views import MonitorViews


class MonitorAPI(Resource):
    #decorators = [auth.login_required]

    monitor_item_title_fields = MonitorViews.monitor_item_title_fields
    #hostlist_parser = HostsViews.parser

    @marshal_with(monitor_item_title_fields)    
    def get(self, category, host_key):
        _abort_if_host_id_doesnt_exist_hostspool(host_key)
        try:
            item_list = MonitorController.get_monitor_item(category)
        except Exception as e:
            raise ModelsDBError(str(e))
        try:
            data_res = MonitorController.monitor_title(item_list, category, host_key, '123')       
        except Exception as e:
            raise MonitorError(str(e))
        return {'data': data_res}

class MonitorDetailAPI(Resource):
    pass

def _abort_if_host_id_doesnt_exist_hostspool(host_key):
    res = MonitorController.get_id_from_hostspool(host_key)
    if not res:
        raise NotFound("Host %s not exist" % host_key)
