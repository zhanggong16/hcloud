from flask_restful import Resource
from flask_restful import abort
from flask import request
from hcloud.server.api.alert.controller import AlertManager

class Alert(Resource):

    def post(self):
        try:
            json_data = request.get_json(force=True)
            AlertManager.send(json_data)
        except Exception as e:
            abort(501, message=str(e), error="Alert post error")
        return json_data