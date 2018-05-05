#!/usr/bin/env python
import requests
import json

alert_rules = 'http://localhost:6000/api/v1/alert_rules_list'


r = requests.get(alert_rules)

rs = r.json()

print rs
print r.status_code

