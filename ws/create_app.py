import os
import sys
import werkzeug
import hashlib
import random
import signal
import types
import base64
import logging

from flask import Flask, Blueprint, render_template, Response, make_response
from flask import request, abort, redirect, url_for, send_file
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_user, LoginManager
from werkzeug.security import check_password_hash # generate_password_hash

from config import config


def api_route(self, *args, **kwargs):
    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls
    return wrapper


db = SQLAlchemy()
login_manager = LoginManager()
SECRET_KEY = '9OLWxND4o83j4K4iuopOd'

def create_app():
    app = Flask('mydig-webservice')
    # TODO: edit app.config
    app.config.update(MAX_CONTENT_LENGTH=1024 * 1024 * 1024 * 10)
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopOd'
    app.config['SQLALCHEMY_DATABASE_URI'] = config['database_url']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
   
    cors = CORS(app, resources={r"*": {"origins": "*"}}, supports_credentials=True)
    api = Api(app)
    api.route = types.MethodType(api_route, api)

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager.init_app(app)
    with app.app_context():
        db.create_all()
    #db.create_all(app=app)

    return app, api