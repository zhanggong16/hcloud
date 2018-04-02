import uuid
from hcloud.models.alert_rules import AlertRulesData



class AlertManager(object):
    @classmethod
    def send(cls, alertinfo):
        print alertinfo

    def create_alert_rules(cls, *add):
        service, monitor_items, statistical_period, statistical_approach, compute_mode, threshold_value = add
        alert_rules_id = str(uuid.uuid1())
        host_id = str(uuid.uuid1())
        rs = AlertRulesData.add(alert_rules_id, host_id, service, monitor_items, statistical_period, statistical_approach, compute_mode, threshold_value)
        return rs

    def update_alert_rules(cls, *update):
        alert_rules_id, statistical_period, statistical_approach, compute_mode, threshold_value = update
        rs = AlertRulesData.update(alert_rules_id,statistical_period, statistical_approach, compute_mode, threshold_value)
        return rs