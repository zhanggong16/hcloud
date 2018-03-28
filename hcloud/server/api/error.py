from flask_restful import abort

class ApiException(object):

    @classmethod
    def nodatareturn(cls, e):
        abort(501, message=str(e), error="No data return from MySQL.")

