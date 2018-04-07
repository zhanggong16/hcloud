#!/usr/bin/env python
import requests

host_id = '840bad62-35be-11e8-9bb6-fa163ea5419d1'

hostlist = 'http://localhost:5000/api/v1/host/%s' % host_id

#r = requests.post(hostlist, params=payload)
r = requests.delete(hostlist)

print r.json()
print r.status_code
