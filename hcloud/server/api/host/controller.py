from hcloud.models.host import HostData

class Host(object):

    @classmethod
    def lst(cls):
        rs = HostData.getlist()
        if rs:
            return [ line.dump() for line in rs ]
        else:
            return
