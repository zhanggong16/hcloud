#!/usr/bin/env python
import requests
import json

alertrules_id = 'dea9afb4-4f43-11e8-8430-fa163ea5419d'
alert_rules = 'http://localhost:6000/api/v1/alert_rules/%s'% alertrules_id


r = requests.get(alert_rules)

rs = r.json()

print rs
print r.status_code

