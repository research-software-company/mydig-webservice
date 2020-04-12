import re
import types
import os
import sys
import shutil
import distutils.dir_util
import json
import types
import werkzeug
import codecs
import csv
import subprocess
import threading
import requests
import gzip
import tarfile
import hashlib
import time
import datetime
import random
import signal
import base64
import dateparser
import logging
import jwt

from flask import Flask, Blueprint, render_template, Response, make_response
from flask import request, abort, redirect, url_for, send_file
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from werkzeug.security import check_password_hash

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "\\..\\ws\\")
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "\\..\\db\\")
sys.path.append(os.getcwd())


from create_app import create_app
from basic_auth import requires_auth, TOKEN_COOKIE_NAME

from config import config
import data_persistence
import templates
import rest
from search.elastic_manager import ES

import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import NoBrokersAvailable
from db.models import User, Project, UserType

# logger
logger = logging.getLogger(config['logging']['name'])
log_formatter = logging.Formatter(config['logging']['format'])
if config['logging'].get('file_path') and config['logging']['file_path'] != '':
    log_file = logging.FileHandler(config['logging']['file_path'])
    log_file.setFormatter(log_formatter)
    logger.addHandler(log_file)
else:
    log_stdout = logging.StreamHandler(sys.stdout)
    log_stdout.setFormatter(log_formatter)
    logger.addHandler(log_stdout)
logger.setLevel(config['logging']['level'])
logging.getLogger('werkzeug').setLevel(config['logging']['werkzeug'])

# in-memory data
data = {}

# regex precompile
re_project_name = re.compile(r'^[a-z0-9]{1}[a-z0-9_-]{0,254}$')
re_url = re.compile(r'[^0-9a-z-_]+')
re_doc_id = re.compile(r'^[a-zA-Z0-9_-]{1,255}$')
os_reserved_file_names = ('CON', 'PRN', 'AUX', 'NUL',
                          'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                          'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9')

g_vars = {
    'kafka_producer': None
}

from create_app import db, login_manager
app, api = create_app()

def project_name_not_found(project_name, user):
    if user.user_type == UserType.ADMIN:
        return rest.not_found('Project {} not found'.format(project_name))
    project_name = re.sub('^' + user.slug + '_', '', project_name)
    return rest.not_found('Project {} not found'.format(project_name))

def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=60),
            'user_id': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


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


# utils

def write_to_file(content, file_path):
    with open(file_path, 'w') as f:
        f.write(content)


def update_master_config_file(project_name):
    file_path = os.path.join(get_project_dir_path(project_name), 'master_config.json')
    write_to_file(json.dumps(data[project_name]['master_config'], indent=4), file_path)


def set_status_dirty(project_name):
    data[project_name]['status_memory_dump_worker'].memory_timestamp = time.time()


def update_status_file(project_name):
    status_file_path = os.path.join(get_project_dir_path(project_name), 'working_dir/status.json')
    data_persistence.dump_data(json.dumps(data[project_name]['status'], indent=4), status_file_path)


def set_catalog_dirty(project_name):
    data[project_name]['catalog_memory_dump_worker'].memory_timestamp = time.time()


def update_catalog_file(project_name):
    data_db_path = os.path.join(get_project_dir_path(project_name), 'data/_db.json')
    data_persistence.dump_data(json.dumps(data[project_name]['data']), data_db_path)


def get_project_dir_path(project_name):
    return os.path.join(config['repo']['local_path'], project_name)


def add_keys_to_dict(obj, keys):  # dict, list
    curr_obj = obj
    for key in keys:
        if key not in curr_obj:
            curr_obj[key] = dict()
        curr_obj = curr_obj[key]
    return obj


def tail_file(f, lines=1, _buffer=4098):
    # https://stackoverflow.com/questions/136168/get-last-n-lines-of-a-file-with-python-similar-to-tail
    """Tail a file and get X lines from the end"""
    # place holder for the lines found
    lines_found = []

    # block counter will be multiplied by buffer
    # to get the block size from the end
    block_counter = -1

    # loop until we find X lines
    while len(lines_found) < lines:
        try:
            f.seek(block_counter * _buffer, os.SEEK_END)
        except IOError:  # either file is too small, or too many lines requested
            f.seek(0)
            lines_found = f.readlines()
            break

        lines_found = f.readlines()

        # we found enough lines, get out
        # Removed this line because it was redundant the while will catch
        # it, I left it for history
        # if len(lines_found) > lines:
        #    break

        # decrement the block counter to get the
        # next X bytes
        block_counter -= 1

    return lines_found[-lines:]
