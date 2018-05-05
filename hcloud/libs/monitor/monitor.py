import requests
import json
#from hcloud.exceptions import MonitorError

server = 'http://localhost:9090'

class Monitor(object):

    def __init__(self):
        print server

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
        return True if status in [200] else False

    def summary(self):
        url = '/api/v1/series?match[]={exported_job="summary"}'
        res = self.get(url)
        return res.json()

m = Monitor()
