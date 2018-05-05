from hcloud.libs.db.mysql import db
class AlertsData(object):
    _table_ah = 'alert_history'

    def __init__(
            self, id_, alert_rules_id, monitor_items, host_id, port, service, alert_time,
            current_value, last_time, state, contact_groups, status):
        self.id_ = str(id_)
        self.alert_rules_id = alert_rules_id
        self.monitor_items = monitor_items
        self.host_id = host_id
        self.service = service
        self.port = port
        self.alert_time = alert_time
        self.current_value = current_value
        self.last_time = last_time
        self.state = state
        self.status = status
        self.contact_groups = contact_groups

    def dump(self):
        req = dict(
            id = self.id_,
            alert_rules_id = self.alert_rules_id,
            host_id = self.host_id,
            service = self.service,
            port = self.port,
            monitor_items = self.monitor_items,
            alert_time = self.alert_time,
            current_value = self.current_value,
            last_time = self.last_time,
            state = self.state,
            status = self.status,
            contact_groups = self.contact_groups)
        return req

    @classmethod
    def get_alerts(cls, alert_rules_id):
        sql = (
            " select id, alert_rules_id, monitor_items, host_id, port, service, alert_time,"
            " current_value, last_time, state, contact_groups, status"
            " from {table} where alert_rules_id := alert_rules_id ").format(table=cls._table_ah)
        params = dict(alert_rules_id=alert_rules_id)
        line = db.execute(sql, params=params).fetchone()
        db.commit()
        return line if line else ''

    @classmethod
    def get_alerts_list(cls):
        sql = (
            " select id, alert_rules_id, monitor_items, host_id, port, service, alert_time,"
            " current_value, last_time, state, contact_groups, status"
            " from {table}").format(table=cls._table_ah)
        rs = db.execute(sql).fetchall()
        db.commit()
        return [cls(*line) for line in rs] if rs else []

    @classmethod
    def add(cls, alert_rules_id, host_id, port, service, monitor_items, alert_time, current_value, last_time, state, contact_groups, status):
        sql = ("insert into {table} "
               "(alert_rules_id, host_id, port, service, monitor_items, alert_time, current_value, last_time, state, contact_groups, status) values "
               "(:alert_rules_id, :host_id, :port, :service, :monitor_items, :alert_time, "
               ":current_value, :last_time, :state, :contact_groups, :status)").format(table=cls._table_ah)
        params = dict(
            host_id=host_id,
            port=port,
            alert_rules_id=alert_rules_id,
            service=service,
            monitor_items=monitor_items,
            alert_time=alert_time,
            current_value=current_value,
            last_time=last_time,
            state=state,
            contact_groups=contact_groups,
            status=status)
        r = db.execute(sql, params=params)
        if r.lastrowid:
            db.commit()
            return r.lastrowid
        db.rollback()



