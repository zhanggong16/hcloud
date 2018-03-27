from force.db.store import DistributedSQLStore, init_context
from envcfg.json.hcloud import MYSQL_DSN

master_ctx = init_context('hcloud', dsn=MYSQL_DSN)
slave_ctxes = []
db = DistributedSQLStore.init_by_context(master_ctx, slave_ctxes)
