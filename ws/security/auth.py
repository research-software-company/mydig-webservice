""" This file contains various security related measures.

    1. Token authentication for users.
    2. Cookie-based authentication for users.
    3. Securing the project's name for communicating with dig-ui
"""

from functools import wraps

import jwt
from flask import Response, make_response, request
from flask_login import LoginManager, current_user, login_manager, login_user
from werkzeug.security import check_password_hash, generate_password_hash

import rest
from config import config
from create_app import SECRET_KEY
from db.models import Project, User, UserType
import datetime

TOKEN_COOKIE_NAME = 'TOKEN_IN_COOKIE'

def _get_token_exp(minutes):
    return datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=minutes)

def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    payload = {
        'exp': _get_token_exp(360),
        'user_id': user_id
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )

def _decode_auth_token(auth_token):
    """
    Returns the user object based on the authentication token
    """
    try:
        payload = jwt.decode(auth_token, SECRET_KEY)
        user = User.query.filter_by(id=payload['user_id']).first()
        return user
    except jwt.ExpiredSignatureError:
        raise Unauthorized('Signature expired. Please log in again.')
    except jwt.InvalidTokenError:
        raise Unauthorized('Invalid token. Please log in again.')

def encode_project_token(user_id, project_name):
    payload = {
        'exp': _get_token_exp(minutes=30),
        'user_id': user_id,
        'project_name': project_name,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


class Unauthorized(Exception):
    pass

def _get_auth_token():
    """ Gets the user token from the request. Looking in both the Token: header and 
        the cookie. If both appear and do not have the same token, a 401 is returned.
    """

    user_token_header = request.headers.environ.get('HTTP_TOKEN', '')
    user_token_cookie = request.cookies.get(TOKEN_COOKIE_NAME, '')

    if user_token_header and user_token_cookie and user_token_header != user_token_cookie:
        raise Unauthorized('Mismatching tokens')

    user_token = user_token_header or user_token_cookie
    if not user_token:
        raise Unauthorized('No user token')

    return user_token


def requires_auth(f):
    """ Decorator for requiring authentication in a view """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            user_token = _get_auth_token()
            user = _decode_auth_token(user_token)
            if not user:
                raise Unauthorized("Please check your login details and try again.")
        except Unauthorized as e:
            return rest.unauthorized(str(e))
        return f(*args, **kwargs)
    return decorated

def get_logged_in_user():
    """ Handy function that returns the logged in user for the request """
    token = _get_auth_token()
    user = _decode_auth_token(token)
    return user

def get_project_from_token(project_token):
    """ Returns project_name from project token """
    payload = jwt.decode(project_token, SECRET_KEY)
    return payload['project_name']