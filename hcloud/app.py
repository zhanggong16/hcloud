from flask import Flask
from flask_restful import Api
from werkzeug.utils import import_string

apis_lst = import_string('hcloud.server.api.router:apis')

def create_app(config=None):
    app = Flask(__name__)
    api = Api(app)    
    
    #register api
    for api_name in apis_lst: 
        api_class, api_path = api_name
        api.add_resource(api_class, api_path)
    
    return app
