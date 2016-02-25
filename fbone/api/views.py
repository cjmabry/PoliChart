# -*- coding: utf-8 -*-

from flask import Blueprint, current_app, request, jsonify
from flask.ext.login import login_user, current_user, logout_user


api = Blueprint('api', __name__, url_prefix='/api')
