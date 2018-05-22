#!/usr/bin/env python
import requests

#url = "http://localhost:5000/api/v1/monitor/detail_data/node/847aa4a4-4632-11e8-abe3-fa163ea5419d?name=cpu_used&query=exported_instance='192.168.0.92:9100',group='gateway',exported_job='node_group',instance='114.67.76.108:9091',job='gateway'&start=1526346000&end=1526347000&interval=15"
#url = "http://localhost:5000/api/v1/monitor/detail_data/node/847aa4a4-4632-11e8-abe3-fa163ea5419d?name=memory_used_rate&query=exported_instance='192.168.0.92:9100',group='gateway',exported_job='node_group',instance='114.67.76.108:9091',job='gateway'&start=1526346000&end=1526347000&interval=15"
#url = "http://localhost:5000/api/v1/monitor/detail_data/node/847aa4a4-4632-11e8-abe3-fa163ea5419d?name=network_io&query=exported_instance='192.168.0.92:9100',group='gateway',exported_job='node_group',instance='114.67.76.108:9091',job='gateway',device='eth0'&start=1526346000&end=1526347000&interval=15"
url = "http://localhost:5000/api/v1/monitor/detail_data/node/847aa4a4-4632-11e8-abe3-fa163ea5419d?name=disk_io&query=exported_instance='192.168.0.92:9100',group='gateway',exported_job='node_group',instance='114.67.76.108:9091',job='gateway',device='vdb'&start=1526346000&end=1526347000&interval=15"


headers = {'Authorization': 'Hcloud secret-token-1'}

r = requests.get(url, headers=headers)
rs = r.json()

print rs
print r.status_code
