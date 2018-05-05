#!/usr/bin/env python
import requests
import json

alertrules_id = '8287ced0-4f45-11e8-bd2d-fa163ea5419d'
alert_rules = 'http://localhost:6000/api/v1/alert_rules/%s'% alertrules_id


r = requests.delete(alert_rules)

#rs = r.json()

#print rs
print r.url
print r.status_code

