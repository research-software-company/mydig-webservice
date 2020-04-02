import os, sys
import re 
import argparse
from secrets import token_hex
from werkzeug.security import generate_password_hash

sys.path.append(os.path.join(os.path.dirname(__file__), 'ws')) # Make sure we can import the backend code

from create_app import db, create_app
from db.models import User, Project, UserType

# python create_user.py <email> <password> --admin 

def create_new_user(email, password, admin):
    app, _ = create_app()
    with app.app_context():
        db.create_all()

        regex_email = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if not re.search(regex_email, email):
            raise ValueError("Invalid Email")
        user = User.query.filter_by(email=email).first()
        user_type = UserType.ADMIN if admin else UserType.GENERAL
        if user:
            user.password = User.get_hash_password(password)
            user.user_type = user_type
            db.session.commit()
            print("Update:\nuser: {}, password: {}, permissions: {}"
                    .format(email, password, user_type))
        else:
            slug = token_hex(7) # len=14
            user = User(email=email, password=User.get_hash_password(password), user_type=user_type, slug=slug)
            db.session.add(user)
            db.session.commit()

if __name__ == "__main__":
    """
    python create_user.py <email> <password> --admin 
    """
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("email", help="The Email address of the user")
        parser.add_argument("password", help="The password")
        parser.add_argument("--admin", action="store_true", default=False,
                            help="Set the user permissions to 'Admin'")
        args = parser.parse_args()

        create_new_user(**vars(args))
    except Exception as ex:
        print(ex)

