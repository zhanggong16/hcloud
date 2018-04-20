import requests
from hcloud.exceptions import MonitorError
from hcloud.config import MONITOR_SERVER

server = MONITOR_SERVER

class Monitor(object):

    @staticmethod
    def post(url, data={}):
        url = server + url
        with requests.Session() as s:
            res = s.post(url, data=json.dumps(data), timeout=5)
            return res.status_code

    @staticmethod
    def get(url):
        url = server + url
        with requests.Session() as s:
            res = s.get(url, timeout=5)
            return res

    def reload(self):
        url = '/-/reload'
        status = self.post(url)
        return True if status in [200, 201] else False

    def summary(self):
        url = '/api/v1/series?match[]={exported_job="summary"}'
        res = self.get(url)
        return res.json()
    
