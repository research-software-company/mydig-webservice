from app_base import *

from security.auth import encode_project_token, requires_auth, get_logged_in_user

@app.route('/login', methods=['POST'])
def login_post():
    email = request.authorization.get('username').strip()
    password = request.authorization.get('password').strip()
    try:
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):  # user.password == password: 
            return rest.not_found("Please check your login details and try again.")
        token = encode_auth_token(user.id)
    except Exception as e:
        return rest.unauthorized(e)

    resp = make_response(token)
    resp.set_cookie(TOKEN_COOKIE_NAME, token)
    return resp
