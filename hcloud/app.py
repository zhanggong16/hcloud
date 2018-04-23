from flask import Flask
from flask import Response
from flask_restful import Api
from flask import got_request_exception
from werkzeug.utils import import_string
from werkzeug.datastructures import Headers
from hcloud.logger import logging

apis_lst = import_string('hcloud.server.api.router:apis')

blueprints = [
    'hcloud.server.test.views:bp'
]

def create_app(config=None):
    app = Flask(__name__)
    app.response_class = CorsResponse

    api = Api(app, catch_all_404s=True)    
    
    #record exception to log
    got_request_exception.connect(log_exception, app)
    
    #register api
    for api_name in apis_lst: 
        api_class, api_path = api_name
        api.add_resource(api_class, api_path)
    
    #define blueprint
    for blueprint_name in blueprints:
        blueprint = import_string(blueprint_name)
        app.register_blueprint(blueprint)

    return app

def log_exception(sender, exception, **extra):
    logging.error('Got exception: %s from %s.' % (exception, sender))   

class CorsResponse(Response):

    def __init__(self, response=None, **kwargs):
        kwargs['headers'] = ''
        headers = kwargs.get('headers')
        
        origin = ('Access-Control-Allow-Origin', '*')
        methods = ('Access-Control-Allow-Methods', 'HEAD, OPTIONS, GET, POST, DELETE, PUT')
        if headers:
            headers.add(*origin)
            headers.add(*methods)
        else:
            headers = Headers([origin, methods])
        kwargs['headers'] = headers
        return super(CorsResponse, self).__init__(response, **kwargs)
