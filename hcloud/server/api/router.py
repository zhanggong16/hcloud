from hcloud.server.api.host.views import HostList

version = 'v1'

apis = [
        [HostList, '/api/{vsersion}/hostlist'.format(vsersion=version)],
]
