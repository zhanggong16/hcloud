from flask import Blueprint
from flask import request
from hcloud.utils import async_cmd_run, sync_cmd_run

bp = Blueprint('test', __name__)

@bp.route('/test', methods=['GET', 'POST'])
def test():
    cmd = "touch /tmp/zhanggong"
    async_cmd_run(cmd)
    return 'zhanggong'
    #res = sync_cmd_run(cmd)
    #return 'hello, %s' % res
