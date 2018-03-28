from hcloud.libs.db.mysql import db

class HostData(object):
    _table_hp = 'host_pool'
    _table_hpe = 'host_pool_extend'

    def __init__(
            self, id_, host_id, name, description, device_key, os_type,
            status, state, attribute, region, privateip, privateip_extend, 
            publicip, publicip_extend, cpu, cpu_process, memory,
            disk_space, disk_type, remark, create_time, update_time):
        self.id_ = str(id_)
        self.host_id = host_id
        self.name = name
        self.description = description
        self.device_key = device_key
        self.os_type = os_type
        self.status = status
        self.state = state
        self.attribute = attribute
        self.region = region
        self.privateip = privateip
        self.privateip_extend = privateip_extend
        self.publicip = publicip
        self.publicip_extend = publicip_extend
        self.cpu = cpu
        self.cpu_process = cpu_process
        self.memory = memory
        self.disk_space = disk_space
        self.disk_type = disk_type
        self.remark = remark
        self.create_time = create_time
        self.update_time = update_time

    def dump(self):
        req = dict(
            id = self.id_,
            host_id = self.host_id,
            name = self.name,
            description = self.description,
            device_key = self.device_key,
            os_type = self.os_type,
            status = self.status,
            state = self.state,
            attribute = self.attribute,
            region = self.region,
            privateip = self.privateip,
            privateip_extend = self.privateip_extend,
            publicip = self.publicip,
            publicip_extend = self.publicip_extend,
            cpu = self.cpu,
            cpu_process = self.cpu_process,
            memory = self.memory,
            disk_space = self.disk_space,
            disk_type = self.disk_type,
            remark = self.remark,
            create_time = self.create_time,
            update_time = self.update_time)
        return req

    @classmethod
    def getlist(cls):
        sql = (
                "select hp.id, hp.host_id, hp.name, hp.description, hp.device_key, "
                "hp.os_type, hp.status, hp.state, hp.attribute, hp.region, "
                "hp.privateip, hpe.privateip_extend, hpe.publicip, "
                "hpe.publicip_extend, hpe.cpu, hpe.cpu_process, hpe.memory, "
                "hpe.disk_space, hpe.disk_type, hp.remark, hp.create_time, hp.update_time "
                "1from {table_hp} hp join {table_hpe} hpe using(host_id)").format(table_hp=cls._table_hp, table_hpe=cls._table_hpe)
        rs = db.execute(sql).fetchall()
        db.commit()
        return [ cls(*line) for line in rs ] if rs else []
