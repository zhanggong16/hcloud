from hcloud.libs.db.mysql import db

class AlertRulesData(object):
    _table_ar = 'alert_rules'

    def __init__(
            self, id_, alert_rules_id, host_id, port, service, monitor_items, statistical_period,
            statistical_approach, compute_mode, threshold_value, silence_time, contact_groups, notify_type, status, deleted, deleted_time,create_time, update_time):
        self.id_ = str(id_)
        self.alert_rules_id = alert_rules_id
        self.host_id = host_id
        self.port = port
        self.service = service
        self.monitor_items = monitor_items
        self.statistical_period = statistical_period
        self.statistical_approach = statistical_approach
        self.compute_mode = compute_mode
        self.threshold_value = threshold_value
        self.silence_time = silence_time
        self.contact_groups = contact_groups
        self.notify_type = notify_type
        self.status = status
        self.deleted = deleted
        self.deleted_time = deleted_time
        self.create_time = create_time
        self.update_time = update_time

    def dump(self):
        req = dict(
            id = self.id_,
            alert_rules_id = self.alert_rules_id,
            host_id = self.host_id,
            port=self.port,
            service = self.service,
            monitor_items = self.monitor_items,
            statistical_period = self.statistical_period,
            statistical_approach = self.statistical_approach,
            compute_mode = self.compute_mode,
            threshold_value = self.threshold_value,
            silence_time=self.silence_time,
            contact_groups=self.contact_groups,
            notify_type=self.notify_type,
            status = self.status,
            deleted = self.deleted,
            deleted_time = self.deleted_time ,
            create_time = self.create_time,
            update_time = self.update_time)
        return req

    @classmethod
    def get_alert_rules(cls, alert_rules_id):
        sql = (
            " select id, alert_rules_id, host_id, port, service, monitor_items, statistical_period,"
            " statistical_approach, compute_mode, threshold_value, silence_time, contact_groups, notify_type, status, deleted, deleted_time, create_time, update_time"
            " from {table} where alert_rules_id = :alert_rules_id and deleted = 0").format(table=cls._table_ar)
        params = dict(alert_rules_id=alert_rules_id)
        line = db.execute(sql, params=params).fetchone()
        db.commit()
        return line if line else ''

    @classmethod
    def get_alert_rules_list(cls):
        sql = (
            " select id, alert_rules_id, host_id, port, service, monitor_items, statistical_period,"
            " statistical_approach, compute_mode, threshold_value, silence_time, contact_groups, notify_type, status, deleted, deleted_time, create_time, update_time"
            " from {table} where deleted = 0").format(table=cls._table_ar)
        rs = db.execute(sql).fetchall()
        db.commit()
        return [cls(*line) for line in rs] if rs else []

    @classmethod
    def show_alert_rules(cls, alert_rules_id):
        sql = (
            " select id, alert_rules_id, host_id, port, service, monitor_items, statistical_period,"
            " statistical_approach, compute_mode, threshold_value, silence_time, contact_groups, notify_type, status, deleted, deleted_time, create_time, update_time"
            " from {table} where alert_rules_id = :alert_rules_id and deleted = 0").format(table=cls._table_ar)
        params = dict(alert_rules_id=alert_rules_id)
        rs = db.execute(sql, params=params).fetchall()
        db.commit()
        return [cls(*line) for line in rs] if rs else []

    @classmethod
    def get_alert_rules_by_name(cls, monitor_items):
        sql = (
            " select id, alert_rules_id, host_id, port, service, monitor_items, statistical_period,"
            " statistical_approach, compute_mode, threshold_value, silence_time, contact_groups, notify_type, status, deleted, deleted_time, create_time, update_time"
            " from {table} where monitor_items = :monitor_items and deleted = 0").format(table=cls._table_ar)
        params = dict(monitor_items=monitor_items)
        line = db.execute(sql, params=params).fetchone()
        db.commit()
        return line if line else ''

    @classmethod
    def add(cls, alert_rules_id, host_id, port, service, monitor_items, statistical_period, statistical_approach, compute_mode, threshold_value, contact_groups, notify_type, status):
        sql = ("insert into {table} "
               "(alert_rules_id, host_id, port, service, monitor_items, statistical_period, statistical_approach, compute_mode, threshold_value, contact_groups, notify_type, status) values "
               "(:alert_rules_id, :host_id, :port, :service, :monitor_items, :statistical_period, "
               ":statistical_approach, :compute_mode, :threshold_value, :contact_groups, :notify_type, :status)").format(table=cls._table_ar)
        params = dict(
            host_id=host_id,
            port=port,
            alert_rules_id=alert_rules_id,
            service=service,
            monitor_items=monitor_items,
            statistical_period=statistical_period,
            statistical_approach=statistical_approach,
            compute_mode=compute_mode,
            threshold_value=threshold_value,
            contact_groups=contact_groups,
            notify_type=notify_type,
            status=status)
        r = db.execute(sql, params=params)
        if r.lastrowid:
            db.commit()
            return r.lastrowid
        db.rollback()

    @classmethod
    def update(cls, alert_rules_id, statistical_period, compute_mode, threshold_value, contact_groups, notify_type):
        sql = (
        "update {table} set statistical_period=:statistical_period, compute_mode=:compute_mode, threshold_value=:threshold_value, contact_groups=:contact_groups, notify_type=:notify_type where alert_rules_id = :alert_rules_id and deleted = 0").format(
            table=cls._table_ar)

        params = dict(
            statistical_period=statistical_period,
            compute_mode=compute_mode,
            threshold_value=threshold_value,
            contact_groups=contact_groups,
            notify_type=notify_type,
            alert_rules_id=alert_rules_id)
        r = db.execute(sql, params=params)
        if r.lastrowid:
            db.commit()
        return r.lastrowid
        db.rollback()

    @classmethod
    def update_status(cls, alert_rules_id, status):
        sql = ("update {table} set status=:status where alert_rules_id = :alert_rules_id and deleted = 0").format(table=cls._table_ar)
        params = dict(
            alert_rules_id=alert_rules_id,
            status = status)
        db.execute(sql, params=params)
        db.commit()

    @classmethod
    def update_silence_time(cls, alert_rules_id, silence_time):
        sql = ("update {table} set silence_time=:silence_time where alert_rules_id = :alert_rules_id and deleted = 0").format(table=cls._table_ar)
        params = dict(
            alert_rules_id=alert_rules_id,
            silence_time=silence_time)
        db.execute(sql, params=params)
        db.commit()

    @classmethod
    def delete_alert_rule(cls, alert_rules_id):
        sql = ("update {table} set deleted = 1 where alert_rules_id = :alert_rules_id and deleted = 0").format(table=cls._table_ar)
        params = dict(
            alert_rules_id=alert_rules_id)
        db.execute(sql, params=params)
        db.commit()




