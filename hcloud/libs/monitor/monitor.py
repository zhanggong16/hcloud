import requests
import json

class Monitor(object):
    
    def get_server(self, user_id=None):
        if user_id:
            return 'http://localhost:9090'
        else:
            return 'http://localhost:9090'

    def __init__(self, user_id=None):
        self.server = self.get_server(user_id) 

    def _post(self, url, data={}):
        url = self.server + url
        with requests.Session() as s:
            res = s.post(url, data=json.dumps(data), timeout=5)
            return res.status_code

    def _get(self, url):
        url = self.server + url
        with requests.Session() as s:
            res = s.get(url, timeout=5)
            return res

    def reload(self):
        url = '/-/reload'
        status = self._post(url)
        return True if status in [200] else False

    def summary_series(self, exported_instance):
        '''
            http://114.67.76.75:9090/api/v1/series?match[]={exported_job="summary",exported_instance="192.168.0.92:9191"}
        '''
        url = '/api/v1/series?match[]={exported_job="summary",exported_instance="%s"}' % exported_instance
        res = self._get(url)
        return res.json()

    def last_data_by_exported_instance(self, query_metric, exported_instance):
        ''' 
            http://114.67.76.75:9090/api/v1/query?query=node_interval{exported_instance="192.168.0.92:9191"}
        '''        
        url = '/api/v1/query?query=%s{exported_instance="%s"}' % (query_metric, exported_instance)
        res = self._get(url)
        return res.json()

m = Monitor()
