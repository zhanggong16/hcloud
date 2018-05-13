from hcloud.libs.db.mysql import db

class HostsData(object):
    _table_hp = 'hosts_pool'

    def __init__(
            self, id_, host_key, user_id, name, description, 
            privateip, cpu_process, cpu_physical, memory_total,
            disk_usage, monitor_status, os_type, state,
            project_id, remark, create_time, update_time):
        self.id_ = str(id_)
        self.host_key = host_key
        self.user_id = user_id
        self.name = name
        self.description = description
        self.privateip = privateip
        self.cpu_process = cpu_process
        self.cpu_physical = cpu_physical
        self.memory_total = memory_total
        self.disk_usage = disk_usage
        self.monitor_status = monitor_status
        self.os_type = os_type
        self.state = state
        self.project_id = project_id
        self.remark = remark
        self.create_time = create_time
        self.update_time = update_time

    def dump(self):
        req = dict(
            id = self.id_,
            host_key = self.host_key,
            user_id = self.user_id,
            name = self.name,
            description = self.description,
            privateip = self.privateip,
            cpu_process = self.cpu_process,
            cpu_physical = self.cpu_physical,
            memory_total = self.memory_total,
            disk_usage = self.disk_usage,
            monitor_status = self.monitor_status,
            os_type = self.os_type,
            state = self.state,
            project_id = self.project_id,
            remark = self.remark,
            create_time = self.create_time,
            update_time = self.update_time)
        return req

    @classmethod
    def getlist(cls):
        sql = (
                "select id, host_key, user_id, name, description, privateip, "
                "cpu_process, cpu_physical, memory_total, disk_usage, monitor_status, "
                "os_type, state, project_id, remark, create_time, update_time "
                "from {table_hp}").format(table_hp=cls._table_hp)
        rs = db.execute(sql).fetchall()
        db.commit()
        return [ cls(*line) for line in rs ] if rs else []

    @classmethod
    def get_privateip_by_host_key(cls, host_key):
        sql = ("select privateip from {table} where host_key=:host_key").format(table=cls._table_hp)
        params = dict(host_key=host_key)
        rs = db.execute(sql, params=params).fetchone()
        db.commit()
        return rs[0] if rs else ''

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
    def get_hostspool_by_host_key(cls, host_key):
        sql = ("select id from {table} where host_key=:host_key").format(table=cls._table_hp)
        params = dict(host_key=host_key)
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
