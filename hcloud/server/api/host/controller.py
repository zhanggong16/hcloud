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
    def add_hostpool(cls, *add):
        name, description, device_key, privateip, os_type, state, attribute, region, remark, dns, project_id = add
        host_id = str(uuid.uuid1())
        rs = HostData.add_hostpool(host_id, name, description, device_key, privateip, os_type, state, attribute, region, remark, dns, project_id)
        return rs

    @classmethod
    def get_id_from_hostpool(cls, host_id):
        rs = HostData.get_hostpool_by_host_id(host_id)
        return rs

    @classmethod
    def delete_from_hostpool(cls, host_id):
        rs = HostData.delete_hostpool_by_host_id(host_id)
        return rs

    @classmethod
    def update_hostpool(cls, *update):
        host_id, name, description, device_key, state, region, remark, dns, project_id = update
        rs = HostData.update_hostpool_by_host_id(host_id, name, description, device_key, state, region, remark, dns, project_id)
        return rs
