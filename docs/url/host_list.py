#!/usr/bin/env python
import requests

hostlist = 'http://localhost:5000/api/v1/hostlist'


payload = {
        'name': 'zhanggong',
        'description': 'zhanggong mmmmm',
        'device_key': '124124',
        'privateip': '10.10.10.10',
        'os_type': 1,
        'state': 1,
        'attribute': 1,
        'region': 1,
        'remark': ''
}

#r = requests.post(hostlist, params=payload)
r = requests.get(hostlist)

rs = r.json()

print rs
print r.status_code
