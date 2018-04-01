from hcloud.server.api.host.server import HostListAPI
from hcloud.server.api.host.server import HostAPI
from hcloud.server.api.alert.server import AlertAPI


version = 'v1'

apis = [
        [HostListAPI, '/api/{vsersion}/hostlist'.format(vsersion=version)],
        [HostAPI, '/api/{vsersion}/host/<host_id>'.format(vsersion=version)],
        [AlertAPI, '/api/{vsersion}/alert'.format(vsersion=version)]
]
