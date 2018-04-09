#!/usr/bin/env python
import requests

hostlist = 'http://localhost:5000/api/v1/hostlist'


payload = {
        'name': 'zhanggong',
        'description': 'zhanggong mmmmmmmmm',
        'device_key': '124124',
        'privateip': '10.10.10.10',
        'os_type': 1,
        'state': 1,
        'attribute': 1,
        'region': 1,
        'dns': 'zhanggong.com',
        'project_id': '01',
        'remark': ''
}

r = requests.post(hostlist, params=payload)

rs = r.json()

print rs
print r.status_code
