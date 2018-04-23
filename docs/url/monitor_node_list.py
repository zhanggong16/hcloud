#!/usr/bin/env python
import requests

url = 'http://localhost:5000/api/v1/monitor/host'


payload = {
}

r = requests.get(url, params=payload)

rs = r.json()

print rs
print r.status_code
