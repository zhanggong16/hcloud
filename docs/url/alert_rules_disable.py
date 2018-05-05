#!/usr/bin/env python
import requests
import json

alertrules_id = '8287ced0-4f45-11e8-bd2d-fa163ea5419d'
alert_rules = 'http://localhost:6000/api/v1/alert_rules/%s'% alertrules_id


payload = {
            "action": {
                "method": "disable",
                "param": {
                    "silence_time": 2
        }
    }
}
print json.dumps(payload)
r = requests.put(alert_rules, data=json.dumps(payload))

#rs = r.json()

#print rs
print r.url
print r.status_code

