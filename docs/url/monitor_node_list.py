#!/usr/bin/env python
import requests

url = 'http://localhost:5000/api/v1/monitor/data/node/847aa4a4-4632-11e8-abe3-fa163ea5419d'

headers = {'Authorization': 'Hcloud secret-token-1'}

payload = {
}

r = requests.get(url, params=payload, headers=headers)

rs = r.json()

print rs
print r.status_code
