from hcloud.libs.db.mysql import db

class MonitorData(object):
    _table = 'monitor_item'

    def __init__(
            self, id_, name, nick_name, category, 
            query, aggregation, unit):
        self.id_ = str(id_)
        self.name = name
        self.nick_name = nick_name
        self.category = category
        self.query = query
        self.aggregation = aggregation
        self.unit = unit

    def dump(self):
        req = dict(
            id = self.id_,
            name = self.name,
            nick_name = self.nick_name,
            category = self.category,
            query = self.query,
            aggregation = self.aggregation,
            unit = self.unit
            )
        return req

    @classmethod
    def get_monitor_item_by_category(cls, category):
        sql = ("select id, name, nick_name, category, query, aggregation, unit "
                "from {table} where category=:category").format(table=cls._table)
        params = dict(category=category)
        rs = db.execute(sql, params=params).fetchall()
        db.commit()
        return [ cls(*line) for line in rs ] if rs else []

    @classmethod
    def get_query_metric_by_name(cls, category, name):
        sql = ("select query_metric from {table} "
                "where category=:category and name=:name").format(table=cls._table)
        params = dict(category=category, name=name)
        rs = db.execute(sql, params=params).fetchone()
        db.commit()
        return rs[0] if rs else ''    
    


