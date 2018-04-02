from hcloud.libs.db.mysql import db
S
class AlertRulesData(object):
    _table_ar = 'alert_rules'

    def __init__(
            self, id_, alert_rules_id, host_id, service, monitor_items, statistical_period,
            statistical_approach, compute_mode, threshold_value, deleted, deleted_time,create_time, update_time):
        self.id_ = str(id_)
        self.alert_rules_id = alert_rules_id
        self.host_id = host_id
        self.service = service
        self.monitor_items = monitor_items
        self.statistical_period = statistical_period
        self.statistical_approach = statistical_approach
        self.compute_mode = compute_mode
        self.threshold_value = threshold_value
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
            deleted = self.deleted,
            deleted_time = self.deleted_time ,
            create_time = self.create_time,
            update_time = self.update_time)
        return req

    @classmethod
    def get_alert_rules(cls, alert_rules_id):
        sql = (
            " select host_id, service, monitor_items, statistical_period,"
            " statistical_approach, statistical_approach, compute_mode, threshold_value"
            " from {table} where alert_rules_id := alert_rules_id ").format(table=cls._table_ar)
        rs = db.execute(sql).fetchall()
        db.commit()
        return [cls(*line) for line in rs] if rs else []

    @classmethod
    def add(cls, alert_rules_id, host_id, service, monitor_items, statistical_period, statistical_approach, compute_mode, threshold_value):
        sql = ("insert into {table} "
               "(alert_rules_id, host_id, service, monitor_items, statistical_period, statistical_approach, compute_mode, threshold_value) values "
               "(:alert_rules_id, :host_id, :service, :monitor_items, :statistical_period, "
               ":statistical_approach, :compute_mode, :threshold_value)").format(table=cls._table_ar)
        params = dict(
            host_id=host_id,
            alert_rules_id=alert_rules_id,
            service=service,
            monitor_items=monitor_items,
            statistical_period=statistical_period,
            statistical_approach=statistical_approach,
            compute_mode=compute_mode,
            threshold_value=threshold_value)
        r = db.execute(sql, params=params)
        if r.lastrowid:
            db.commit()
            return r.lastrowid
        db.rollback()

    @classmethod
    def update(cls, alert_rules_id, statistical_period, statistical_approach, compute_mode, threshold_value):
        sql = ("update {table} set "
               "statistical_period=:statistical_period, statistical_approach=:statistical_approach, compute_mode=:compute_mode, threshold_value=:threshold_value"
               "where alert_rules_id = :alert_rules_id").format(table=cls._table_ar)
        params = dict(
            statistical_period=statistical_period,
            statistical_approach=statistical_approach,
            compute_mode=compute_mode,
            threshold_value=threshold_value)
        r = db.execute(sql, params=params)
        if r.lastrowid:
            db.commit()
        return r.lastrowid
        db.rollback()




