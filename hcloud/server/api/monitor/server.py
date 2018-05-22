from flask_restful import Resource
from flask_restful import marshal_with
from flask import g, request
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

    @marshal_with(monitor_item_title_fields)    
    def get(self, category, key):
        _abort_if_host_id_doesnt_exist_hostspool(key)
        try:
            item_list = MonitorController.get_monitor_item(category)
        except Exception as e:
            raise ModelsDBError(str(e))
        try:
            data_res = MonitorController.monitor_title(item_list, category, key, '123')       
        except Exception as e:
            raise MonitorError(str(e))
        if data_res:
            status = 'success'
        else:
            status = 'failed'
        return {'data': data_res, 'status': status}

class MonitorDetailAPI(Resource):
    #decorators = [auth.login_required]

    #monitor_parser = MonitorViews.parser

    def get(self, category, key):
        para_dict = {
            'start': request.args['start'],
            'end': request.args['end'],
            'query': request.args['query'],
            'interval': request.args['interval'],
            'name': request.args['name'],
            'category': category
            }   
        print para_dict['query']
        try:
            data_res = MonitorController.monitor_data(para_dict, '123')
        except Exception as e:
            raise MonitorError(str(e))
        if data_res:
            status = 'success'
        else:
            status = 'failed'
        return {'data': data_res, 'status': status}

def _abort_if_host_id_doesnt_exist_hostspool(key):
    res = MonitorController.get_id_from_hostspool(key)
    if not res:
        raise NotFound("Host %s not exist" % key)
