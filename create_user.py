import os, sys
import re 
from werkzeug.security import generate_password_hash, check_password_hash

sys.path.append(os.path.join(os.path.dirname(__file__), 'ws')) # Make sure we can import the backend code

from create_app import db, create_app
from db.models import User, Project, UserType


def add_new_entity():
    app, _ = create_app()
    with app.app_context():
        db.create_all()

        email = input('Email: ') or "default"
        regex_email = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if not re.search(regex_email, email):
            raise ValueError("Invalid Email") 
        user = User.query.filter_by(email=email).first()
        if user:
            raise ValueError("ERROR: The email already exists in the database")
        password = input("Password: ") or "default"
        try:
            user_type = input("UserType: ('a': admin, otherwise: general): ")
            user_type = UserType.ADMIN if user_type == 'a' else UserType.GENERAL
        except:
            raise ValueError("UserType doesn't valid")
        entity = User(email=email, password=User.get_hash_password(password), user_type=user_type)
        db.session.add(entity)
        db.session.commit()

if __name__ == "__main__":
    try:
        add_new_entity()
    except Exception as ex:
        print(ex)

