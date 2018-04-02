from hcloud.server.api.host.server import HostList
from hcloud.server.api.alert.server import SendToAlert
from hcloud.server.api.alert.server import AlertRules
version = 'v1'

apis = [
        [HostList, '/api/{vsersion}/hostlist'.format(vsersion=version)],
        [SendToAlert, '/api/{vsersion}/alert'.format(vsersion=version)],
        [AlertRules, '/api/{vsersion}/alert_rules'.format(vsersion=version)],
        [AlertRules, '/api/{vsersion}/alert_rules/<int:alertrules_id>'.format(vsersion=version)]

]
