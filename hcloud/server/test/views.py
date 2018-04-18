from flask import Blueprint

bp = Blueprint('test', __name__)

@bp.route('/test', methods=['GET', 'POST'])
def test():
    cmd = "touch /tmp/zhanggong"
    return 'zhanggong'
