from hcloud.models.hosts import HostsData
from hcloud.models.monitor import MonitorData
from hcloud.libs.monitor.monitor import Monitor
from hcloud.config import (
    SUMMARY_AGENT_PORT, 
    NODE_AGENT_PORT
    )
from hcloud.logger import logging
import math
import datetime

class MonitorController(object):

    _MONITOR_DISPLAY_LIMIT = 1000

    @classmethod
    def get_id_from_hostspool(cls, key):
        rs = HostsData.get_hostspool_by_host_key(key)
        return rs

    @classmethod
    def get_monitor_item(cls, category):
        rs = MonitorData.get_monitor_item_by_category(category)
        if rs:
            return [ line.dump() for line in rs ]
        else:
            return
    
    @classmethod
    def monitor_data(cls, para_dict, user_id):
        category, name, query, start_timestamp, end_timestamp, interval = para_dict['category'], para_dict['name'], para_dict['query'], para_dict['start'], para_dict['end'], para_dict['interval']
        m = Monitor(user_id)
        
        diff = int(end_timestamp) - int(start_timestamp)
        display_interval = math.ceil(math.ceil(diff / cls._MONITOR_DISPLAY_LIMIT) / float(interval))
        step = int(display_interval * float(interval))
        
        time_format = "%Y-%m-%dT%H:%M:%SZ"
        start_time = datetime.datetime.fromtimestamp(float(start_timestamp))
        end_time = datetime.datetime.fromtimestamp(float(end_timestamp))
        start_str = start_time.strftime(time_format)
        end_str = end_time.strftime(time_format)
        
        query_temp_total = MonitorData.get_query_metric_by_name(category, name)
        status_flag = 0
        data_res = dict()
        axis_list, data_list = [], []
        for query_temp in query_temp_total.split(','):
            if query_temp:
                query_name, query_metric_temp = query_temp.split(':')
                query_metric = query_metric_temp.format(query=query)
                query_metric = query_metric.replace('(', '%28').replace(')', '%29').replace('+', '%2B')
            else:
                logging.error("Monitor: get query_metric failed from database, category: %s, name: %s" % (category, name))
                status_flag = 1
                break
            # get data from monotir api
            data = m.query_range(query_metric, start_str, end_str, step)
            if data.get('status') == 'success':
                try:
                    data = data.get('data').get('result')[0].get('values')
                except Exception as e:
                    logging.error("Monitor data: get data failed, para_dict: %s, error: %s, data: %s." % (para_dict, str(e), data))
                    status_flag = 1
                    break
            else:
                logging.error("Monitor data: monitor return error, para_dict: %s, query: %s, error data: %s." % (para_dict, query_metric, data))
                status_flag = 1
                break
            # assem data
            data_one_dict = {
                'name': query_name
            }
            sub_data_list = []
            axis_flag = 0 if not axis_list else 1
            for item in data:
                axis, sub_data = item
                if axis_flag == 0:
                    axis_list.append(axis)
                sub_data_list.append('%.2f' % float(sub_data))
            data_one_dict['data'] = sub_data_list
            data_list.append(data_one_dict)
        data_res = {
            'axias': axis_list,
            'data': data_list
        }
        return data_res if status_flag == 0 else []

    @classmethod
    def monitor_title(cls, item_list, category, key, user_id):
        
        def _query(data):
            '''
                {u'exported_instance': u'192.168.0.92:9100', u'group': u'gateway', u'exported_job': u'node_group', u'fstype': u'ext4', u'instance': u'114.67.76.108:9091', u'job': u'gateway', u'mountpoint': u'/data', u'device': u'/dev/vdb', u'__name__': u'node_filesystem_free'}
            '''
            res_str = ''
            for k in data:
                if k != '__name__':
                    res_str += "%s='%s'," % (k, data[k])
            return res_str.strip(',')

        device_exclude_list = ['tmpfs', 'rootfs', 'selinuxfs', 'autofs', 'rpc_pipefs', 
                                'rpc_pipefs', 'none', 'devpts', 'sysfs', 'debugfs', 'lo']
        m = Monitor(user_id)
        privateip = HostsData.get_privateip_by_host_key(key)
        summary_exported_instance = '%s:%s' % (privateip, SUMMARY_AGENT_PORT)
        # get summary insterval
        summary_metric = "%s_interval" % category
        data = m.last_data_by_exported_instance(summary_metric, summary_exported_instance)
        if data.get('status') == 'success':
            try:
                interval = data.get('data').get('result')[0].get('value')[-1]
            except Exception as e:
                logging.error("Monitor title: get interval data failed, error %s, data:%s." % (str(e), data))
                return []
        else:
            logging.error("Monitor title: monitor return error, instances %s, error data %s." % (summary_exported_instance, data))
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
                            'interval': interval,
                            'nick_name': item.get('nick_name'),
                            'status': 'success',
                            'unit': item.get('unit')
                        }
                    device_item = d.get('metric').get('device')
                    mountpoint_item = d.get('metric').get('mountpoint')
                    # file
                    if mountpoint_item and device_item:
                        if device_item not in device_exclude_list:
                            item_title_dict['sub_name'] = mountpoint_item
                        else:
                            continue
                    # io, network
                    elif not mountpoint_item and device_item:
                        if device_item not in device_exclude_list:
                            item_title_dict['sub_name'] = device_item
                        else:
                            continue
                    # cpu, memory    
                    else:
                        item_title_dict['sub_name'] = ''
                    item_title_dict['query'] = _query(d.get('metric'))
                    item_title_list.append(item_title_dict)
            except Exception as e:
                item_title_dict = {
                    'name': item.get('name'),
                    'nick_name': item.get('nick_name'),
                    'category': item.get('category'),
                    'aggregation': item.get('aggregation'),
                    'interval': interval,
                    'status': 'failed',
                    'query': '',
                    'unit': ''
                }
                item_title_list.append(item_title_dict)
                logging.error("Monitor: get item %s error, %s" % (item, str(e)))
        return item_title_list
