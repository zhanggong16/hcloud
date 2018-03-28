from hcloud.server.api.host.server import HostList

version = 'v1'

apis = [
        [HostList, '/api/{vsersion}/hostlist'.format(vsersion=version)],
]
