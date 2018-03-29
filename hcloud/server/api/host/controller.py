from hcloud.models.host import HostData
import uuid

class Host(object):

    @classmethod
    def lst(cls):
        rs = HostData.getlist()
        if rs:
            return [ line.dump() for line in rs ]
        else:
            return

    @classmethod
    def add_host(cls, *add):
        name, description, device_key, privateip, os_type, state, attribute, region, remark = add
        host_id = str(uuid.uuid1())
        rs = HostData.add(host_id, name, description, device_key, privateip, os_type, state, attribute, region, remark)
        return rs
        
