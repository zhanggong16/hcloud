from hcloud.libs.db.mysql import db
class AlertRulesData(object):
    _table_ar = 'alert_rules'

    def __init__(
            self, id_, alert_rules_id, host_id, service, monitor_items, statistical_period,
            statistical_approach, compute_mode, threshold_value, status, deleted, deleted_time,create_time, update_time):
        self.id_ = str(id_)
        self.alert_rules_id = alert_rules_id
        self.host_id = host_id
        self.service = service
        self.monitor_items = monitor_items
        self.statistical_period = statistical_period
        self.statistical_approach = statistical_approach
        self.compute_mode = compute_mode
        self.threshold_value = threshold_value
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
            service = self.service,
            monitor_items = self.monitor_items,
            statistical_period = self.statistical_period,
            statistical_approach = self.statistical_approach,
            compute_mode = self.compute_mode,
            threshold_value = self.threshold_value,
            status = self.status,
            deleted = self.deleted,
            deleted_time = self.deleted_time ,
            create_time = self.create_time,
            update_time = self.update_time)
        return req

    @classmethod
    def get_alert_rules(cls, alert_rules_id):
        sql = (
            " select host_id, service, monitor_items, statistical_period,"
            " statistical_approach, statistical_approach, compute_mode, threshold_value, status"
            " from {table} where alert_rules_id := alert_rules_id ").format(table=cls._table_ar)
        params = dict(alert_rules_id=alert_rules_id)
        line = db.execute(sql, params=params).fetchone()
        db.commit()
        return line if line else ''

    @classmethod
    def add(cls, alert_rules_id, host_id, service, monitor_items, statistical_period, statistical_approach, compute_mode, threshold_value, status):
        sql = ("insert into {table} "
               "(alert_rules_id, host_id, service, monitor_items, statistical_period, statistical_approach, compute_mode, threshold_value, status) values "
               "(:alert_rules_id, :host_id, :service, :monitor_items, :statistical_period, "
               ":statistical_approach, :compute_mode, :threshold_value, :status)").format(table=cls._table_ar)
        params = dict(
            host_id=host_id,
            alert_rules_id=alert_rules_id,
            service=service,
            monitor_items=monitor_items,
            statistical_period=statistical_period,
            statistical_approach=statistical_approach,
            compute_mode=compute_mode,
            threshold_value=threshold_value,
            status=status)
        r = db.execute(sql, params=params)
        if r.lastrowid:
            db.commit()
            return r.lastrowid
        db.rollback()

    @classmethod
    def update(cls, alert_rules_id, statistical_period, statistical_approach, compute_mode, threshold_value, status):
        sql = ("update {table} set "
               "statistical_period=:statistical_period, statistical_approach=:statistical_approach, compute_mode=:compute_mode, threshold_value=:threshold_value, status=:status"
               "where alert_rules_id = :alert_rules_id").format(table=cls._table_ar)
        params = dict(
            statistical_period=statistical_period,
            statistical_approach=statistical_approach,
            compute_mode=compute_mode,
            threshold_value=threshold_value,
            alert_rules_id=alert_rules_id,
            status = status)
        r = db.execute(sql, params=params)
        if r.lastrowid:
            db.commit()
        return r.lastrowid
        db.rollback()

    @classmethod
    def update_status(cls, alert_rules_id, status):
        sql = ("update {table} set status=:status where alert_rules_id = :alert_rules_id").format(table=cls._table_ar)
        params = dict(
            alert_rules_id=alert_rules_id,
            status = status)
        db.execute(sql, params=params)
        db.commit()




