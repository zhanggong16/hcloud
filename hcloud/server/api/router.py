from hcloud.server.api.host.server import HostListAPI
from hcloud.server.api.host.server import HostAPI
from hcloud.server.api.monitor.server import MonitorAPI
from hcloud.server.api.monitor.server import MonitorDetailAPI
from hcloud.server.api.alert.server import AlertRules
from hcloud.server.api.alert.server import AlertRulesList
from hcloud.server.api.alert.server import Alert
from hcloud.server.api.alert.server import CreateAlertRules


version = 'v1'

apis = [
        [HostListAPI, '/api/{vsersion}/<string:category>/list'.format(vsersion=version)],
        #[HostAPI, '/api/{vsersion}/host/<host_id>'.format(vsersion=version)],
        [MonitorAPI, '/api/{vsersion}/monitor/data/<string:category>/<string:key>'.format(vsersion=version)],
        [MonitorDetailAPI, '/api/{vsersion}/monitor/detail_data/'
                        '<string:category>/<string:key>'.format(vsersion=version)],
        [Alert, '/api/{vsersion}/alert'.format(vsersion=version)],
        [CreateAlertRules, '/api/{vsersion}/alert_rules'.format(vsersion=version)],
        [AlertRules, '/api/{vsersion}/alert_rules/service/<service_name>'.format(vsersion=version)],
        [AlertRulesList, '/api/{vsersion}/alert_rules_list'.format(vsersion=version)]
]
