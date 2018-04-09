from hcloud.server.api.host.server import HostListAPI
from hcloud.server.api.host.server import HostAPI
from hcloud.server.api.alert.server import SendToAlert
from hcloud.server.api.alert.server import AlertRules
version = 'v1'

apis = [
        [HostListAPI, '/api/{vsersion}/hostlist'.format(vsersion=version)],
        [HostAPI, '/api/{vsersion}/host/<host_id>'.format(vsersion=version)],
        [SendToAlert, '/api/{vsersion}/alert'.format(vsersion=version)],
        [AlertRules, '/api/{vsersion}/alert_rules'.format(vsersion=version)],
        [AlertRules, '/api/{vsersion}/alert_rules/<alert_rules_id>'.format(vsersion=version)]
]
