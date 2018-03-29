from flask_restful import abort

class ApiException(object):
    ''' Raise a HTTPException '''

    @classmethod
    def handler_hcloud_error(cls, e):
        abort(505, message=str(e))
