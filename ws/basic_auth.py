# http://flask.pocoo.org/snippets/8/
from functools import wraps

import jwt
from flask import Response, make_response, request
from flask_login import LoginManager, current_user, login_manager, login_user
from werkzeug.security import check_password_hash, generate_password_hash

import rest
from config import config
from create_app import SECRET_KEY
from db.models import Project, User, UserType

TOKEN_COOKIE_NAME = 'HTTP_TOKEN'


def authenticate(restful=True):
    """Sends a 401 response that enables basic auth"""
    if not restful:
        resp = Response('Invalid credentials', 401)
        resp.headers['WWW-Authenticate'] = 'Basic realm="Restricted"'
        return resp
    return rest.unauthorized('Invalid credentials')

def _decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: user 
    """
    try:
        payload = jwt.decode(auth_token, SECRET_KEY)
        user = User.query.filter_by(id=payload['user_id']).first()
        return user
    except jwt.ExpiredSignatureError:
        raise ValueError('Signature expired. Please log in again.')
    except jwt.InvalidTokenError:
        raise ValueError('Invalid token. Please log in again.')
    except Exception as e:
        raise ValueError(e)

class Unauthorized(Exception):
    pass

def _get_auth_token():
    user_token_header = request.headers.environ.get('HTTP_TOKEN', '')
    user_token_cookie = request.cookies.get('HTTP_TOKEN', '')

    if user_token_header and user_token_cookie and user_token_header != user_token_cookie:
        raise Unauthorized()

    user_token = user_token_header or user_token_cookie
    if not user_token:
        raise Unauthorized()

    return user_token


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            user_token_header = request.headers.environ.get('HTTP_TOKEN', '')
            user_token_cookie = request.cookies.get(TOKEN_COOKIE_NAME, '')

            if user_token_header and user_token_cookie and user_token_header != user_token_cookie:
                return rest.unauthorized('Confusing tokens')

            user_token = user_token_header or user_token_cookie
            user = _decode_auth_token(user_token)
            if not user:
                raise ValueError("Please check your login details and try again.")
        except ValueError as e:
            return rest.unauthorized(str(e))
        return f(*args, **kwargs)
    return decorated

def get_logged_in_user():
    return _decode_auth_token(request.headers.environ.get('HTTP_TOKEN', ''))
