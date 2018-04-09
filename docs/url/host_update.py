#!/usr/bin/env python
import requests

hostlist = 'http://localhost:5000/api/v1/host/053c7088-310a-11e8-84ee-ac853dafc5c4'


payload = {
        'name': 'zhanggong',
        'description': 'zhanggong ccccc',
        'device_key': '124124',
        'state': 1,
        'region': 1,
        'dns': 'zhanggong.com',
        'project_id': '01',
        'remark': ''
}

r = requests.put(hostlist, params=payload)

rs = r.json()

print rs
print r.status_code
