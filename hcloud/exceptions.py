from collections import namedtuple
from werkzeug.exceptions import HTTPException
from werkzeug._compat import text_type

Error = namedtuple('Error', ['message', 'http_status_code'])

class HcloudError(HTTPException):
    
    def __init__(self, message=''):
        super(HcloudError, self).__init__(message)
        self.description = message or self._error.message
        self.code = self._error.http_status_code


class NotFound(HcloudError):
    _error = Error('Resource not found', 404)

class ModelsDBError(HcloudError):
    _error = Error('Failed to obtain data from MySQL', 505)

class MonitorError(HcloudError):
    _error = Error('Request monitor api error', 501)

class Error(HcloudError):
    _error = Error('Program error', 500)
