from flask import jsonify

class ApiError(object):
    
    @classmethod
    def DataReturn(cls, message):
        status_code = 501
        response = jsonify({
            'status': status_code,
            'description': 'Failed to obtain data from MySQL.',
            'message': message
        })
        response.status_code = status_code
        return response
