from hcloud.models.hosts import HostsData
from hcloud.models.monitor import MonitorData
from hcloud.libs.monitor.monitor import Monitor
from hcloud.config import (
    SUMMARY_AGENT_PORT, 
    NODE_AGENT_PORT
    )
from hcloud.logger import logging

class MonitorController(object):

    @classmethod
    def get_id_from_hostspool(cls, host_key):
        rs = HostsData.get_hostspool_by_host_key(host_key)
        return rs

    @classmethod
    def get_monitor_item(cls, category):
        rs = MonitorData.get_monitor_item_by_category(category)
        if rs:
            return [ line.dump() for line in rs ]
        else:
            return

    @classmethod
    def monitor_title(cls, item_list, category, host_key, user_id):
        include_list = ['tmpfs', 'rootfs', 'lo']
        m = Monitor(user_id)
        privateip = HostsData.get_privateip_by_host_key(host_key)
        summary_exported_instance = '%s:%s' % (privateip, SUMMARY_AGENT_PORT)
        # get summary insterval
        summary_metric = "%s_interval" % category
        data = m.last_data_by_exported_instance(summary_metric, summary_exported_instance)
        if data.get('status') == 'success':
            try:
                interval = data.get('data').get('result')[0].get('value')[-1]
            except Exception:
                logging.error("Monitor: get summary interval failed, %s." % data)
                return []
        else:
            logging.error("Monitor: get %s summary failed." % exported_instance)
            return []
        # get summary port
        if category == 'node':
            port = NODE_AGENT_PORT
        else:
            port = SUMMARY_AGENT_PORT
        exported_instance = '%s:%s' % (privateip, port)
        # get item title
        item_title_list = []
        for item in item_list:
            query_metric = item.get('query')
            data = m.last_data_by_exported_instance(query_metric, exported_instance)
            try:
                data_list = data.get('data').get('result')
                for d in data_list:
                    item_title_dict = {
                            'name': item.get('name'),
                            'category': item.get('category'),
                            'aggregation': item.get('aggregation'),
                            'interval': '%ss' % interval,
                            'status': 'success',
                        }
                    judge_item = d.get('metric').get('device')
                    # disk, network
                    if judge_item:
                        if judge_item not in include_list:
                            item_title_dict['nick_name'] = '%s-%s' % (item.get('nick_name'), judge_item)
                        else:
                            continue
                    # cpu, memory    
                    else:
                        item_title_dict['nick_name'] = item.get('nick_name')
                    item_title_list.append(item_title_dict)
            except Exception:
                item_title_dict = {
                    'name': item.get('name'),
                    'nick_name': item.get('nick_name'),
                    'category': item.get('category'),
                    'aggregation': item.get('aggregation'),
                    'interval': interval,
                    'status': 'failed',
                }
                item_title_list.append(item_title_dict)
        return item_title_list
