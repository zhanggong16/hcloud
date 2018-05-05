#!/usr/bin/env python
import requests

alert_rules = 'http://localhost:6000/api/v1/alert_rules'


payload = {
  "host_id": "192.168.0.93",
  "port": 9100,
  "service": "node",
  "monitor_items":  "memory_usage",
  "statistical_period": "5s",
  "statistical_approach":  "max",
  "compute_mode":  ">",
  "threshold_value": 1,
  "contact_groups":"machao",
  "notify_type": 0
}

r = requests.post(alert_rules, params=payload)

rs = r.json()

print rs
print r.status_code

