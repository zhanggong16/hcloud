from hcloud.models.hosts import HostsData

class HostsController(object):

    @classmethod
    def get_list(cls):
        rs = HostsData.getlist()
        if rs:
            return [ line.dump() for line in rs ]
        else:
            return
