from flask_restful import abort

class ApiException(object):
    ''' Raise a HTTPException '''

    @classmethod
    def get_data_from_mysql_error(cls, e):
        abort(505, message=str(e))

    @classmethod
    def data_not_found(cls, id_):
        abort(404, message='The operating resources: %s do not exist.' % id_)
