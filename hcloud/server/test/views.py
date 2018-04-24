from flask import Blueprint
from hcloud.middleware.auth import auth

bp = Blueprint('test', __name__)

@bp.route('/test', methods=['GET', 'POST'])
@auth.login_required
def test():
    cmd = "touch /tmp/zhanggong"
    return 'zhanggong'
