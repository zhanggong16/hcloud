#!/usr/bin/env python
import requests

hostlist = 'http://localhost:6000/api/v1/alert_rules'


payload = {
  "host_id": "192.168.0.92",
  "port": 9100,
  "service": "node",
  "monitor_items":  "memory_usage",
  "statistical_period": "5m",
  "statistical_approach":  "max",
  "compute_mode":  ">",
  "threshold_value": 80
}

r = requests.post(hostlist, params=payload)

rs = r.json()

print rs
print r.status_code
