from hcloud.libs.db.mysql import db

class HostData(object):
    _table_hp = 'host_pool'
    _table_hpe = 'host_pool_extend'
    _table_p = 'project'

    def __init__(
            self, id_, host_id, name, description, device_key, os_type,
            status, monitor_status, state, attribute, region, privateip, privateip_extend, 
            publicip, publicip_extend, cpu, cpu_process, memory,
            disk_space, disk_type, dns, project_id, project_name, project_description, remark, create_time, update_time):
        self.id_ = str(id_)
        self.host_id = host_id
        self.name = name
        self.description = description
        self.device_key = device_key
        self.os_type = os_type
        self.status = status
        self.monitor_status = monitor_status
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
        self.dns = dns
        self.project_id = project_id
        self.project_name = project_name
        self.project_description = project_description
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
            monitor_status = self.monitor_status,
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
            dns = self.dns,
            project_id = self.project_id,
            project_name = self.project_name,
            project_description = self.project_description,
            remark = self.remark,
            create_time = self.create_time,
            update_time = self.update_time)
        return req

    @classmethod
    def getlist(cls):
        sql = (
                "select hp.id, hp.host_id, hp.name, hp.description, hp.device_key, "
                "hp.os_type, hp.status, hp.monitor_status, hp.state, hp.attribute, hp.region, "
                "hp.privateip, hpe.privateip_extend, hpe.publicip, "
                "hpe.publicip_extend, hpe.cpu, hpe.cpu_process, hpe.memory, "
                "hpe.disk_space, hpe.disk_type, hp.dns, hp.project_id, "
                "p.project_name, p.project_description, hp.remark, hp.create_time, hp.update_time "
                "from {table_hp} hp left join {table_hpe} hpe using(host_id) "
                "left join {table_p} p on p.pid=hp.project_id").format(table_hp=cls._table_hp, table_hpe=cls._table_hpe, table_p=cls._table_p)
        rs = db.execute(sql).fetchall()
        db.commit()
        return [ cls(*line) for line in rs ] if rs else []

    @classmethod
    def add_hostpool(cls, host_id, name, description, device_key, privateip, os_type, state, attribute, region, remark, dns, project_id):
        sql = ("insert into {table} "
               "(host_id, name, description, device_key, privateip, os_type, state, attribute, region, dns, project_id, remark) values "
               "(:host_id, :name, :description, :device_key, :privateip, "
               ":os_type, :state, :attribute, :region, :dns, :project_id, :remark)").format(table=cls._table_hp)
        params = dict(
                host_id=host_id,
                name=name,
                description=description,
                device_key=device_key,
                privateip=privateip,
                os_type=os_type,
                state=state,
                attribute=attribute,
                region=region,
                dns=dns,
                project_id=project_id,
                remark=remark)
        r = db.execute(sql, params=params)
        if r.lastrowid:
            db.commit()
            return r.lastrowid
        db.rollback()

    @classmethod
    def get_hostpool_by_host_id(cls, host_id):
        sql = ("select id from {table} where host_id=:host_id").format(table=cls._table_hp)
        params = dict(host_id=host_id)
        rs = db.execute(sql, params=params).fetchone()
        db.commit()
        return rs[0] if rs else ''

    
    @classmethod
    def delete_hostpool_by_host_id(cls, host_id):
        sql = ("delete from {table} where host_id=:host_id").format(table=cls._table_hp)
        params = dict(host_id=host_id)
        db.execute(sql, params=params)
        db.commit()
        return host_id

    @classmethod
    def update_hostpool_by_host_id(cls, host_id, name, description, device_key, state, region, remark, dns, project_id):
        sql = ("update {table} set name=:name, description=:description, "
                "device_key=:device_key, state=:state, region=:region, remark:=remark, "
                "dns=:dns, project_id=:project_id where host_id=:host_id").format(table=cls._table_hp)
        params = dict(
                host_id=host_id,
                name=name,
                description=description,
                device_key=device_key,
                state=state,
                region=region,
                dns=dns,
                project_id=project_id,
                remark=remark)
        db.execute(sql, params=params)
        db.commit()
        return host_id
