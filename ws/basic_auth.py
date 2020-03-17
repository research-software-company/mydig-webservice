# http://flask.pocoo.org/snippets/8/
import rest
import jwt
from functools import wraps
from flask import request, Response, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager
from werkzeug.security import check_password_hash

from config import config
from models import User, Project, UserType
from create_app import SECRET_KEY


def authenticate(restful=True):
    """Sends a 401 response that enables basic auth"""
    if not restful:
        resp = Response('Invalid credentials', 401)
        resp.headers['WWW-Authenticate'] = 'Basic realm="Restricted"'
        return resp
    return rest.unauthorized('Invalid credentials')

def decode_auth_token(auth_token):
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


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            user_token = request.headers.environ.get('HTTP_TOKEN', '')
            user = decode_auth_token(user_token)
            if not user:
                raise ValueError("Please check your login details and try again.")
        except ValueError as e:
            return rest.unauthorized(str(e))
        return f(*args, **kwargs)
    return decorated
