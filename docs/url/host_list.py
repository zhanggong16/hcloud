#!/usr/bin/env python
import requests

hostlist = 'http://localhost:5000/api/v1/hostlist'

#headers = {'Authorization': 'Hcloud secret-token-1'}
headers = {}

#r = requests.post(hostlist, params=payload)
r = requests.get(hostlist, headers=headers)

print r.status_code
print r
rs = r.json()
print rs

#print r.headers
