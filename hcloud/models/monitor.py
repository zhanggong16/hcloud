from hcloud.libs.db.mysql import db

class MonitorData(object):
    _table = 'monitor_item'

    def __init__(
            self, id_, name, nick_name, category, 
            query, aggregation):
        self.id_ = str(id_)
        self.name = name
        self.nick_name = nick_name
        self.category = category
        self.query = query
        self.aggregation = aggregation

    def dump(self):
        req = dict(
            id = self.id_,
            name = self.name,
            nick_name = self.nick_name,
            category = self.category,
            query = self.query,
            aggregation = self.aggregation)
        return req

    @classmethod
    def get_monitor_item_by_category(cls, category):
        sql = ("select id, name, nick_name, category, query, aggregation "
                "from {table} where category=:category").format(table=cls._table)
        params = dict(category=category)
        rs = db.execute(sql, params=params).fetchall()
        db.commit()
        return [ cls(*line) for line in rs ] if rs else []
