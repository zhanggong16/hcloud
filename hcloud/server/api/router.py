from hcloud.server.api.host.server import HostList
from hcloud.server.api.alert.server import Alert

version = 'v1'

apis = [
        [HostList, '/api/{vsersion}/hostlist'.format(vsersion=version)],
        [Alert, '/api/{vsersion}/alert'.format(vsersion=version)]
]
