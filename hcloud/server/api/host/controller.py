from hcloud.models.hosts import HostData

class HostsController(object):

    @classmethod
    def get_list(cls):
        rs = HostData.getlist()
        if rs:
            return [ line.dump() for line in rs ]
        else:
            return
