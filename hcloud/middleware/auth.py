from flask import g
from flask_httpauth import HTTPTokenAuth

auth = HTTPTokenAuth(scheme='Hcloud')

tokens = {
    "secret-token-1": "John",
    "secret-token-2": "Susan"
}

@auth.verify_token
def verify_token(token):
    g.user = None
    if token in tokens:
        g.user = tokens[token]
        return True
    return False
