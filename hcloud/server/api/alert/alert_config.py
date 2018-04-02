# -*- coding: UTF-8 -*-

##alert config
NODE_DICT = {
    'port': 9100,
    'interval': 15,
    'item_lst': [
        {'cpu_usage':
            {
                'nick': '一分钟负载',
                'query': 'node_load1{instance="%s:%s"}'
            }
        },
        {'MemAvailable':
            {
                'nick': '可用内存(MB)',
                'query': 'node_memory_MemAvailable{instance="%s:%s"} / 1024 / 1024'
            }
        },
        {'node_disk_bytes_read':
            {
                'nick': '磁盘读(MB)',
                'query': 'node_disk_bytes_read{instance="%s:%s"} / 1024 / 1024 / 1024'
            }
        },
        {'node_network_receive_bytes':
            {
                'nick': '网卡接收(MB)',
                'query': 'node_network_receive_bytes{instance="%s:%s", device="eth0"} / 1024 / 1024'
            }
        }

    ]
}